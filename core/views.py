from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import resolve, reverse
from django.db import transaction
from core.forms import CouponForm, RefundForm
from django.http import HttpResponse
from django.db.models import Q

import stripe

from .models import Item, Address, Coupon, Order, OrderItem, Payment, Refund
from .forms import CheckoutForm


stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(ListView):
    model = Item
    template_name = "home.html"
    context_object_name = "items"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # get human-readable categories
        context['categories'] = list(zip(*Item.CATEGORY_CHOICES))[1]

        return context

    def get_queryset(self):
        # original queryset
        items = Item.objects.all()

        # selection part: filter is applied first, then search
        filter_query_val = self.request.GET.get('filter', None)
        search_query_val = self.request.GET.get('search', None)

        if filter_query_val:
            if filter_query_val == 'sale':
                items = items.filter(discount_price__isnull=False)
            else:
                # Extra search part is needed for filtering
                # by HUMAN-READABLE category values
                # e.g:  ?filter=shirt    -> searching by S
                #       ?filter=S        -> searching by S
                extra_search_val = dict(
                    map(lambda string: string.lower(), (v, k))
                    for k, v in Item.CATEGORY_CHOICES
                ).get(filter_query_val, '')

                items = items.filter(
                    Q(category__iexact=filter_query_val) | Q(category__iexact=extra_search_val))

        if search_query_val:
            items = items.filter(Q(title__icontains=search_query_val))

        return items.order_by('-time_added')


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add in a QuerySet recommended items
        item_object = context['item']
        same_category_recommendations = Item.objects.filter(
            category=item_object.category).exclude(id=item_object.id).order_by('-id')[:5]

        if not same_category_recommendations.exists():
            another_recommendations = Item.objects.all().exclude(
                id=item_object.id).order_by('-id')[:5]

            print(another_recommendations)
            context['recommended'] = another_recommendations
        else:
            context['recommended'] = same_category_recommendations

        return context


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            order = Order.objects.create(user=self.request.user)

        context = {"order": order}
        return render(self.request, "order_summary.html", context)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        checkout_form = CheckoutForm()
        coupon_form = CouponForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': checkout_form,
            'couponForm': coupon_form,
            'order': order
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        if not form.is_valid():
            messages.warning(self.request, "Please, enter correct data")
            return redirect("core:checkout-page")

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"objects": order}
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        phone_number = form.cleaned_data.get('phone_number')

        street_address = form.cleaned_data.get('street_address')
        apartment_address = form.cleaned_data.get('apartment_address')
        country = form.cleaned_data.get('country')
        zip_code = form.cleaned_data.get('zip_code')

        # save_info = form.cleaned_data.get('save_info')
        payment_option = form.cleaned_data.get('payment_option')

        billing_address = Address(
            user=self.request.user,
            street_address=street_address,
            apartment_address=apartment_address,
            country=country,
            zip_code=zip_code,
            # same_shipping_address=same_shipping_address,
            # save_info=save_info,
            # payment_option=payment_option
        )
        billing_address.save()

        order.shipping_address = billing_address
        order.save()

        if payment_option == 'S':
            return redirect('core:payment', payment_option='stripe')
        elif payment_option == 'P':
            return redirect('core:payment', payment_option='paypal')
        else:
            messages.warning(self.request, 'Invalid payment option selected')
            return redirect('core:checkout')

        return redirect("core:checkout-page")


@login_required
def add_to_cart(request, *args, **kwargs):
    item = get_object_or_404(Item, *args, **kwargs)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "Your cart was successfully updated!")
        else:
            order.items.add(order_item)
            messages.success(request, "This item was added into your cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, "This item was added into your cart")

    # Get redirect url
    redirect_to = request.GET.get("redirect_to", "core:product-page")
    return redirect(redirect_to, *args, **kwargs)


@login_required
def remove_from_cart(request, slug, all_items=True, *args, **kwargs):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]

            if all_items or order_item.quantity <= 1:
                order.items.remove(order_item)
                order_item.delete()
                messages.success(
                    request, "All these itemes were removed from your cart")
            else:
                order_item.quantity -= 1
                order_item.save()
                messages.success(
                    request, f"One item of {order_item.item.title} was removed from your cart")
                return redirect("core:order-summary")
        else:
            messages.warning(request, "This item was not in your cart")
    else:
        messages.warning(request, "You do not have an active order")

    return redirect("core:product-page", slug=slug)


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        if order.shipping_address:
            context = {
                'order': order
            }

            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You do not enter you shipping address")
            return redirect("core:checkout-page")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        token = self.request.POST.get('stripeToken')
        amount = int(order.get_order_price() * 100)

        try:
            # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_order_price()
            payment.save()

            order.ordered = True
            order.payment = payment
            order.ordered_date = timezone.now()
            order.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            with transaction.atomic():
                for item in order_items:
                    item.save()

            messages.success(
                self.request, "Your order was successfully processed")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Authentication failed")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, "Something went wrong")
        except Exception as e:
            # Send an email to ourselves
            messages.warning(self.request, "A seriuos error occured.")

        return redirect('/')


class AddCouponView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)

        if form.is_valid():
            try:
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                code = form.cleaned_data.get('code')

                try:
                    coupon = Coupon.objects.get(code=code)
                except ObjectDoesNotExist:
                    messages.warning(
                        self.request, "This coupon does not exist")
                    return redirect("core:checkout-page")

                order.coupon = coupon
                order.save()

                messages.success(
                    self.request, "Coupon was successfully applied")
                return redirect("core:checkout-page")
            except ObjectDoesNotExist:
                messages.warning(
                    self.request, "You do not have an active order")
                return redirect("core:checkout-page")


class RequestRefundView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {
            'form': RefundForm()
        }
        return render(self.request, "refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST or None)

        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')

            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()
            except ObjectDoesNotExist:
                messages.warning(self.request, "The order does not exist")
                return redirect("core:refund")

            refund = Refund()
            refund.order = order
            refund.reason = message
            refund.email = email
            refund.save()

            messages.success(self.request, "Your refund request was received!")
            return redirect("/")


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(ordered=True, user=self.request.user)

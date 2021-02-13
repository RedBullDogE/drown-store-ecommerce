from django.urls import path

from .views import (AddCouponView, CheckoutView, HomeView, ItemDetailView,
                    OrderListView, OrderSummaryView, PaymentView,
                    RequestRefundView, add_to_cart, remove_from_cart)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('checkout/', CheckoutView.as_view(), name='checkout-page'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product-page'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug>/all/',
         remove_from_cart, name='remove-from-cart-all'),
    path('remove_from_cart/<slug>/', remove_from_cart,
         {'all_items': False}, name='remove-from-cart-single'),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('refund/', RequestRefundView.as_view(), name='refund'),
    path('orders/', OrderListView.as_view(), name='order-list')
]

from django.template import Library
from core.models import Order

register = Library()


@register.filter(name='range')
def paginator_range(number):
    return range(1, number + 1)


@register.filter(name='item_count')
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)

        if qs.exists():
            return qs[0].items.count()

        return 0

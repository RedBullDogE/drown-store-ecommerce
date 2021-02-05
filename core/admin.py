from django.contrib import admin

from .models import *


# Custom admin actions
def make_refund_accepted(model_admin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'

# Admin classes


class ItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'time_added']


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ref_code',
        'ordered',
        'being_delivered',
        'received',
        'refund_requested',
        'refund_granted',
        'shipping_address',
        'payment',
        'coupon'
    ]

    list_display_links = [
        'user',
        'shipping_address',
        'payment',
        'coupon'
    ]

    list_filter = [
        'user',
        'ordered',
        'being_delivered',
        'received',
        'refund_requested',
        'refund_granted'
    ]

    search_fields = [
        'user__username',
        'ref_code'
    ]

    actions = [make_refund_accepted]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['get_title', 'user', 'ordered', 'quantity']

    def get_title(self, obj):
        return obj.item.title

    get_title.short_description = 'Item Title'
    get_title.admin_order_field = 'item'


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip_code',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip_code']


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)

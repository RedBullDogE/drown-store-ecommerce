from django.db import models
from django.conf import settings
from django.urls import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


from re import sub

from .utils import generate_random_code
from django.db.models import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify

# from background_task import background

# TODO: Add 'New' label autoset

# TODO: Add thumbnail creation for product photos


class Item(models.Model):
    CATEGORY_CHOICES = (
        ('S', 'Sport'),
        ('C', 'Casual'),
        ('F', 'Formal'),
    )

    LABEL_CHOICES = (
        ('B', 'bestseller'),
        ('BP', 'best price')
    )

    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=1, null=True, blank=True)
    description = models.TextField(default='', blank=True, null=True)

    time_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(
        upload_to="clothes_pictures", default="default.png")

    def get_absolute_url(self):
        return reverse('core:product-page', kwargs={
            'slug': self.slug
        })

    def is_ordered(self):
        return self.order_item.filter(ordered=False).exists()

    def is_new(self):
        return timezone.now() - self.time_added < timezone.timedelta(days=1)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet

            # generating slug field from title
            title_slug_part = slugify(self.title)
            random_slug_part = generate_random_code(8)
            self.slug = f"{title_slug_part}-{random_slug_part}".lower()

        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.slug})'


class OrderItem(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='order_item')
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def get_total_price(self):
        return (self.item.discount_price or self.item.price) * self.quantity

    def get_discount(self):
        return (self.item.price - self.item.discount_price or self.item.price) * self.quantity

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'


class Order(models.Model):
    """
    1. Adding to cart
    2. Adding a billing address
    (failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc)
    4. Being delivered
    5. Received
    6. Refunds
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(
        unique=True, max_length=20, default=generate_random_code(20))
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    shipping_address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='shipping_address'
    )

    payment = models.ForeignKey(
        'Payment',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def get_order_price(self):
        order_price_dirty = sum([order_item.get_total_price()
                                 for order_item in self.items.all()])

        if self.coupon and self.items.count():
            coupon_amount = self.coupon.amount

            if self.coupon.discount_type == 'A':
                return order_price_dirty - coupon_amount
            else:
                return order_price_dirty * (100 - coupon_amount) / 100

        return order_price_dirty


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(max_length=20)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('A', 'Absolute'),
        ('R', 'Relative'),
    )

    code = models.CharField(max_length=15)
    discount_type = models.CharField(
        max_length=1, choices=DISCOUNT_TYPE_CHOICES, default='A')
    amount = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            if self.amount < 0:
                raise ValidationError(
                    'Amount value of coupon must be greater than zero')

            if self.discount_type == 'R' and self.amount > 100:
                raise ValidationError(
                    'Amount value of RELATIVE type coupon should be a percent value (between 0 and 100%)')

        super(Coupon, self).save(*args, **kwargs)

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.order.ref_code}"

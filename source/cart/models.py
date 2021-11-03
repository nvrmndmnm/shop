from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from storefront.models import BaseModel, Product

status_choices = [
    ('NEW', 'New'),
    ('PROCESSING', 'Processing'),
    ('ON_DELIVERY', 'On delivery'),
    ('CANCELED', 'Canceled'),
    ('RETURNED', 'Returned'),
    ('FINISHED', 'Finished')
]


class Order(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Order user')
    items = models.ManyToManyField('cart.OrderItem', verbose_name='Items')
    address = models.ForeignKey('cart.Address', related_name='address',
                                on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(choices=status_choices, max_length=50, verbose_name="Status")
    finished_date = models.DateField(blank=True, null=True, verbose_name='Finished date')

    def __str__(self):
        return f"{self.pk} - {self.user}"

    def get_subtotal(self):
        total = 0
        for item in self.items.all():
            total += item.get_subtotal()
        return total

    def get_shipping(self):
        if self.get_subtotal() > 5000:
            return 0
        return 1000

    def get_total(self):
        return self.get_subtotal() + self.get_shipping()


class OrderItem(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Cart user')
    item = models.ForeignKey('storefront.Product', on_delete=models.CASCADE, verbose_name='Order item')
    quantity = models.IntegerField(default=1, verbose_name='Items quantity')
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity}x{self.item.title}"

    def get_subtotal(self):
        return self.item.stock.price * self.quantity


class Address(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Address user')
    street = models.CharField(max_length=100, verbose_name='Street')
    building = models.CharField(max_length=20, verbose_name='Building')
    apartment = models.CharField(max_length=20, verbose_name='Apartment', null=True, blank=True)
    country = CountryField(default='KZ', verbose_name='Country')
    zip_code = models.CharField(max_length=20, verbose_name='Zip code')

    def __str__(self):
        return f'{self.user} - {self.zip_code}'

from django.contrib import admin
from cart.models import Order, OrderItem, Address

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address)

from django.contrib import admin
from storefront.models import Product, Category, Brand, Stock, ImageContainer, Image


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Stock)
admin.site.register(ImageContainer)
admin.site.register(Image)

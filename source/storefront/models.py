from django.db import models


class BaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    sku = models.CharField(max_length=50, verbose_name='Product SKU')
    title = models.CharField(max_length=255, verbose_name='Product title')
    category = models.ForeignKey('storefront.Category', on_delete=models.RESTRICT,
                                 verbose_name='Product category', related_name='category')
    brand = models.ForeignKey('storefront.Brand', on_delete=models.RESTRICT,
                              verbose_name='Product brand', related_name='brand')
    image_container = models.ForeignKey('storefront.ImageContainer', on_delete=models.CASCADE,
                                        verbose_name='Product images', related_name='images')
    stock = models.ForeignKey('storefront.Stock', on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Product stock', related_name='stock')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return f"{self.id} - {self.title}"


class Category(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Category title')
    parent_cat = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True, verbose_name='Parent category',
                                   related_name='parent_category')

    def __str__(self):
        return f"{self.id} - {self.title}"


class Brand(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Brand title')
    logo = models.ImageField(null=True, blank=True, upload_to='brand_logos', verbose_name='Brand logo')

    def __str__(self):
        return f"{self.id} - {self.title}"


class Stock(BaseModel):
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Discount price")

    def __str__(self):
        return f"{self.id}"


class ImageContainer(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Image(BaseModel):
    file = models.ImageField(upload_to='product_images', verbose_name='Product image')
    container = models.ForeignKey('storefront.ImageContainer', on_delete=models.CASCADE,
                                  verbose_name='Images container', related_name='image_container')

    def __str__(self):
        return f"{self.id} - {self.container.title}"

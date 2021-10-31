from django import forms
from storefront.models import Product, Category, Brand, ImageContainer, Image, PriceList


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = 'widgets/image_widget.html'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'brand', 'title', 'category', 'description']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = PriceList
        fields = ['file']


class ImageContainerForm(forms.ModelForm):
    images = forms.ModelMultipleChoiceField(queryset=Image.objects.all(), label='Images')

    class Meta:
        model = ImageContainer
        fields = ['images']
        # widgets = {'images': }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file']


class CategoryForm(forms.ModelForm):
    parent_cat = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['title', 'parent_cat']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['title', 'logo']

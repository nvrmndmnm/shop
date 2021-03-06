import csv
from io import StringIO

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView, FormView

from cms.forms import ProductForm, CategoryForm, BrandForm, ImageContainerForm, ImageForm, UploadFileForm
from storefront.models import Product, Category, Brand, ImageContainer, Stock, PriceList
from storefront.views import ProductSearchView


class CMSProductSearchView(ProductSearchView):
    template_name = 'inventory/product/list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-time_created')
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product/create.html'

    def get_context_data(self, **kwargs):
        if 'image_form' not in kwargs:
            kwargs['image_form'] = self.get_image_form()
        return super().get_context_data(**kwargs)

    def get_image_form(self):
        form_kwargs = {}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ImageForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        image_form = self.get_image_form()
        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form, image_form)

    def form_valid(self, form, image_form):
        product = form.save(commit=False)
        product.image_container = ImageContainer.objects.create(title=product.sku)
        image = image_form.save()
        image.code = image.filename()
        image.save()
        product.image_container.images.add(image)
        product.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, image_form):
        context = self.get_context_data(form=form, image_form=image_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('cms:products')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product/update.html'

    def get_context_data(self, **kwargs):
        if 'image_container_form' not in kwargs:
            kwargs['image_container_form'] = self.get_image_container_form()
        if 'image_form' not in kwargs:
            kwargs['image_form'] = self.get_image_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_container_form = self.get_image_container_form()
        image_form = self.get_image_form()
        if form.is_valid() and image_container_form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_container_form, image_form)
        else:
            return self.form_invalid(form, image_container_form, image_form)

    def form_valid(self, form, image_container_form, image_form):
        response = super().form_valid(form)
        image = image_form.save()
        image.code = image.filename()
        image.save()
        image_container = image_container_form.save(commit=False)
        image_container.images.add(image)
        image_container.save()
        return response

    def form_invalid(self, form, image_container_form, image_form):
        context = self.get_context_data(form=form, image_form=image_form, image_container_form=image_container_form)
        return self.render_to_response(context)

    def get_image_container_form(self):
        form_kwargs = {'instance': self.object.image_container}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ImageContainerForm(**form_kwargs)

    def get_image_form(self):
        form_kwargs = {'instance': self.object.image_container.images.add()}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ImageForm(**form_kwargs)

    def get_success_url(self):
        return reverse_lazy('cms:products')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'inventory/product/delete.html'
    success_url = reverse_lazy('cms:products')


class PriceCreateView(CreateView):
    model = PriceList
    form_class = UploadFileForm
    template_name = 'inventory/product/upload_stock.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        price_list = form.save()
        price_list.code = price_list.filename()
        price_list.save()
        update_stocks(price_list.file)
        return response

    def get_success_url(self):
        return reverse_lazy('cms:products')


def update_stocks(csv_upload):
    file = csv_upload.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')

    for row in csv_data:
        row_dict = dict((x, y) for x, y in enumerate(row))
        product = get_object_or_404(Product, sku=row_dict.get(0))
        product.stock = Stock.objects.create(price=row_dict.get(1),
                                             quantity=row_dict.get(2),
                                             discount_price=row_dict.get(3, None))
        product.save()


class CMSCategorySearchView(ProductSearchView):
    template_name = 'inventory/category/list.html'

    def get_queryset(self):
        queryset = Category.objects.all().order_by('title')
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        category = form.save()
        if category.parent_cat:
            category.parent_cat.is_parent = True
            category.parent_cat.save()
        return response

    def get_success_url(self):
        return reverse_lazy('cms:categories')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category/update.html'

    def get_success_url(self):
        return reverse_lazy('cms:categories')


class CMSBrandSearchView(CMSProductSearchView):
    template_name = 'inventory/brand/list.html'

    def get_queryset(self):
        queryset = Brand.objects.all().order_by('title')
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/brand/create.html'

    def get_success_url(self):
        return reverse_lazy('cms:brands')


class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/brand/update.html'

    def get_success_url(self):
        return reverse_lazy('cms:brands')

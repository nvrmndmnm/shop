from django.db.models import Q
from django.shortcuts import render
from django.utils.http import urlencode
from django.views.generic import View, ListView, DetailView

from storefront.forms import SearchForm
from storefront.models import Product, Image


class ProductSearchView(ListView):
    model = Product
    template_name = 'product_list.html'
    ordering = ['-time_created']
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        self.search_form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search_form'] = self.search_form
        if self.search_value:
            context['query'] = urlencode({'q': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset().exclude(stock__isnull=True).filter(stock__quantity__gt=0)
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset

    def get_query(self):
        query = Q(title__icontains=self.search_value)
        return query

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.search_form.is_valid():
            return self.search_form.cleaned_data['q']


class IndexView(ProductSearchView):
    template_name = 'index.html'
    paginate_by = 12


class ProductListView(ProductSearchView):
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk'):
            queryset = queryset.filter(category_id=self.kwargs['pk'])
        return queryset


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset().exclude(stock__isnull=True).exclude(image_container__isnull=True)
        return queryset


class DeliveryPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'info_pages/delivery.html')


class BenefitsPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'info_pages/benefits.html')


class ReturnPolicyPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'info_pages/return_policy.html')

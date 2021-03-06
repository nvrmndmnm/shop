from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DetailView

from cart.models import Order
from storefront.views import ProductSearchView


class OrderSearchView(PermissionRequiredMixin, ProductSearchView):
    template_name = 'orders/list.html'
    paginate_by = 10
    permission_required = 'employee'
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = Order.objects.all().order_by('time_created')
        if self.search_value:
            query = self.get_query()
            queryset = queryset.filter(query)
        return queryset

    def get_query(self):
        query = Q(id__icontains=self.search_value)
        return query


class NewOrderListView(PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'orders/list.html'
    paginate_by = 10
    ordering = ['time_created']
    permission_required = 'employee'
    login_url = 'accounts:login'

    def get_queryset(self):
        return Order.objects.filter(status='PROCESSING')


class ProcessedOrderListView(NewOrderListView):
    def get_queryset(self):
        return Order.objects.filter(status='ON_DELIVERY')


class ArchivedOrderListView(NewOrderListView):
    def get_queryset(self):
        return Order.objects.filter(status__in=['CANCELED', 'RETURNED', 'FINISHED'])


class OrderDetailView(PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'
    permission_required = 'employee'
    login_url = 'accounts:login'


@permission_required(perm='employee', login_url='accounts:login')
def order_processed(request, **kwargs):
    order = get_object_or_404(Order, pk=kwargs.get("pk"))
    order.status = 'ON_DELIVERY'
    order.save()
    return redirect('cms:orders_new')


@permission_required(perm='employee', login_url='accounts:login')
def order_delivered(request, **kwargs):
    order = get_object_or_404(Order, pk=kwargs.get("pk"))
    order.status = 'FINISHED'
    order.finished_date = datetime.now()
    order.save()
    return redirect('cms:orders_new')


@permission_required(perm='employee', login_url='accounts:login')
def order_canceled(request, **kwargs):
    order = get_object_or_404(Order, pk=kwargs.get("pk"))
    order.status = 'CANCELED'
    order.save()
    return redirect('cms:orders_new')


@permission_required(perm='employee', login_url='accounts:login')
def order_returned(request, **kwargs):
    order = get_object_or_404(Order, pk=kwargs.get("pk"))
    order.status = 'RETURNED'
    order.save()
    return redirect('cms:orders_new')

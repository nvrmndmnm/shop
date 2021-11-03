from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, CreateView
from cart.forms import AddressForm, OrderItemQuantityForm
from storefront.models import Product
from cart.models import Order, OrderItem, Address


class CartSummaryView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'cart_summary.html'

    def get_object(self, queryset=None):
        try:
            return Order.objects.filter(user=self.request.user, status='NEW', items__isnull=False).first()
        except ObjectDoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if order:
            for item in order.items.all():
                product = get_object_or_404(Product, pk=item.item.pk)
                if item.quantity > product.stock.quantity:
                    messages.info(self.request,
                                  f'You added more products to your cart than we currently have in our stock. '
                                  f'We adjusted the quantity of [{item.item.title}].')
                    item.quantity = product.stock.quantity
                    item.save()
        return super().get(request, *args, **kwargs)


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'checkout.html'
    form_class = AddressForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.order = self.get_order()
        return super().dispatch(request, *args, **kwargs)

    def get_order(self):
        try:
            return Order.objects.filter(user=self.request.user, status='NEW', items__isnull=False).first()
        except ObjectDoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        self.order.address = address
        self.order.status = 'PROCESSING'
        for order_item in self.order.items.all():
            print(order_item.ordered)
            order_item.ordered = True
            order_item.save()
            print(order_item.ordered)
        self.order.save()
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('cart:order_complete')

# class CheckoutView(LoginRequiredMixin, FormView):
#     template_name = 'checkout.html'
#     form_class = AddressForm
#
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             self.order = self.get_order()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         self.form = self.get_form()
#         if self.form.is_valid():
#             print('tes')
#         else:
#             return reverse('cart:checkout')
#
#     def get_order(self):
#         try:
#             return Order.objects.filter(user=self.request.user, status='NEW', items__isnull=False).first()
#         except ObjectDoesNotExist:
#             return None
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['order'] = self.order
#         return context
#
#     def form_valid(self, form):
#         print(form)
#         self.address = form.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('cart:order_complete')


class OrderCompleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'order_complete.html')


@login_required
def add_to_cart(request, **kwargs):
    item = get_object_or_404(Product, pk=kwargs.get("pk"))
    order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item, ordered=False)
    order_qs = Order.objects.filter(user=request.user, status='NEW')
    quantity = 1
    if request.method == 'POST':
        form = OrderItemQuantityForm(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
    if created:
        order_item.quantity = quantity
        order_item.save()
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += quantity
            order_item.save()
            # messages.info(request, 'Another product added.')
        else:
            # messages.info(request, 'Product added to your cart.')
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, status='NEW')
        order.items.add(order_item)
        # messages.info(request, 'Product added to your cart.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_cart(request, **kwargs):
    item = get_object_or_404(Product, pk=kwargs.get("pk"))
    order_qs = Order.objects.filter(user=request.user, status='NEW')
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            # messages.info(request, 'Product removed from your cart.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            # messages.info(request, 'Product was not in the cart.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # messages.info(request, 'You do not have an order.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


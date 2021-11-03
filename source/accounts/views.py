from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from cart.models import Order


class UserCreateView(CreateView):
    model = get_user_model()
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('storefront:index')
        return next_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'detail.html'
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_orders'] = self.get_user_orders()
        return context

    def get_user_orders(self):
        return Order.objects.filter(user=self.get_object())


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'update_profile.html'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:profile')


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'update_password.html'

    def get_success_url(self):
        return reverse('accounts:profile')


from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


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


class UserDetailView(UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = 'detail.html'
    context_object_name = 'user_obj'
    permission_required = 'auth.view_user'

    def test_func(self):
        return self.request.user == self.get_object() or\
               self.request.user.has_perm(self.permission_required)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'update_profile.html'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'update_password.html'

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})


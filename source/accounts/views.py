from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView


class UserListView(ListView):
    model = get_user_model()
    template_name = 'list.html'

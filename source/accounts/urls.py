from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import UserListView

app_name = 'accounts'

urlpatterns = [
    path('', UserListView.as_view(), name='profiles')
]

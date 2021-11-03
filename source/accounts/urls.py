from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import UserCreateView, UserDetailView, UserUpdateView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('change-password/', UserPasswordChangeView.as_view(), name='update_password')
]

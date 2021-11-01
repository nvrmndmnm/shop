from django.urls import path
from cart import views as cart_views

app_name = 'cart'

urlpatterns = [
    path('', cart_views.add_to_cart, name='add_to_cart'),
]

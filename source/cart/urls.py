from django.urls import path
from cart import views as cart_views

app_name = 'cart'

urlpatterns = [
    path('', cart_views.CartSummaryView.as_view(), name='cart_summary'),
    path('checkout/', cart_views.CheckoutView.as_view(), name='checkout'),
    path('complete/', cart_views.OrderCompleteView.as_view(), name='order_complete'),
    path('add/<int:pk>', cart_views.add_to_cart, name='add_to_cart'),
    path('remove/<int:pk>', cart_views.remove_from_cart, name='remove_from_cart')
]

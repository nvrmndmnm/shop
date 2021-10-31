from django.urls import path
from storefront import views as storefront_views

app_name = 'storefront'

urlpatterns = [
    path('', storefront_views.IndexView.as_view(), name='index'),
    path('p/<int:pk>/', storefront_views.ProductDetailView.as_view(), name='product'),
    path('c/<int:pk>/', storefront_views.ProductListView.as_view(), name='category'),
    path('search/', storefront_views.ProductSearchView.as_view(), name='search')
]

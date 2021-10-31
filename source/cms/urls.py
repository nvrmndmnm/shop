from django.urls import path
from cms import views as cms_views

app_name = 'cms'

urlpatterns = [
    path('', cms_views.ProductListView.as_view(), name='cms'),
    path('products/', cms_views.ProductListView.as_view(), name='products'),
    path('products/create/', cms_views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', cms_views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', cms_views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/price-list/', cms_views.PriceCreateView.as_view(), name='price_upload'),
    path('categories/', cms_views.CategoryListView.as_view(), name='categories'),
    path('categories/create/', cms_views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', cms_views.CategoryUpdateView.as_view(), name='category_update'),
    path('brands/', cms_views.BrandListView.as_view(), name='brands'),
    path('brands/create/', cms_views.BrandCreateView.as_view(), name='brand_create'),
    path('brands/<int:pk>/', cms_views.BrandUpdateView.as_view(), name='brand_update'),
]

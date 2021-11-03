from django.urls import path
from cms import views as cms_views

app_name = 'cms'

urlpatterns = [
    path('', cms_views.NewOrderListView.as_view(), name='cms'),
    path('orders/new/', cms_views.NewOrderListView.as_view(), name='orders_new'),
    path('orders/processed/', cms_views.ProcessedOrderListView.as_view(), name='orders_processed'),
    path('orders/archive/', cms_views.ArchivedOrderListView.as_view(), name='orders_archived'),
    path('orders/<int:pk>', cms_views.OrderDetailView.as_view(), name='order'),
    path('orders/<int:pk>/process/', cms_views.process_order, name='process_order'),
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

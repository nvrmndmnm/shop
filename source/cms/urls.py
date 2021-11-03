from django.urls import path
from cms import views as cms_views

app_name = 'cms'

urlpatterns = [
    path('', cms_views.NewOrderListView.as_view(), name='cms'),
    path('orders/new/', cms_views.NewOrderListView.as_view(), name='orders_new'),
    path('orders/processed/', cms_views.ProcessedOrderListView.as_view(), name='orders_processed'),
    path('orders/archive/', cms_views.ArchivedOrderListView.as_view(), name='orders_archived'),
    path('orders/<int:pk>', cms_views.OrderDetailView.as_view(), name='order'),
    path('orders/<int:pk>/process/', cms_views.order_processed, name='order_processed'),
    path('orders/<int:pk>/delivered/', cms_views.order_delivered, name='order_delivered'),
    path('orders/<int:pk>/cancel/', cms_views.order_canceled, name='order_canceled'),
    path('orders/<int:pk>/return/', cms_views.order_returned, name='order_returned'),
    path('products/', cms_views.CMSProductSearchView.as_view(), name='products'),
    path('products/create/', cms_views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', cms_views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', cms_views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/price-list/', cms_views.PriceCreateView.as_view(), name='price_upload'),
    path('products/search/', cms_views.CMSProductSearchView.as_view(), name='search_product'),
    path('categories/', cms_views.CMSCategorySearchView.as_view(), name='categories'),
    path('categories/create/', cms_views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', cms_views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/search/', cms_views.CMSCategorySearchView.as_view(), name='search_category'),
    path('brands/', cms_views.CMSBrandSearchView.as_view(), name='brands'),
    path('brands/create/', cms_views.BrandCreateView.as_view(), name='brand_create'),
    path('brands/<int:pk>/', cms_views.BrandUpdateView.as_view(), name='brand_update'),
    path('brands/search/', cms_views.CMSBrandSearchView.as_view(), name='search_brand'),
]

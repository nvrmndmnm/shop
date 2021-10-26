from django.urls import path
from storefront import views as storefront_views

app_name = 'storefront'

urlpatterns = [
    path('', storefront_views.IndexView.as_view(), name='index'),
]

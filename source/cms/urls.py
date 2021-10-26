from django.urls import path
from cms import views as cms_views

app_name = 'cms'

urlpatterns = [
    path('', cms_views.IndexView.as_view(), name='index2'),
]

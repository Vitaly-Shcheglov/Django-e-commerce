from django.urls import path
from . import views
from .views import product_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add_product/', add_product, name='add_product'),
]

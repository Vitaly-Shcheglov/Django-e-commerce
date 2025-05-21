from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomeView, ContactView, ProductDetailView, AddProductView, ProductListView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

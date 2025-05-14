from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomeView, ContactView, ProductDetailView, AddProductView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

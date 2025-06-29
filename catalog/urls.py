from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    HomeView,
    ContactView,
    ProductDetailView,
    AddProductView,
    ProductListView,
    ProductUpdateView,
    ProductDeleteView,
    PublishProductView,
    UnpublishProductView,
    ProductsInCategoryView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add_product/", AddProductView.as_view(), name="add_product"),
    path("edit/<int:pk>/", ProductUpdateView.as_view(), name="product_edit"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/publish/<int:pk>/", PublishProductView.as_view(), name="publish_product"),
    path("products/unpublish/<int:pk>/", UnpublishProductView.as_view(), name="unpublish_product"),
    path("category/<int:pk>/products/", ProductsInCategoryView.as_view(), name="products_in_category"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

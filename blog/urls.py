from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('add/', BlogCreateView.as_view(), name='blog_add'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]

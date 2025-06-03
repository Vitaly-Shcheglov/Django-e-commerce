from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegisterView, login_view, profile_edit, profile_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile_view, name='profile'),
]

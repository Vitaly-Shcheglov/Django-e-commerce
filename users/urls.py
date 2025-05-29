from django.urls import path
from .views import register
from .views import profile_edit
from .views import login_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]

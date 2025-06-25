from django.urls import path
from .views import recipient_list, create_recipient

urlpatterns = [
    path('recipients/', recipient_list, name='recipient_list'),
    path('recipients/create/', create_recipient, name='create_recipient'),
]

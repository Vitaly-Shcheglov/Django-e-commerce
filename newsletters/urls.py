from django.urls import path
from .views import recipient_list, create_recipient, statistics_view, create_message, create_mailing, MailingListView, message_list

urlpatterns = [
    path('recipients/', recipient_list, name='recipient_list'),
    path('recipients/create/', create_recipient, name='create_recipient'),
    path('statistics/', statistics_view, name='statistics'),
    path('messages/create/', create_message, name='create_message'),
    path('mailings/create/', create_mailing, name='create_mailing'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('messages/', message_list, name='message_list'),
]

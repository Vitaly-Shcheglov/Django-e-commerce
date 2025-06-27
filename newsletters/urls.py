from django.urls import path
from django.views.generic import DetailView
from .views import recipient_list, create_recipient, statistics_view, create_message, create_mailing, MailingListView, MailingEditView, MailingDeleteView, message_list, MessageDetailView, MessageCreateView, MessageEditView, MessageDeleteView, MailingDetailView, RecipientDetailView, RecipientEditView, RecipientDeleteView


urlpatterns = [
    path('messages/create/', MessageCreateView.as_view(), name='create_message'),
    path('messages/', message_list, name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/edit/<int:pk>/', MessageEditView.as_view(), name='edit_message'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('mailings/create/', create_mailing, name='create_mailing'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_list'),
    path('mailings/edit/<int:pk>/', MailingEditView.as_view(), name='edit_mailing'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('recipients/', recipient_list, name='recipient_list'),
    path('recipients/create/', create_recipient, name='create_recipient'),
    path('recipients/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/edit/<int:pk>/', RecipientEditView.as_view(), name='edit_recipient'),
    path('recipients/delete/<int:pk>/', RecipientDeleteView.as_view(), name='delete_recipient'),
    path('statistics/', statistics_view, name='statistics'),
]

from django import forms
from .models import Recipient, Message, Mailing, SendingAttempt

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipients', 'end_time']

class SendingAttemptForm(forms.ModelForm):
    class Meta:
        model = SendingAttempt
        fields = ['status', 'response', 'mailing']

from django import forms
from .models import Recipient, Message, Mailing, SendingAttempt


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]


class MailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = self.fields['message'].queryset.filter(owner=user)
        self.fields['recipients'].queryset = self.fields['recipients'].queryset.filter(owner=user)


    class Meta:
        model = Mailing
        fields = ["message", "recipients", "end_time"]


class SendingAttemptForm(forms.ModelForm):
    class Meta:
        model = SendingAttempt
        fields = ["status", "response", "mailing"]

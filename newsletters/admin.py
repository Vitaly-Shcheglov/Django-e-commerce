from django.contrib import admin
from .models import Recipient, Message, Mailing, SendingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "comment")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("message", "start_time", "end_time", "status")


@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    list_display = ("attempt_time", "status", "mailing")

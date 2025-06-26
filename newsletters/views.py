from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipient, Message, Mailing, SendingAttempt
from .forms import RecipientForm, MessageForm, MailingForm, SendingAttemptForm


def recipient_list(request):
    recipients = Recipient.objects.all()
    return render(request, 'newsletters/recipient_list.html', {'recipients': recipients})

def create_recipient(request):
    if request.method == 'POST':
        form = RecipientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipient_list')
    else:
        form = RecipientForm()
    return render(request, 'newsletters/create_recipient.html', {'form': form})


def statistics_view(request):
    successful_attempts = SendingAttempt.objects.filter(status='Успешно').count()
    unsuccessful_attempts = SendingAttempt.objects.filter(status='Не успешно').count()

    return render(request, 'newsletters/statistics.html', {
        'successful_attempts': successful_attempts,
        'unsuccessful_attempts': unsuccessful_attempts,
    })


def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'newsletters/create_message.html', {'form': form})

def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            form.save_m2m()
            return redirect('mailing_list')
    else:
        form = MailingForm()
    return render(request, 'newsletters/create_mailing.html', {'form': form})


class MailingListView(ListView):
    model = Mailing
    template_name = 'newsletters/mailing_list.html'
    context_object_name = 'mailings'

def message_list(request):
    messages = Message.objects.all()
    return render(request, 'newsletters/message_list.html', {'messages': messages})
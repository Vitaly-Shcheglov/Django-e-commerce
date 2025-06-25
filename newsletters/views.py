from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipient, Message, Mailing, SendingAttempt
from .forms import RecipientForm, MessageForm, MailingForm  # Не забудьте создать формы

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

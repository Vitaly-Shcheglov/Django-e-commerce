from django.views.generic import ListView, CreateView, DetailView, View, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipient, Message, Mailing, SendingAttempt
from .forms import RecipientForm, MessageForm, MailingForm, SendingAttemptForm
from django.urls import reverse_lazy


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

    def get_queryset(self):
        return Mailing.objects.all()


def message_list(request):
    messages = Message.objects.all()
    return render(request, 'newsletters/message_list.html', {'messages': messages})


class MessageDetailView(DetailView):
    model = Message
    template_name = 'newsletters/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(View):
    def get(self, request):
        form = MessageForm()
        return render(request, 'newsletters/create_message.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')
        return render(request, 'newsletters/create_message.html', {'form': form})


class MessageEditView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'newsletters/edit_message.html'
    context_object_name = 'message'

    def get_success_url(self):
        return reverse_lazy('message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'newsletters/message_confirm_delete.html'
    context_object_name = 'message'

    def get_success_url(self):
        return reverse_lazy('message_list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'newsletters/mailing_detail.html'
    context_object_name = 'mailing'


class MailingEditView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletters/edit_mailing.html'

    def get_success_url(self):
        return reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'newsletters/mailing_confirm_delete.html'
    context_object_name = 'mailing'

    def get_success_url(self):
        return reverse_lazy('mailing_list')


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'newsletters/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientEditView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletters/edit_recipient.html'

    def get_success_url(self):
        return reverse_lazy('recipient_list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'newsletters/recipient_confirm_delete.html'
    context_object_name = 'recipient'

    def get_success_url(self):
        return reverse_lazy('recipient_list')

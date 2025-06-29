from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, View, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipient, Message, Mailing, SendingAttempt, TechnicalTask
from .forms import RecipientForm, MessageForm, MailingForm, SendingAttemptForm
from django.urls import reverse_lazy, path
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


def statistics_view(request):
    if request.user.is_authenticated:
        mailings = Mailing.objects.filter(owner=request.user)

        statistics = []
        for mailing in mailings:
            successful_attempts = SendingAttempt.objects.filter(mailing=mailing, status='Успешно').count()
            unsuccessful_attempts = SendingAttempt.objects.filter(mailing=mailing, status='Не успешно').count()
            statistics.append({
                'mailing': mailing,
                'successful_attempts': successful_attempts,
                'unsuccessful_attempts': unsuccessful_attempts,
            })

        return render(request, 'newsletters/statistics.html', {'statistics': statistics})
    else:
        return redirect('login')

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'newsletters/create_message.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('message_list')

class MessageListView(ListView):
    model = Message
    template_name = 'newsletters/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetailView(DetailView):
    model = Message
    template_name = 'newsletters/message_detail.html'
    context_object_name = 'message'

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

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletters/create_mailing.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mailing_list')

class MailingListView(ListView):
    model = Mailing
    template_name = 'newsletters/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

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

class RecipientListView(ListView):
    model = Recipient
    template_name = 'newsletters/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)

class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'newsletters/create_recipient.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipient_list')

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

def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
    recipients = mailing.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                'from@example.com',  # Замените на фактический email отправителя
                [recipient.email],
                fail_silently=False,
            )
            SendingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status='Успешно',
                server_response='Письмо отправлено успешно'
            )
        except Exception as e:
            SendingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status='Не успешно',
                server_response=str(e)
            )
            messages.error(request, f"Ошибка при отправке сообщения на {recipient.email}: {str(e)}")

    messages.success(request, "Рассылка успешно отправлена!")
    return redirect('mailing_list')

def technical_task_list(request):
    tasks = TechnicalTask.objects.all()
    return render(request, 'newsletters/technical_task_list.html', {'tasks': tasks})

def technical_task_detail(request, pk):
    task = get_object_or_404(TechnicalTask, pk=pk)
    return render

from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipient, Message, Mailing, SendingAttempt
from .forms import RecipientForm, MessageForm, MailingForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required
def mailing_service_view(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status='Запущена').count()
    unique_recipients = Recipient.objects.values('email').distinct().count()

    is_mailing_manager = request.user.groups.filter(name='Mailing Manager').exists()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients,
        'is_mailing_manager': is_mailing_manager,
    }

    return render(request, 'newsletters/mailing_service.html', context)


@login_required
def statistics_view(request):
    mailings = Mailing.objects.filter(owner=request.user)

    statistics = []
    for mailing in mailings:
        successful_attempts = SendingAttempt.objects.filter(mailing=mailing, status="Успешно").count()
        unsuccessful_attempts = SendingAttempt.objects.filter(mailing=mailing, status="Не успешно").count()

        statistics.append(
            {
                "mailing": mailing,
                "successful_attempts": successful_attempts,
                "unsuccessful_attempts": unsuccessful_attempts,
            }
        )

    # context = {
    #     "statistics": statistics,
    # }

    return render(request, "newsletters/statistics.html", {"statistics": statistics})


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletters/create_message.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("message_list")


class MessageListView(ListView):
    model = Message
    template_name = "newsletters/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.groups.filter(name='Mailing Manager').exists():
            return Message.objects.all()
        else:
            return Message.objects.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageDetailView(DetailView):
    model = Message
    template_name = "newsletters/message_detail.html"
    context_object_name = "message"


class MessageEditView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletters/edit_message.html"
    context_object_name = "message"

    def get_success_url(self):
        return reverse_lazy("message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "newsletters/message_confirm_delete.html"
    context_object_name = "message"

    def get_success_url(self):
        return reverse_lazy("message_list")


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletters/create_mailing.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mailing_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "newsletters/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.groups.filter(name='Mailing Manager').exists():
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "newsletters/mailing_detail.html"
    context_object_name = "mailing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_mailing_manager'] = self.request.user.groups.filter(name='Mailing Manager').exists()
        return context


class MailingEditView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletters/edit_mailing.html"

    def get_success_url(self):
        return reverse_lazy("mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "newsletters/mailing_confirm_delete.html"
    context_object_name = "mailing"

    def get_success_url(self):
        return reverse_lazy("mailing_list")


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "newsletters/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.groups.filter(name='Mailing Manager').exists():
            return Recipient.objects.all()
        else:
            return Recipient.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_mailing_manager'] = self.request.user.groups.filter(name='Mailing Manager').exists()
        return context

class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "newsletters/create_recipient.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("recipient_list")


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "newsletters/recipient_detail.html"
    context_object_name = "recipient"


class RecipientEditView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "newsletters/edit_recipient.html"

    def get_success_url(self):
        return reverse_lazy("recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "newsletters/recipient_confirm_delete.html"
    context_object_name = "recipient"

    def get_success_url(self):
        return reverse_lazy("recipient_list")


def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    recipients = mailing.recipients.all()
    emails = [recipient.email for recipient in recipients]

    try:
        send_mail(
            subject=mailing.title,
            message=mailing.description,
            from_email='your_email@example.com', # Укажите свой email
            recipient_list=emails,
            fail_silently=False,
        )

        for recipient in recipients:
            SendingAttempt.objects.create(mailing=mailing, recipient=recipient, status='Успешно')
    except Exception as e:
        for recipient in recipients:
            SendingAttempt.objects.create(mailing=mailing, recipient=recipient, status='Не успешно')
        print(f"Ошибка при отправке: {e}")

    return redirect('mailing_list')  #


def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    mailing.status = "disabled"
    mailing.save()
    return redirect('mailing_list')


def task_detail(request):
    return render(request, "newsletters/task_detail.html", {})

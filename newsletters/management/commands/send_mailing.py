from django.core.management.base import BaseCommand
from newsletters.models import Mailing
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Отправка рассылки"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки для отправки")

    def handle(self, *args, **kwargs):
        mailing_id = kwargs["mailing_id"]
        mailing = Mailing.objects.get(id=mailing_id)

        recipients = mailing.recipients.all()
        for recipient in recipients:
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    "from@example.com",  # Замените на фактический email отправителя
                    [recipient.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f"Сообщение отправлено на {recipient.email}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при отправке на {recipient.email}: {str(e)}"))

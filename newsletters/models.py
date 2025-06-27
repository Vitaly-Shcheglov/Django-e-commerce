from django.db import models
from django.utils import timezone

class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        permissions = [
            ("can_view_recipient", "Can view recipient"),
            ("can_edit_recipient", "Can edit recipient"),
            ("can_delete_recipient", "Can delete recipient"),
        ]

    def __str__(self):
        return self.full_name

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("can_view_message", "Can view message"),
            ("can_edit_message", "Can edit message"),
            ("can_delete_message", "Can delete message"),
        ]

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_view_mailing", "Can view mailing"),
            ("can_edit_mailing", "Can edit mailing"),
            ("can_delete_mailing", "Can delete mailing"),
        ]

    def __str__(self):
        return f"Рассылка: {self.message.subject} - Статус: {self.get_status_display()}"

class SendingAttempt(models.Model):
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status} at {self.attempt_time}"
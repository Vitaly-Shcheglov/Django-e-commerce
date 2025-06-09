from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Выводит группы, в которых состоит указанный пользователь'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email пользователя')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        try:
            user = CustomUser.objects.get(email=email)
            user_groups = user.groups.all()

            if user_groups.exists():
                self.stdout.write(f'Группы для пользователя {email}:')
                for group in user_groups:
                    self.stdout.write(f' - {group.name}')
            else:
                self.stdout.write(f'У пользователя {email} нет групп.')
        except CustomUser.DoesNotExist:
            self.stdout.write(f'Пользователь с email {email} не найден.')

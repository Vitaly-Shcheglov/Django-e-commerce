from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Выводит код разрешений для указанного пользователя'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email пользователя')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        try:
            user = CustomUser.objects.get(email=email)
            user_permissions = user.user_permissions.all()

            if user_permissions.exists():

                self.stdout.write(f'Разрешения для пользователя {email}:')
                for perm in user_permissions:
                    self.stdout.write(f' - {perm.codename}')
            else:
                self.stdout.write(f'У пользователя {email} нет разрешений.')
        except CustomUser.DoesNotExist:
            self.stdout.write(f'Пользователь с email {email} не найден.')

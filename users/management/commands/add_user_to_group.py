from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Добавляет пользователя в группу и наделяет разрешениями'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email пользователя')
        parser.add_argument('group_name', type=str, help='Название группы')
        parser.add_argument('permissions', nargs='+', type=str, help='Список кодов разрешений')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        group_name = kwargs['group_name']
        permissions = kwargs['permissions']

        try:
            user = CustomUser.objects.get(email=email)

            group, created = Group.objects.get_or_create(name=group_name)

            user.groups.add(group)

            for perm in permissions:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Разрешение "{perm}" не найдено.'))

            self.stdout.write(
                self.style.SUCCESS(f'Пользователь {email} добавлен в группу "{group_name}" и наделен разрешениями.'))

        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Пользователь с email {email} не найден.'))

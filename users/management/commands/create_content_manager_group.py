from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создает группу Контент-менеджер и назначает права'

    def handle(self, *args, **kwargs):
        # Создание группы контент-менеджеров
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')

        # Получаем права
        manage_blog_permission = Permission.objects.get(codename='can_manage_blog')

        # Назначение прав группе
        content_manager_group.permissions.add(manage_blog_permission)

        self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" создана и права назначены.'))

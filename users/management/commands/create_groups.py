from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы и назначает права'

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        can_unpublish = Permission.objects.get(codename='can_unpublish_product')
        delete_permission = Permission.objects.get(codename='delete_product')

        moderator_group.permissions.add(can_unpublish, delete_permission)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана и права назначены.'))

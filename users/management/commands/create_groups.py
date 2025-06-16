from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Create groups with specific permissions'

    def handle(self, *args, **kwargs):
        content_manager_group, created = Group.objects.get_or_create(name='Content manager group')
        change_permission = Permission.objects.get(codename='can_change_blogpost')
        delete_permission = Permission.objects.get(codename='can_delete_blogpost')
        view_permission = Permission.objects.get(codename='can_view_blogpost')

        content_manager_group.permissions.add(change_permission, delete_permission, view_permission)
        user = CustomUser.objects.get(email=' example@forexample.com') # Замените на фактический email зарегистрированного пользователя
        user.groups.add(content_manager_group)

        product_moderator_group, created = Group.objects.get_or_create(name='Product moderator group')
        can_unpublish_permission = Permission.objects.get(codename='can_unpublish_product')
        can_delete_permission = Permission.objects.get(codename='can_delete_product')

        product_moderator_group.permissions.add(can_unpublish_permission, can_delete_permission)
        user = CustomUser.objects.get(email='yuristresurs@mail.ru')
        user.groups.add(product_moderator_group)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions.'))

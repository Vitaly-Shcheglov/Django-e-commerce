from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import CustomUser


class Command(BaseCommand):
    help = "Create groups with specific permissions"

    def handle(self, *args, **kwargs):
        content_manager_group, created = Group.objects.get_or_create(name="Content manager group")
        change_permission = Permission.objects.get(codename="can_change_blogpost")
        delete_permission = Permission.objects.get(codename="can_delete_blogpost")
        view_permission = Permission.objects.get(codename="can_view_blogpost")

        content_manager_group.permissions.add(change_permission, delete_permission, view_permission)

        user = CustomUser.objects.get(
            email="yuristresurs@mail.ru"
        )  # Замените на фактический email зарегистрированного пользователя
        user.groups.add(content_manager_group)

        product_moderator_group, created = Group.objects.get_or_create(name="Product moderator group")
        can_unpublish_permission = Permission.objects.get(codename="can_unpublish_product")
        can_delete_permission = Permission.objects.get(codename="can_delete_product")

        product_moderator_group.permissions.add(can_unpublish_permission, can_delete_permission)

        user.groups.add(product_moderator_group)

        mailing_manager_group, created = Group.objects.get_or_create(name="Mailing Manager")
        can_view_recipient = Permission.objects.get(codename="can_view_recipient")
        can_view_message = Permission.objects.get(codename="can_view_message")
        can_view_mailing = Permission.objects.get(codename="can_view_mailing")
        can_view_users = Permission.objects.get(codename="can_view_users")
        can_block_user = Permission.objects.get(codename="can_block_user")
        can_disable_mailing = Permission.objects.get(codename="can_disable_mailing")

        mailing_manager_group.permissions.add(
            can_view_recipient, can_view_message, can_view_mailing, can_view_users, can_block_user, can_disable_mailing
        )
        user.groups.add(mailing_manager_group)

        self.stdout.write(self.style.SUCCESS("Successfully created groups and assigned permissions."))

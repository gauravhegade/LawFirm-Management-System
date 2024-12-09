from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from lawyer_app.models import Client, Lawyer


class Command(BaseCommand):
    help = "Creates default user groups and assigns permissions"

    def handle(self, *args, **kwargs):
        # Define groups
        groups_permissions = {
            "Lawyer": ["view_case", "add_case", "change_case"],
            "Client": ["view_case"],
            "Admin": [
                "add_lawyer",
                "change_lawyer",
                "delete_lawyer",
                "add_client",
                "change_client",
                "delete_client",
            ],
        }

        # Create groups and assign permissions
        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Group "{group_name}" created successfully')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group "{group_name}" already exists')
                )

            # Assign permissions to group
            for perm in permissions:
                model_name = perm.split("_")[1]
                content_type = ContentType.objects.get(
                    model=model_name
                )  # Get model content type
                try:
                    permission = Permission.objects.get(
                        codename=perm, content_type=content_type
                    )
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Permission "{perm}" does not exist for model "{model_name}"'
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(f'Permissions assigned to "{group_name}" group')
            )

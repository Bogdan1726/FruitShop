from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser and user-joker'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            super_user = User.objects.create(
                username='Admin',
                is_superuser=True,
                is_staff=True
            )
            super_user.set_password('Zaqwerty123')
            self.stdout.write('Superuser successfully created')
        else:
            self.stdout.write('Superuser already been created before')

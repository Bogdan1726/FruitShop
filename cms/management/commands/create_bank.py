from django.core.management.base import BaseCommand
from cms.models import Bank


class Command(BaseCommand):
    help = 'Create bank'

    def handle(self, *args, **options):
        if not Bank.objects.all().exists():
            Bank.objects.create(
                balance=0
            )
            self.stdout.write('Bank has been successfully created')
        else:
            self.stdout.write('Bank have already been created before')

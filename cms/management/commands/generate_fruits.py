from django.core.management.base import BaseCommand
from cms.models import Fruit


class Command(BaseCommand):
    help = 'Generate test fruits'

    def handle(self, *args, **options):
        if not Fruit.objects.all().exists():
            Fruit.objects.bulk_create([
                Fruit(name='Ананасы', quantity=1000),
                Fruit(name='Яблоки', quantity=1000),
                Fruit(name='Бананы', quantity=1000),
                Fruit(name='Апельсины', quantity=1000),
                Fruit(name='Абрикосы', quantity=1000),
                Fruit(name='Киви', quantity=1000)
            ])
            self.stdout.write('Fruits has been successfully generated')
        else:
            self.stdout.write('Fruit have already been generated before')

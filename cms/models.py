from django.db import models
from django.utils.translation import gettext_lazy as _


class Fruit(models.Model):
    objects = None
    name = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Bank(models.Model):
    objects = None
    balance = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.balance}'


class Declaration(models.Model):
    date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='files')


class Logging(models.Model):
    class TypeOperation(models.TextChoices):
        BOUGHT = 'BOUGHT', _('Куплено')
        SOLD = 'SOLD', _('Продано')

    class TypeLogging(models.TextChoices):
        ERROR = 'ERROR', _('ERROR')
        SUCCESS = 'SUCCESS', _('SUCCESS')

    type_operation = models.CharField(max_length=6, choices=TypeOperation.choices, null=True, blank=True)
    type_logging = models.CharField(max_length=7, choices=TypeLogging.choices, default=TypeLogging.SUCCESS)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    usd = models.PositiveIntegerField()
    provider = models.BooleanField(default=True)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE, related_name='logging')

    def __str__(self):
        return self.type_logging

    class Meta:
        ordering = ('-date',)

    @property
    def get_operation(self):
        format_date = self.date.strftime("%d.%m.%Y %H:%M")
        if self.type_operation == 'BOUGHT':
            return f'{format_date} - куплены  {self.fruit.name} в количестве {self.amount} шт. за {self.usd} usd'
        elif self.type_operation == 'SOLD':
            return f'{format_date} - проданы {self.fruit.name} в количестве {self.amount} шт.  за {self.usd} usd'

    @property
    def get_log(self):
        format_date = self.date.strftime("%d.%m.%Y %H:%M")
        if self.type_logging == 'SUCCESS':
            if self.provider:
                return f'{format_date} - SUCCESS: Поставщик привёз товар {self.fruit.name} ' \
                       f'в количестве {self.amount} шт. Со счёта списано {self.usd} USD, покупка завершена.'
            else:
                return f'{format_date} - SUCCESS: Продажа товара ' \
                       f'{self.fruit.name} в количестве {self.amount} шт. На счёт зачислено {self.usd} USD, ' \
                       f'продажа завершена.'
        else:
            if self.provider:
                return f'{format_date} - ERROR: Поставщик привёз товар {self.fruit.name} ' \
                       f'в количестве {self.amount} шт. Недостаточно средств на счету, закупка отменена.'
            else:
                return f'{format_date} - ERROR: Невозможно продать товар ' \
                       f'{self.fruit.name} в количестве {self.amount} шт. Недостаточно на складе, продажа отменена.'

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

    @property
    def get_success_log(self):
        """
        Get last success log
        """
        return self.logging.filter(type_logging='SUCCESS').last()


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
        ordering = ('id',)

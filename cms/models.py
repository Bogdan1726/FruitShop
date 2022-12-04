from django.db import models


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

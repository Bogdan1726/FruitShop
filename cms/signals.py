import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save
from cms.models import Bank, Declaration

channel_layer = get_channel_layer()


@receiver(post_save, sender=Bank)
def post_save_bank(**kwargs):
    instance = kwargs.get('instance')
    async_to_sync(channel_layer.group_send)(
        'bank_warehouse',
        {
            'type': 'update_bank',
            'balance': instance.balance
        }
    )


@receiver(post_save, sender=Declaration)
def post_save_declaration(**kwargs):
    count = Declaration.objects.filter(date=datetime.datetime.now()).count()
    async_to_sync(channel_layer.group_send)(
        'bank_warehouse',
        {
            'type': 'new_declaration',
            'amount': count
        }
    )

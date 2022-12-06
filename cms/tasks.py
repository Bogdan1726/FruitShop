import datetime
from random import randint
from asgiref.sync import async_to_sync
from celery import shared_task, signals
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from cms.models import Fruit, Bank
from config.settings import API_JESTER
from users.models import Chat
from channels.layers import get_channel_layer
import requests
from django.core.cache import cache

logger = get_task_logger(__name__)

channel_layer = get_channel_layer()

User = get_user_model()


@signals.worker_ready.connect()
def at_start(sender, **kwargs):
    cache.clear()
    task_jester.delay()


@shared_task(bind=True)
def task_jester(self):
    """
    A task that, via websockets, adds jokes with an interval equal to the length of the previous joke
    """
    logger.info('Task jester send')
    response = requests.get(url=API_JESTER)
    try:
        if response.status_code == 200:
            response_data = response.json()
            text = response_data.get('joke')
            Chat.objects.create(message=str(text))
            async_to_sync(channel_layer.group_send)(
                'chat_warehouse',
                {
                    'type': 'chat_message',
                    'message': str(text),
                    'user': 'Шутник',
                    'time': str(datetime.datetime.now().time())
                }
            )
            logger.info('Task jester successful')
            task_jester.apply_async(countdown=int(len(text)))
        else:
            raise Exception()
    except Exception as exp:
        logger.error('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=exp, countdown=5)


@shared_task(bind=True)
def task_check_warehouse(self, user):
    """
    The task is doing accounting. By means of websocket draws progress on the front
    """
    try:
        counter = 0
        res = AsyncResult(self.request.id)
        for i in range(1, 26):
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            counter += 100000 ** 100000
            self.update_state(state='PROGRESS',
                              meta={'current': i * 4, 'total': 100})
            async_to_sync(channel_layer.group_send)(
                f'audit_{user}',
                {
                    'type': 'update_progress',
                    'progress': res.result
                }
            )
        cache.delete(user)
    except Exception as exc:
        logger.error(exc)
        cache.delete(user)


@shared_task(bind=True)
def task_buy_fruits(self, value, count):
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    fruit = Fruit.objects.get(pk=value)
    bank = Bank.objects.all().first()
    price = randint(1, 4)
    summa = (int(price) * int(count))
    if summa > int(bank.balance):
        log = f'{current_date.strftime("%d.%m.%Y")} {current_time.strftime("%H:%M:%S")} - ERROR: Недостаточно ' \
              f'средств на счету для покупкм {count} {fruit.name}, покупки отменена.'
    else:
        fruit.quantity += int(count)
        fruit.save()
        bank.balance -= summa
        bank.save()
        log = f'{current_date.strftime("%d.%m.%Y")} {current_time.strftime("%H:%M:%S")} - SUCCESS: Покупка ' \
              f'{count} {fruit.name}. Со счёта списано {summa} USD, покупка завершена.'

    async_to_sync(channel_layer.group_send)(
        'fruit_warehouse',
        {
            'type': 'update_warehouse',
            'log': log,
            'fruit_id': fruit.id,
            'fruit_count': fruit.quantity,
        }
    )
    async_to_sync(channel_layer.group_send)(
        'bank_warehouse',
        {
            'type': 'update_bank',
            'balance': bank.balance,
        }
    )


@shared_task(bind=True)
def task_sell_fruits(self, value, count):
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()
    fruit = Fruit.objects.get(pk=value)
    bank = Bank.objects.all().first()
    price = randint(1, 4)
    summa = (int(price) * int(count))
    if int(count) > int(fruit.quantity):
        log = f'{current_date.strftime("%d.%m.%Y")} {current_time.strftime("%H:%M:%S")} - ERROR: Недостаточное ' \
              f'количество {fruit.name} на складе, продажа отменена.'
    else:
        fruit.quantity -= int(count)
        fruit.save()
        bank.balance += summa
        bank.save()
        log = f'{current_date.strftime("%d.%m.%Y")} {current_time.strftime("%H:%M:%S")} - SUCCESS: Продажа ' \
              f'{count} {fruit.name}. На счёт зачислено {summa} USD, продажа завершена.'

    async_to_sync(channel_layer.group_send)(
        'fruit_warehouse',
        {
            'type': 'update_warehouse',
            'log': log,
            'fruit_id': fruit.id,
            'fruit_count': fruit.quantity,
        }
    )
    async_to_sync(channel_layer.group_send)(
        'bank_warehouse',
        {
            'type': 'update_bank',
            'balance': bank.balance,
        }
    )

import datetime
from random import randint
from asgiref.sync import async_to_sync
from celery import shared_task, signals
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from cms.models import Fruit, Bank, Logging, Declaration
from config.celery import app
from config.settings import API_JESTER
from users.models import Chat
from channels.layers import get_channel_layer
import requests
from django.core.cache import cache
import translators as ts  # noqa
from django_celery_beat.models import PeriodicTask, IntervalSchedule, PeriodicTasks

logger = get_task_logger(__name__)

channel_layer = get_channel_layer()

User = get_user_model()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # cache.clear()
    sender.add_periodic_task(10, test.s(), name='test_test')


@app.task
def test():
    print('Test')
    return 'Test'


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
            translated_joke = ts.bing(text, from_language='en', to_language='ru')
            Chat.objects.create(message=str(translated_joke))
            async_to_sync(channel_layer.group_send)(
                'chat_warehouse',
                {
                    'type': 'chat_message',
                    'message': str(translated_joke),
                    'user': 'Шутник',
                    'time': str(datetime.datetime.now().time())
                }
            )
            logger.info('Task jester successful')
            task_jester.apply_async(countdown=int(len(translated_joke)))
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
        res = AsyncResult(self.request.id)
        for i in range(1, 26):
            counter = [100000 ** 100000 for _ in range(10)]  # noqa
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
def task_update_declaration(self):
    """
    The task for declarations check quantity
    """
    count = Declaration.objects.filter(date=datetime.datetime.now()).count()
    async_to_sync(channel_layer.group_send)(
        'bank_warehouse',
        {
            'type': 'new_declaration',
            'amount': count
        }
    )


@shared_task(bind=True)
def task_clear_old_log(self):
    """
    The task for old log clear
    """
    before_yesterday = datetime.datetime.now() - datetime.timedelta(2)
    Logging.objects.filter(date__lt=before_yesterday).delete()


@shared_task(bind=True)
def task_buy_fruits(self, value, count=randint(1, 20)):
    date = datetime.datetime.now()
    fruit = Fruit.objects.get(pk=value)
    bank = Bank.objects.all().first()
    price = randint(1, 4)
    summa = (int(price) * int(count))
    if summa > int(bank.balance):
        operation = None
        Logging.objects.create(type_logging='ERROR', amount=int(count), usd=int(summa), fruit_id=fruit.id)
        log = f'{date.strftime("%d.%m.%Y %H:%M")} - ERROR: Поставщик привёз товар {fruit.name} ' \
              f'в количестве {count} шт. Недостаточно средств на счету, закупка отменена.'
    else:
        fruit.quantity += int(count)
        fruit.save()
        bank.balance -= summa
        bank.save()
        Logging.objects.create(
            type_logging='SUCCESS', type_operation='BOUGHT', amount=int(count), usd=int(summa), fruit_id=fruit.id)
        log = f'{date.strftime("%d.%m.%Y %H:%M")} - SUCCESS: Поставщик привёз товар {fruit.name} ' \
              f'в количестве {count} шт. Со счёта списано {summa} USD, покупка завершена.'
        operation = f'{date.strftime("%d.%m.%Y %H:%M")} - куплены  {fruit.name} в количестве {count} шт. за {summa} usd'

    async_to_sync(channel_layer.group_send)(
        'fruit_warehouse',
        {
            'type': 'update_warehouse',
            'log': log,
            'operation': operation,
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
def task_sell_fruits(self, value, count=randint(5, 20)):
    date = datetime.datetime.now()
    fruit = Fruit.objects.get(pk=value)
    bank = Bank.objects.all().first()
    price = randint(1, 2)
    summa = (int(price) * int(count))
    if int(count) > int(fruit.quantity):
        operation = None
        Logging.objects.create(
            type_logging='ERROR', provider=False, amount=int(count), usd=int(summa), fruit_id=fruit.id)
        log = f'{date.strftime("%d.%m.%Y %H:%M")} - ERROR: Невозможно продать товар ' \
              f'{fruit.name} в количестве {count} шт. Недостаточно на складе, продажа отменена.'
    else:
        fruit.quantity -= int(count)
        fruit.save()
        bank.balance += summa
        bank.save()
        Logging.objects.create(
            type_logging='SUCCESS', type_operation='SOLD', provider=False, amount=int(count), usd=int(summa),
            fruit_id=fruit.id
        )
        log = f'{date.strftime("%d.%m.%Y %H:%M")} - SUCCESS: Продажа товара ' \
              f'{fruit.name} в количестве {count} шт. На счёт зачислено {summa} USD, продажа завершена.'
        operation = f'{date.strftime("%d.%m.%Y %H:%M")} - проданы  {fruit.name} в количестве {count} шт. за {summa} usd'

    async_to_sync(channel_layer.group_send)(
        'fruit_warehouse',
        {
            'type': 'update_warehouse',
            'log': log,
            'operation': operation,
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

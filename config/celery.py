from celery import Celery
from celery.schedules import crontab
import os
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config', broker='redis://127.0.0.1:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.task_queues = (
#     Queue('Queue1',    routing_key='Queue1'),
#     Queue('Queue2', routing_key='Queue2'),
# )
# region schedules


# app.conf.beat_schedule = {
#     'check-count-declaration-every-00:00': {
#         'task': 'cms.tasks.task_update_declaration',
#         'schedule': crontab(minute=0, hour=0)
#     },
#
#     'clear-logging-every-00:00': {
#         'task': 'cms.tasks.task_clear_old_log',
#         'schedule': crontab(minute=1, hour=0)
#     },
#     'buy-fruit-pineapples': {
#         'task': 'cms.tasks.task_buy_fruits',
#         'schedule': 10.0,
#         'args': (1,)
#     },
#     'buy-fruit-apple': {
#         'task': 'cms.tasks.task_buy_fruits',
#         'schedule': 8.0,
#         'args': (2,)
#     },
#     'buy-fruit-banana': {
#         'task': 'cms.tasks.task_buy_fruits',
#         'schedule': 12.0,
#         'args': (3,)
#     },
#     'buy-fruit-orange': {
#         'task': 'cms.tasks.task_buy_fruits',
#         'schedule': 15.0,
#         'args': (4,)
#     },
#     'buy-fruit-apricot': {
#         'task': 'cms.tasks.task_buy_fruits',
#         'schedule': 16.0,
#         'args': (5,)
#     },
#     'buy-fruit-kiwi': {
#         'task': 'cms.tasks.task_buy_fruits',
#         'schedule': 17.0,
#         'args': (6,)
#     },
#     'sell-fruit-pineapples': {
#         'task': 'cms.tasks.task_sell_fruits',
#         'schedule': 19.0,
#         'args': (1,)
#     },
#     'sell-fruit-apple': {
#         'task': 'cms.tasks.task_sell_fruits',
#         'schedule': 18.0,
#         'args': (2,)
#     },
#     'sell-fruit-banana': {
#         'task': 'cms.tasks.task_sell_fruits',
#         'schedule': 17.0,
#         'args': (3,)
#     },
#     'sell-fruit-orange': {
#         'task': 'cms.tasks.task_sell_fruits',
#         'schedule': 15.0,
#         'args': (4,)
#     },
#     'sell-fruit-apricot': {
#         'task': 'cms.tasks.task_sell_fruits',
#         'schedule': 16.0,
#         'args': (5,)
#     },
#     'sell-fruit-kiwi': {
#         'task': 'cms.tasks.task_sell_fruits',
#         'schedule': 17.0,
#         'args': (6,)
#     }
# }

# endregion schedules

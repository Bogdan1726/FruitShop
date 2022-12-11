import random

from celery import Celery
from celery.schedules import crontab
import os

from cms.utils import list_fruits

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# region schedules


app.conf.beat_schedule = {
    'buy-fruit-pineapples': {
        'task': 'cms.tasks.task_buy_fruits',
        'schedule': 10.0,
        'args': (1,)
    },
    'buy-fruit-apple': {
        'task': 'cms.tasks.task_buy_fruits',
        'schedule': 8.0,
        'args': (2,)
    },
    'buy-fruit-banana': {
        'task': 'cms.tasks.task_buy_fruits',
        'schedule': 12.0,
        'args': (3,)
    },
    'buy-fruit-orange': {
        'task': 'cms.tasks.task_buy_fruits',
        'schedule': 15.0,
        'args': (4,)
    },
    'buy-fruit-apricot': {
        'task': 'cms.tasks.task_buy_fruits',
        'schedule': 16.0,
        'args': (5,)
    },
    'buy-fruit-kiwi': {
        'task': 'cms.tasks.task_buy_fruits',
        'schedule': 17.0,
        'args': (6,)
    }
}

# endregion schedules

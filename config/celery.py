from celery.schedules import crontab
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# region schedules

# app.conf.beat_schedule = {
#     'send_task_jester': {
#         'task': 'cms.tasks.task_jester',
#         'schedule': 10.0,
#     }
# }
#
#
# app.conf.timezone = 'Europe/Kiev'



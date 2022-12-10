import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from cms.tasks import task_jester
from config.celery import app
from users.models import Chat
from django_celery_beat.models import PeriodicTask, IntervalSchedule

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']

        user = User.objects.get(id=user_id)
        Chat.objects.create(
            message=message,
            user=user
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,
                'time': str(datetime.datetime.now().time())
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']
        time = event['time']

        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'time': time
        }))


class BankConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'bank_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def update_bank(self, event):
        balance = event['balance']
        self.send(text_data=json.dumps({
            'balance': balance,
        }))


class AuditConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'audit_{user.id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def update_progress(self, event):
        progress = event['progress']
        self.send(text_data=json.dumps({
            'progress': progress,
        }))


class WarehouseConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'fruit_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def update_warehouse(self, event):
        log = event['log']
        operation = event['operation']
        fruit_id = event['fruit_id']
        fruit_count = event['fruit_count']
        self.send(text_data=json.dumps({
            'log': log,
            'operation': operation,
            'fruit_id': fruit_id,
            'fruit_count': fruit_count
        }))

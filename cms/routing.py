from django.urls import re_path
from cms.consumers import ChatConsumer, BankConsumer, AuditConsumer, WarehouseConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/bank/(?P<room_name>\w+)/$', BankConsumer.as_asgi()),
    re_path(r'ws/audit/(?P<room_name>\w+)/$', AuditConsumer.as_asgi()),
    re_path(r'ws/fruit/(?P<room_name>\w+)/$', WarehouseConsumer.as_asgi())
]

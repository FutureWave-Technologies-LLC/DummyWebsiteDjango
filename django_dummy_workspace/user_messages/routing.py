# '''
# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]
# '''

from django.urls import re_path
from user_messages.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sender_id>\d+)/(?P<receiver_id>\d+)/$', ChatConsumer.as_asgi()),
]

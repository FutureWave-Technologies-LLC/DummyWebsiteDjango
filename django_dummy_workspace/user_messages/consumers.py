import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import user_messages
from users.models import users
'''
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
'''
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_group_name = f'chat_{min(self.sender_id, self.receiver_id)}_{max(self.sender_id, self.receiver_id)}'

        # Join the chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket connection attempt: {self.scope['url_route']['kwargs']}")
        await self.accept()

    async def disconnect(self, close_code):
        logger.info("WebSocket disconnected.")
        # Leave the chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        message_text = data['message_text']

        # Save the message to the database
        sender = users.objects.get(user_id=sender_id)
        user_messages.objects.create(
            sender=sender,
            receiver_id=receiver_id,
            message_text=message_text
        )

        # Send the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message_text': message_text
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'message_text': event['message_text']
        }))

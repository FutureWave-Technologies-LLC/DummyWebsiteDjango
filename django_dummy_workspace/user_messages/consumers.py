import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import user_messages
from users.models import users

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"WebSocket connection: {self.scope['path']}")
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
        print(sender_id, receiver_id, message_text)

        if not sender_id or not receiver_id or not message_text:
            await self.send(text_data=json.dumps({
                'error': 'Missing required fields: sender_id, receiver_id, or message_text'
            }))
            return

        # Save the message to the database
        try:
            sender = await database_sync_to_async(users.objects.get)(user_id=sender_id)
            receiver = await database_sync_to_async(users.objects.get)(user_id=receiver_id)

            # Create and save the message
            await database_sync_to_async(user_messages.objects.create)(
                sender=sender,
                receiver_id=receiver_id,
                message_text=message_text
            )

        except users.DoesNotExist:
            await self.send(text_data=json.dumps({
                'error': 'Sender or receiver user not found.'
            }))
            return

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

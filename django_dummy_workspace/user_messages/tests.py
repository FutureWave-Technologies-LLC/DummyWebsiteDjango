from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *

class SendMessageViewTests(APITestCase):
    def setUp(self):
        self.sender = users.objects.create(user_id=1, username="sender")
        self.receiver = users.objects.create(user_id=2, username="receiver")
        self.url = reverse('messages')  # replace with your actual URL name for this endpoint

    def test_send_message(self):
        data = {
            'sender_id': self.sender.user_id,
            'receiver_id': self.receiver.user_id,
            'message_text': 'Hello, this is a test message.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Response'], "Message sent")

class GetMessagesViewTests(APITestCase):
    def setUp(self):
        self.sender = users.objects.create(user_id=1, username="sender")
        self.receiver = users.objects.create(user_id=2, username="receiver")
        self.message1 = user_messages.objects.create(
            sender=self.sender, receiver_id=self.receiver.user_id, message_text="Hello from sender."
        )
        self.message2 = user_messages.objects.create(
            sender=self.receiver, receiver_id=self.sender.user_id, message_text="Hello from receiver."
        )
        self.url = reverse('messages')  # replace with your actual URL name for this endpoint

    def test_get_messages(self):
        response = self.client.get(self.url, {'sender_id': self.sender.user_id, 'receiver_id': self.receiver.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting two messages between sender and receiver
        self.assertEqual(response.data[0]['message_text'], self.message1.message_text)
        self.assertEqual(response.data[1]['message_text'], self.message2.message_text)

class GetMessagesNoMessagesViewTests(APITestCase):
    def setUp(self):
        self.sender = users.objects.create(user_id=1, username="sender")
        self.receiver = users.objects.create(user_id=2, username="receiver")
        self.url = reverse('messages')  # replace with your actual URL name for this endpoint

    def test_get_no_messages(self):
        response = self.client.get(self.url, {'sender_id': self.sender.user_id, 'receiver_id': self.receiver.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No messages should be found

class GetMessagesInvalidUserIDViewTests(APITestCase):
    def setUp(self):
        self.sender = users.objects.create(user_id=1, username="sender")
        self.receiver = users.objects.create(user_id=2, username="receiver")
        self.url = reverse('messages')  # replace with your actual URL name for this endpoint

    def test_get_invalid_user_id(self):
        response = self.client.get(self.url, {'sender_id': 999, 'receiver_id': 2})  # Invalid sender ID
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No messages should be found

        response = self.client.get(self.url, {'sender_id': 1, 'receiver_id': 999})  # Invalid receiver ID
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No messages should be found

class SendMessageSameSenderReceiverViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="user")
        self.url = reverse('messages')  # replace with your actual URL name for this endpoint

    def test_send_message_same_sender_receiver(self):
        data = {
            'sender_id': self.user.user_id,
            'receiver_id': self.user.user_id,
            'message_text': 'Test message to self'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Assuming you allow sending messages to oneself
        self.assertEqual(response.data['Response'], "Message sent")

class MessageSerializationViewTests(APITestCase):
    def setUp(self):
        self.sender = users.objects.create(user_id=1, username="sender")
        self.receiver = users.objects.create(user_id=2, username="receiver")
        self.message = user_messages.objects.create(
            sender=self.sender, receiver_id=self.receiver.user_id, message_text="Test message"
        )
        self.url = reverse('messages')  # replace with your actual URL name for this endpoint

    def test_message_serialization(self):
        response = self.client.get(self.url, {'sender_id': self.sender.user_id, 'receiver_id': self.receiver.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response contains the serialized message
        self.assertEqual(response.data[0]['message_text'], self.message.message_text)
        self.assertEqual(response.data[0]['sender'], self.sender.user_id)

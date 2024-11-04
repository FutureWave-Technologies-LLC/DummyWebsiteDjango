# serializers.py
from rest_framework import serializers
from .models import user_messages

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_messages
        fields = ('message_id', 'reciever_id', 'text', 'user_id')

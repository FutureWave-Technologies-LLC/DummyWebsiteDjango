# serializers.py
from rest_framework import serializers
from .models import messages

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = messages
        fields = ['message_id', 'user', 'reciever_id', 'text']

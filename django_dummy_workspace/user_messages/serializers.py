from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source='sender.id')  
    receiver_id = serializers.IntegerField(source='receiver.id')  

    class Meta:
        model = Message
        fields = ['sender_id', 'receiver_id', 'message_text']

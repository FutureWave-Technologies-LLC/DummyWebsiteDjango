from rest_framework import serializers
from .models import user_messages

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_messages
        fields = ('message_id', 'sender', 'receiver_id', 'message_text')
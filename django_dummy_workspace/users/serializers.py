from rest_framework import serializers
from .models import users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ('username', 'password', 'first_name', 'last_name')

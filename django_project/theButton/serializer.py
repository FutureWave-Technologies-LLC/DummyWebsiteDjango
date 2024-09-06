from rest_framework import serializers 
from .models import dummydata

class dummydataserializer(serializers.ModelSerializer):
    class Meta:
        model = dummydata
        fields = ['id', 'username', 'password']

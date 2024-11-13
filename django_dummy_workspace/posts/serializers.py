from rest_framework import serializers
from .models import *

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts
        fields = ('title', 'description', 'media')

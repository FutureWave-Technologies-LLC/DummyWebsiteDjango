from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from users.models import users
from profiles.models import follow
from .models import user_messages
from .serializers import MessageSerializer
from random import randrange
from django.db.models import Q

#GET MESSAGES BETWEEN TWO USERS
@api_view(['GET'])
def messages(request):
    if request.method == 'GET':
        sender_id = request.GET.get("sender_id")
        receiver_id = request.GET.get("receiver_id")
        
        # Fetch messages between the two users
        queryset = user_messages.objects.filter(
            Q(sender=sender_id, receiver_id=receiver_id) |
            Q(sender=receiver_id, receiver_id=sender_id)
        ).order_by('creation_date')
        #print(queryset)
        serializer = MessageSerializer(queryset, many=True)
        data = serializer.data
        for message in data:
            message['sender_id'] = int(message['sender'])
        
        return Response(data)

#GET USERS THAT CAN BE MESSAGED
@api_view(['GET'])
def get_messageable_users(request):
    user_id = request.GET.get("user_id")

    messageable_users = []
    for user in users.objects.all():
        if (follow.objects.filter(followee_id=user_id, follower_id=user.user_id).first() 
        and follow.objects.filter(followee_id=user.user_id, follower_id=user_id).first()):
            messageable_users.append({"username": user.username, 
                                    "user_id": user.user_id,
                                    "profile_image": user.profile_image})

    return Response(messageable_users)
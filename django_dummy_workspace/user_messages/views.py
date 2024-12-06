
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
# from django.contrib import messages
from users.models import users
from profiles.models import follow
from .serializers import MessageSerializer
from random import randrange
'''
#USER MESSAGES
@api_view(['GET','POST'])
def messages(request):
    #GET MESSAGES BETWEEN TWO USERS BASED ON IDS
    if request.method == 'GET':
        req_sender_id = request.GET.get("sender_id")
        req_receiver_id = request.GET.get("receiver_id")

        queryset = user_messages.objects.filter(sender=req_sender_id, receiver_id=req_receiver_id) | user_messages.objects.filter(sender=req_receiver_id, receiver_id=req_sender_id)
        serializer = MessageSerializer(queryset.order_by("creation_date"), many=True)
        return Response(serializer.data)
    #CREATE A MESSAGE
    elif request.method == 'POST':
        sender = users.objects.filter(user_id=request.data.get("sender_id")).first()
        new_message_info = user_messages(sender=sender,
                                         receiver_id=request.data.get("receiver_id"),
                                         message_text=request.data.get("message_text"))
        new_message_info.save()
        return Response({"Response": "Message sent"}, status=status.HTTP_201_CREATED)
        # serializer = MessageSerializer(data=request.data)

        # if serializer.is_valid():
        #     user = users.objects.filter(user_id = request.GET.get("user_id")).first()
        #     serializer.data["user_model_id"] = user
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user_messages
from .serializers import MessageSerializer
from users.models import users
from django.db.models import Q

@api_view(['GET', 'POST'])
def messages(request):
    if request.method == 'GET':
        sender_id = request.GET.get("sender_id")
        receiver_id = request.GET.get("receiver_id")
        
        # Fetch messages between the two users
        queryset = user_messages.objects.filter(
            Q(sender=sender_id, receiver_id=receiver_id) |
            Q(sender=receiver_id, receiver_id=sender_id)
        ).order_by('creation_date')
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        sender = users.objects.filter(user_id=request.data.get("sender_id")).first()
        new_message = user_messages(
            sender=sender,
            receiver_id=request.data.get("receiver_id"),
            message_text=request.data.get("message_text")
        )
        new_message.save()
        return Response({"Response": "Message sent"}, status=201)

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
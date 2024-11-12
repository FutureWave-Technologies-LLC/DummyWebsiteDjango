from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
# from django.contrib import messages
from users.models import users
from .serializers import MessageSerializer
from random import randrange

#USER MESSAGES
@api_view(['GET','POST'])
def messages(request):
    #GET MESSAGES BETWEEN TWO USERS BASED ON IDS
    if request.method == 'GET':
        req_sender_id = request.GET.get("sender_id")
        req_receiver_id = request.GET.get("receiver_id")

        queryset = user_messages.objects.filter(sender=req_sender_id, receiver_id=req_receiver_id) | user_messages.objects.filter(sender=req_receiver_id, receiver_id=req_sender_id).order_by("creation_date")
        serializer = MessageSerializer(queryset, many=True)
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

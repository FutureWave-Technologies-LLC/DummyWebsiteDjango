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
    #GET MESSAGES FOR TWO USERS BASED ON ID
    if request.method == 'GET':
        user_id = request.GET.get("user_id")
        reciever_id = request.GET.get("reciever_id")

        queryset = user_messages.objects.filter(user_id=user_id, reciever_id=reciever_id) | user_messages.objects.filter(user_id=reciever_id, reciever_id=user_id)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)
    #CREATE A MESSAGE
    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save(commit=False)
            user = users.objects.filter(user_id=request.data.user_id).first()
            instance.user_model = user.user_id
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

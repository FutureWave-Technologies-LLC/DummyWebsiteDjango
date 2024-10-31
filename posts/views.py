from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from random import randrange

# Create your views here.

#CREATES A POST
@api_view(['POST'])
def recieving_posts(request):
    data = request.data
    
    my_post_id = posts.objects.all().count()+1
    user = users.objects.filter(username=data.get('username')).first()

    my_post_info = posts(post_id = my_post_id, media = 'media', 
                         text = data.get('postText'), user_id = user.user_id, 
                         title = data.get('title'), 
                         username = user.username)
    my_post_info.save()
    json_data = {"Response": "Post was created", "error": False}
    return JsonResponse(json_data, safe=False)

#GET ALL POSTS DATA
@api_view(['GET'])
def get_posts(request):
    data = posts.objects.all().values()
    return Response(list(data))

#GET ALL DATA FOR A POST BASED ON ID
@api_view(['GET'])
def get_post(request):
    post = posts.objects.filter(post_id=request.GET.get('post_id')).first()  # Assuming posts have a 'username' field
    
    if post:
        json_data = {"post_id": post.post_id, 
                     "title": post.title, 
                     "text": post.text,
                     "username":post.username,
                     "user_id": post.user_id,
                     "media": post.media}
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "Post with this ID cannot be found", "error": True}
        return JsonResponse(json_data, safe=False)

#GET REPLIES
@api_view(['GET'])
def get_replies(request):
    data = replies.objects.all().values()
    return Response(list(data))

#GET COMMENTS
@api_view(['GET'])
def get_comments(request):
    data = comments.objects.all().values()
    return Response(list(data))

#GET LIKES
@api_view(['GET'])
def get_likes(request):
    data = likes.objects.all().values()
    return Response(list(data))

#UPDATE LIKES
@api_view(['POST'])
def update_likes(request):
    my_user = likes.objects.filter(email = "email@gmial.com").first()
    my_user.like_count += 1 #update like count for this user to be like_count + 1
    my_user.save()
    json_data = serializers.serialize('json', [my_user])
    # Return the JSON response
    return JsonResponse(json_data, safe=False)
    #from the previous user check the likes_count
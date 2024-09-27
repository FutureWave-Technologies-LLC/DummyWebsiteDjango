from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers


@api_view(['GET'])
def get_messages(request):
    data = messages.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_replies(request):
    data = replies.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_comments(request):
    data = comments.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_posts(request):
    data = posts.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def get_personal_pages(request):
    data = personal_pages.objects.all().values()
    return Response(list(data))

@api_view(['GET', 'POST'])
def get_users(request):
    if request.method == 'POST':
        data = request.data

        my_user_count = users.objects.all().count()
        
        # my_user = users.objects.create(user_id = '10').last()
        my_user_info = users(user_id = my_user_count, username = data.get('username'), 
                             password = data.get('password'), status = True, 
                             first_name = data.get('first_name'), last_name = data.get('last_name'))
        my_user_info.save()
        json_data = serializers.serialize('json', [my_user_info])

        # Return the JSON response
        return JsonResponse(json_data, safe=False)
        #from the previous user check the likes_count
    elif request.method == 'GET':
        data = users.objects.all().values()
        return Response(list(data))

@api_view(['GET'])
def get_likes(request):
    data = likes.objects.all().values()
    return Response(list(data))

@api_view(['POST'])
def update_likes(request):
    my_user = likes.objects.filter(email = "email@gmial.com").first()
    my_user.like_count += 1 #update like count for this user to be like_count + 1
    my_user.save()
    json_data = serializers.serialize('json', [my_user])
    # Return the JSON response
    return JsonResponse(json_data, safe=False)
    #from the previous user check the likes_count
@api_view(['POST'])
def update_username(request):
    my_user = users.objects.all().filter(username = "John").first()
    #my_user.username == input from user goes here
    my_user.save()
    json_data = serializers.serialize('json', [my_user])
    # Return the JSON response
    return JsonResponse(json_data, safe=False)
    #from the previous user check the likes_count

def home(request):
        return HttpResponse("Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.")
# Create your views here.

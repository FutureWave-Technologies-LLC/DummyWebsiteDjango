from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from django.contrib.auth.models import User

# validates fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['user_id', 'username', 'password']


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
        username = data.get('username')
        password = data.get('password')
        
        #check if user does not exist
        if not User.objects.filter(username = username).exists():
            new_user = User.objects.create_user()

        # my_user = users.objects.all().filter(user_id = 0).first()  
        # my_user = users.objects.create(user_id = '10').last()

        my_user.username = data.get('username')
        my_user.password = data.get('password')
        my_user.status = True
        my_user.save()
        json_data = serializers.serialize('json', [my_user])

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

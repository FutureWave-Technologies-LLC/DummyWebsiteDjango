from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import UsersSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from random import randrange
import hashlib


#GET ALL DATA FROM 'USERS' MODEL 
@api_view(['GET'])
def get_users(request):
    data = users.objects.all().values()
    return Response(list(data))

#GET USER'S DATA BASED ON ID
@api_view(['GET'])
def get_user_data(request):
    requested_user_id = request.GET.get("user_id")
    user = users.objects.filter(user_id = requested_user_id).first()
    
    if user:
        json_data = {"username": user.username, 
                     "user_id": user.user_id, 
                     "profile_image": user.profile_image,
                     "first_name": user.first_name,
                     "last_name": user.last_name,
                     "creation_date": user.creation_date,
                     "error": False}
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "User with this ID cannot be found", "error": True}
        return JsonResponse(json_data, safe=False)
    
#AUTHENTICATE USER AND RETURN A TOKEN WITH DATA
@api_view(['POST'])
def authenticate_user(request):
    data = request.data
    # Find the user by username
    user = users.objects.filter(username=data.get('username')).first()

    if user and user.password == hashlib.sha256(str(data.get('password')).encode()).hexdigest():
        # Generate token with user_id and username, add token_id for additional use
        json_data = {
            "username": user.username,
            "user_id": user.user_id,  # Include user_id here
            "token_id": randrange(1, 100000)  # Random token ID (you could replace this with a real token if needed)
        }
        return JsonResponse(json_data, safe=False, status=status.HTTP_200_OK)
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False, status=status.HTTP_400_BAD_REQUEST)

#LOGIN USER
@api_view(['GET'])
def login_user(request):
    request_username = request.GET.get("username")
    request_password = request.GET.get("password")
    
    user = users.objects.filter(username = request_username).first()
    # username not found
    if not user:
        json_data = {"response": "Invalid Username", "error": True}
        return JsonResponse(json_data, safe=False)
    
    # if user.password != request_password:
    if user.password != hashlib.sha256(str(request_password).encode()).hexdigest():
        json_data = {"response": "Invalid Password", "error": True}
        return JsonResponse(json_data, safe=False)
    
    json_data = {"response": "Successful login for "+user.username, "error": False}
    return JsonResponse(json_data, safe=False)

# SIGN-UP USER
@api_view(['POST'])
def signup_user(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()
    if user:
        # Return JSON that username is taken
        json_data = {"response": "Username already exists.", "error": True}
        return JsonResponse(json_data, safe=False)
    if len(data.get('password')) < 4:
        # Return JSON that invalid password
        json_data = {"response": "Password must be more than 4 characters long.", "error": True}
        return JsonResponse(json_data, safe=False)
    
    #hash password
    # print(f'RAW PASSWORD:{data['password']}')
    data['password'] = hashlib.sha256(str(data.get('password')).encode()).hexdigest()
    
    new_user_info = users(username=data.get('username'),
                          password=data.get('password'),
                          first_name=data.get('first_name'),
                          last_name=data.get('last_name'),
                          profile_image="")
    new_user_info.save()
    json_data = {"response": "User was created", "error": False}
    return JsonResponse(json_data, safe=False, status=status.HTTP_201_CREATED)
        

#SEARCH FOR USERS VIA SEARCHBAR
@api_view(['GET'])
def search_users(request):
    query_username = request.GET.get("query")
    matched_users = []
    for user in users.objects.all():
        if (user.username.find(query_username) != -1):
            matched_users.append({"username": user.username, "user_id": user.user_id})

    if len(matched_users) > 0:
        return(Response(matched_users))
    else:
        json_data = {"Response": f"No matching user found for: {query_username}", "error": True}
        return JsonResponse(json_data, safe=False)
    
#UPDATE USER'S SETTINGS
@api_view(['POST'])
def update_settings(request):
    data = request.data

    user = users.objects.filter(user_id=data.get('user_id')).first()

    #UPDATE FIELDS FOR USER
    user.profile_image = data.get('profile_image')
    user.save()

    return HttpResponse(status=status.HTTP_200_OK)

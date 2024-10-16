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

# View function for home page
def home(request):
    return render(request, 'home.html')

@api_view(['GET', 'POST'])
def get_users(request):
    if request.method == 'POST':
        data = request.data 
        user = users.objects.filter(username=data.get('username')).first()
        if user:
            # Display information message if username is taken
            json_data = {"response": "Username already exists, please choose another username", "error": True}
            # Return the JSON response
            return JsonResponse(json_data, safe=False)
        if len(data.get('password')) < 4:
            # Display information message if username is taken
            json_data = {"response": "Password must be more than 4 characters long", "error": True}
            # Return the JSON response
            return JsonResponse(json_data, safe=False)
        my_user = users.objects.all().count()
        my_user_info = users(user_id = my_user, username = data.get('username'), password = data.get('password')
                             ,status = False, first_name = data.get('first_name'), last_name = data.get('last_name'),
                             follower_id = my_user)
        my_user_info.save()
        json_data = {"response": "User was created", "error": False}
        # Return the JSON response
        return JsonResponse(json_data, safe=False)
        #from the previous user check the likes_count
    elif request.method == 'GET':
        data = users.objects.all().values()
        return Response(list(data))
    
#Gets a user's data based on username
@api_view(['GET'])
def get_user_data(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()
    
    #TBD: Function that compares password hashes
    if data.get('password') == user.password:
        data = user.values()
        return(Response(data))
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)
    
#Update token for a user
@api_view(['POST'])
def authenticate_user(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()
    
    #TBD: Function that compares password hashes
    if data.get('password') == user.password:
        print("password match")
        #data to be stored to token by frontend
        json_data = {"username": user.username,
                     "token_id": randrange(1, 100000, 1)
                     }
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)

    
@api_view(['POST'])
def recieving_posts(request):
    data = request.data
    my_post_id = posts.objects.all().count()
    my_post_info = posts(post_id = my_post_id, media = 'media', text = data.get('postText'), user_id = '9', title = data.get('title'), username = 'usernameGoesHere')
    my_post_info.save()
    json_data = {"Response": "Post was created", "error": False}
    return JsonResponse(json_data, safe=False)

@api_view(['GET','POST'])
def following(request):
    #gets data from the frontend
    data = request.data
    # temp values for the frontend, change the 'user_following_id' and 'following_id' to value specified in the frontend
    my_follow_id = data.get('user_follower_id') # is the user's follower_id
    following_id = data.get('following_id') # is the other user's follower_id they are trying to follow
    
    check_following_id = follow.objects.filter(follower_id= data.get('following_id')).first()
    check_follow_id = follow.objects.filter(follow_id = data.get('follow_id')).first()
    if check_following_id and check_follow_id == my_follow_id and following_id:
        unfollow = follow.objects.filter(following_id = check_following_id).delete()
        #unfollow.save()
        json_data = {"Response": f"{my_follow_id} successfully unfollowed {following_id}", "error": False}
        return JsonResponse(json_data, safe=False)
    #if user doesn't follow the other user it will create a new following
    else:
        my_follow_info = follow(follow_id = my_follow_id, followed_id = following_id)
        my_follow_info.save()
        json_data = {"Response": f"{my_follow_id} successfully followed {following_id}", "error": False}
        return JsonResponse(json_data, safe=False)

@api_view(['GET'])
def search_users(request):
    data = request.data
    my_username = data.get('username')
    username_check = users.objects.filter(username = my_username).first()
    if username_check:
        return(Response(my_username))
    else:
        #Display information message if user does not exist
        json_data = {"Response": f"No User found with username: {my_username}", "error": True}
        return JsonResponse(json_data, safe=False)

@api_view(['GET'])
def get_post_data(request):
    data = posts.objects.all().values()
    return(Response(data))

# View function for login page
@api_view(['POST'])
def login_page(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    print("test")
    #fetching the user from database
    user = users.objects.filter(username=username).first()
    if not user:
        # Display an error message if the username does not exist
        json_data = {"response": "Username was not valid", "error": True}
        return JsonResponse(json_data, safe=False)
    # Check if user with the provided username exists
    #if password doesn't match return error
    #TBD: Function that compares password hashes
    if user.password != password:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)
    # Log in the user and redirect to home page upon sign in
    json_data = {"response": "Valid user", "error": False}
    return JsonResponse(json_data, safe=False)

# View function for registration page
@api_view(['POST'])
def register_page(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    # Check if user with provided username already exists
    user = users.objects.filter(username=username)

    if user.exists():
        # Display information message if username is taken
        messages.info(request, "Username is already taken")
        return redirect('/register/')

    # Create a new User object with the provided information
    user = users.objects.create_user(
        username=username,
    )

    # Set user's password and save user object
    user.set_password(password)
    user.save()

    # Display information message indicating successful acount creation
    messages.info(request, "Account created Successfully")
    return redirect('/register/')

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

#def home(request):
        #return HttpResponse("Welcome to the Dummy Website API. Visit ' http://localhost:8000/api/dummy-data/ ' to fetch data.")

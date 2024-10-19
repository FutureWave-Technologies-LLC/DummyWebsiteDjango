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

# View function for home page
def home(request):
    return render(request, 'home.html')

#GET ALL DATA FROM 'USERS' MODEL 
@api_view(['GET'])
def get_users(request):
    data = users.objects.all().values()
    return Response(list(data))

#GET USER'S DATA BASED ON ID
@api_view(['GET'])
def get_user_data(request):
    requested_user_id = request.GET.get("user_id")
    user_data = users.objects.filter(user_id=requested_user_id).values()
    
    if user_data:
        return(Response(user_data))
    else:
        json_data = {"response": "User with this ID cannot be found", "error": True}
        return JsonResponse(json_data, safe=False)
    
#AUTHENTICATE USER AND RETURN A TOKEN WITH DATA
@api_view(['POST'])
def authenticate_user(request):
    data = request.data
    user = users.objects.filter(username=data.get('username')).first()

    #TBD: Function that compares password hashes
    if data.get('password') == user.password:
        #data that the frontend token stores
        json_data = {"username": user.username,
                     "token_id": randrange(1, 100000, 1)
                     }
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "Password was not valid", "error": True}
        return JsonResponse(json_data, safe=False)

#SIGN-IN/LOGIN USER
@api_view(['GET'])
def login_user(request):
    request_username = request.GET.get("username")
    request_password = request.GET.get("password")
    
    user = users.objects.filter(username = request_username).first()
    # username not found
    if not user:
        json_data = {"response": "Username is not valid", "error": True}
        return JsonResponse(json_data, safe=False)
    #TBD: Function that compares password hashes
    if user.password != request_password:
        json_data = {"response": "Password is not valid", "error": True}
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
        json_data = {"response": "Username already exists, please choose another username", "error": True}
        return JsonResponse(json_data, safe=False)
    if len(data.get('password')) < 4:
        # Return JSON that invalid password
        json_data = {"response": "Password must be more than 4 characters long", "error": True}
        return JsonResponse(json_data, safe=False)
    
    new_user_id = users.objects.all().count()+1
    new_user_info = users(user_id = new_user_id, username = data.get('username'), password = data.get('password')
                            ,status = False, first_name = data.get('first_name'), last_name = data.get('last_name'),
                            follower_id = new_user_id)
    new_user_info.save()
    json_data = {"response": "User was created", "error": False}
    return JsonResponse(json_data, safe=False)

#SEARCH FOR USERS VIA SEARCHBAR
@api_view(['GET'])
def search_users(request):
    query_username = request.GET.get("query")
    matched_users = []
    for user in users.objects.all():
        if (user.username.find(query_username) != -1):
            matched_users.append({"username": user.username})

    if len(matched_users) > 0:
        return(Response(matched_users))
    else:
        json_data = {"Response": f"No matching user found for: {query_username}", "error": True}
        return JsonResponse(json_data, safe=False)

#API FOR FOLLOWERS
@api_view(['GET','POST'])
def followers(request):
    #USER FOLLOWS ANOTHER USER
    if request.method == 'POST':
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
    #RETURNS LIST OF USER'S FOLLOWERS
    elif request.method == 'GET':
        request_user_id = request.GET.get("user_id")
        #TODO:
        return JsonResponse({"Response": 1111}, safe=False)
        


#CREATES A POST
@api_view(['POST'])
def recieving_posts(request):
    data = request.data
    
    my_post_id = posts.objects.all().count()
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

#GET MESSAGES
@api_view(['GET'])
def get_messages(request):
    data = messages.objects.all().values()
    return Response(list(data))

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

#GET PERSONAL PAGES
@api_view(['GET'])
def get_personal_pages(request):
    data = personal_pages.objects.all().values()
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

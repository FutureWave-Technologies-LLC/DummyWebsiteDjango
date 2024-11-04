from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
# from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .serializers import MessageSerializer
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
    user = users.objects.filter(user_id = requested_user_id).first()
    
    if user:
        json_data = {"username": user.username, "user_id": user.user_id, "error": False}
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "User with this ID cannot be found", "error": True}
        return JsonResponse(json_data, safe=False)
    
#GET MESSAGES
@api_view(['GET'])
def get_user_messages(request):
    user = request.user
    user_messages = messages.objects.filter(user=user) | messages.objects.filter(reciever_id=user.id)
    serializer = MessageSerializer(user_messages, many=True)
    return Response(serializer.data)

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
        serializer_class = MessageSerializer
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
#AUTHENTICATE USER AND RETURN A TOKEN WITH DATA
from random import randrange
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import users  # Assuming 'users' is your user model

@api_view(['POST'])
def authenticate_user(request):
    data = request.data
    # Find the user by username
    user = users.objects.filter(username=data.get('username')).first()

    # Check if user exists and compare passwords (you should hash and compare passwords in a secure way)
    if user and data.get('password') == user.password:
        # Generate token with user_id and username, add token_id for additional use
        json_data = {
            "username": user.username,
            "user_id": user.user_id,  # Include user_id here
            "token_id": randrange(1, 100000)  # Random token ID (you could replace this with a real token if needed)
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
            matched_users.append({"username": user.username, "user_id": user.user_id})

    if len(matched_users) > 0:
        return(Response(matched_users))
    else:
        json_data = {"Response": f"No matching user found for: {query_username}", "error": True}
        return JsonResponse(json_data, safe=False)

#API FOR FOLLOWING
@api_view(['GET','POST'])
def following(request):
    #USER FOLLOWS ANOTHER USER
    if request.method == 'POST':
        data = request.data 
        request_username_to_follow = data.get("username_to_follow")
        request_follower_id = data.get("follower_id")

        #USER TO FOLLOW
        user_to_follow = users.objects.filter(username = request_username_to_follow).first()
        to_follow_username = user_to_follow.username
        to_follow_id = user_to_follow.user_id
        
        #GET FOLLOWS WITH THE ID OF FOLLOWER (WHO SENT FROM REQUEST) 
        follows_with_follower = follow.objects.filter(follower_id = request_follower_id)
        isFollowing = False
        primary_key = -1

        #CHECK IN EACH FOLLOW IF HAVE ID OF USER TO FOLLOW
        if follows_with_follower:
            for follow_with_follower in follows_with_follower:
                if follow_with_follower.followee_id == to_follow_id:
                    isFollowing = True
                    primary_key = follow_with_follower.primary_key
                    break
        
        #USER HAS FOLLOWED USER
        if isFollowing:
            current_follow = follow.objects.filter(primary_key = primary_key).first()
            current_follow.delete()
            json_data = {"Response": f"{request_follower_id} unfollowed {to_follow_id} ({to_follow_username})", 
                         "Followed": False,
                         "error": False,}
            return JsonResponse(json_data, safe=False)
        
        #USER HAS NOT FOLLOWED USER OR NOT FOLLOWED AT ALL
        else:
            #PRIMARY KEY IS THE LAST FOLLOW'S PRIMARY KEY+1
            new_primary_key = -1
            if (follow.objects.last()):
                new_primary_key = follow.objects.last().primary_key + 1
            else:
                new_primary_key = 0
            new_follow_info = follow(primary_key = new_primary_key,
                                     follower_id = request_follower_id,
                                     followee_id = to_follow_id)
            new_follow_info.save()
            json_data = {"Response": f"{request_follower_id} followed {to_follow_id} ({to_follow_username})", 
                         "Followed": True,
                         "error": False,}
            return JsonResponse(json_data, safe=False)
           
    #RETURNS LIST OF USER'S FOLLOWEES
    elif request.method == 'GET':
        request_follower_id = request.GET.get("user_id")
        follows_with_follower = follow.objects.filter(follower_id = request_follower_id)
        followings = []
        for follow_with_follower in follows_with_follower:
            followee = users.objects.filter(user_id = follow_with_follower.followee_id).first()
            followings.append({"username": followee.username, "user_id":followee.user_id})
        return(Response(followings))
    
#API FOR RETURNS LIST OF A USER'S FOLLOWERS
@api_view(['GET'])
def get_followers(request): 
    request_user_id = request.GET.get("user_id")
    follows_with_followee = follow.objects.filter(followee_id = request_user_id)
    followings = []
    for follow_with_followee in follows_with_followee:
        follower = users.objects.filter(user_id = follow_with_followee.follower_id).first()
        followings.append({"username": follower.username, "user_id":follower.user_id})
    return(Response(followings))

#GETS PROFILE POSTS
@api_view(['GET'])
def profile_posts(request):
    username = request.GET.get('username')
    post = posts.objects.filter(username=username).values()  # Assuming posts have a 'username' field
    return JsonResponse(list(post), safe=False)

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

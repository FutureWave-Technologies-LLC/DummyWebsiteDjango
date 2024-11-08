from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from users.models import users
from posts.models import posts
from django.http import HttpResponse
from django.http import JsonResponse

#GETS PROFILE POSTS
@api_view(['GET'])
def profile_posts(request):
    username = request.GET.get('username')
    post = posts.objects.filter(username=username).values()  # Assuming posts have a 'username' field
    return JsonResponse(list(post), safe=False)

#API FOR FOLLOWING
@api_view(['GET','POST'])
def following(request):
    #USER FOLLOWS ANOTHER USER
    if request.method == 'POST':
        data = request.data 
        request_username_to_follow = data.get("username_to_follow")
        request_follower_id = data.get("follower_id")

        #USER TO FOLLOW
        followee_user = users.objects.filter(username = request_username_to_follow).first()
        followee_username = followee_user.username
        followee_id = followee_user.user_id
        
        #GET FOLLOWS WITH THE ID OF FOLLOWER (WHO SENT FROM REQUEST) 
        follower_user = users.objects.filter(user_id=request_follower_id).first()
        follows_with_follower = follow.objects.filter(follower_id = request_follower_id)
        isFollowing = False
        primary_key = -1

        #CHECK IN EACH FOLLOW IF HAVE ID OF USER TO FOLLOW
        if follows_with_follower:
            for follow_with_follower in follows_with_follower:
                if follow_with_follower.followee_id == followee_id:
                    isFollowing = True
                    primary_key = follow_with_follower.primary_key
                    break
        
        #USER HAS FOLLOWED USER
        if isFollowing:
            current_follow = follow.objects.filter(primary_key = primary_key).first()
            current_follow.delete()
            json_data = {"Response": f"{request_follower_id} unfollowed {followee_id} ({followee_username})", 
                         "Followed": False,
                         "error": False,}
            return JsonResponse(json_data, safe=False)
        
        #USER HAS NOT FOLLOWED USER OR NOT FOLLOWED AT ALL
        else:
            #PRIMARY KEY IS THE LAST FOLLOW'S PRIMARY KEY+1
            new_primary_key = 0
            if (follow.objects.last()):
                new_primary_key = follow.objects.last().primary_key + 1
            new_follow_info = follow(primary_key = new_primary_key,
                                     follower_id = request_follower_id,
                                     followee_id = followee_id,
                                     followee_model = followee_user)
            new_follow_info.save()
            json_data = {"Response": f"{request_follower_id} followed {followee_id} ({followee_username})", 
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

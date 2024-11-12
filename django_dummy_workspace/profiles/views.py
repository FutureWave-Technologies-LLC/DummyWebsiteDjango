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
    user = users.objects.filter(user_id=request.GET.get('user_id')).first()
    response_set = []
    for post in posts.objects.filter(author=user):
        response_set.append({"post_id": post.post_id, 
                            "title": post.title, 
                            "description": post.description,
                            "username": post.author.username,
                            "media": post.media,
                            "creation_date": post.creation_date})
    return Response(response_set)

#API FOR FOLLOWING
@api_view(['GET','POST'])
def following(request):
    #USER FOLLOWS ANOTHER USER
    if request.method == 'POST':
        data = request.data 
        request_followee_username = data.get("followee_username")
        request_follower_id = data.get("follower_id")

        #FIND THE FOLLOWEE
        followee_user = users.objects.filter(username = request_followee_username).first()
        followee_username = followee_user.username
        followee_id = followee_user.user_id
        
        #GET FOLLOWS WITH THE ID OF FOLLOWER (WHO SENT FROM REQUEST) 
        follower_user = users.objects.filter(user_id=request_follower_id).first()
        follows_with_follower = follow.objects.filter(follower_id = request_follower_id)
        primary_key = -1

        #CHECK IN EACH FOLLOW IF HAVE ID OF USER TO FOLLOW
        if follows_with_follower:
            for follow_with_follower in follows_with_follower:
                if follow_with_follower.followee_id == followee_id:
                    primary_key = follow_with_follower.pk_follow
                    break
        
        #USER HAS FOLLOWED USER
        if primary_key != -1:
            current_follow = follow.objects.filter(pk_follow = primary_key).first()
            current_follow.delete()
            json_data = {"Response": f"{request_follower_id} unfollowed {followee_id} ({followee_username})", 
                         "Followed": False,
                         "error": False,}
            return JsonResponse(json_data, safe=False)
        
        #USER HAS NOT FOLLOWED USER OR NOT FOLLOWED AT ALL
        else:
            new_follow_info = follow(follower = follower_user,
                                     followee_id = followee_id)
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

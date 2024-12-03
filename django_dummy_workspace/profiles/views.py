from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import follow
from users.models import users
from posts.models import posts
from django.http import JsonResponse

# GET PROFILE POSTS
@api_view(['GET'])
def profile_posts(request):
    user_id = request.GET.get('user_id')
    user = users.objects.filter(user_id=user_id).first()
    
    if not user:
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    response_set = []
    for post in posts.objects.filter(author=user).order_by("creation_date"):
        response_set.append({
            "post_id": post.post_id, 
            "title": post.title,  
            "description": post.description,
            "username": post.author.username,
            "media": post.media,
            "creation_date": post.creation_date
        })
    return Response(response_set)

# API FOR FOLLOWING
@api_view(['GET', 'POST'])
def following(request):
    #FOLLOW/UNFOLLOW
    if request.method == 'POST':
        data = request.data
        followee_username = data.get("followee_username")
        follower_id = data.get("follower_id")
        
        # Find the followee user
        followee_user = users.objects.filter(username=followee_username).first()
        if not followee_user:
            return Response({"error": "Followee does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Find the follower user
        follower_user = users.objects.filter(user_id=follower_id).first()
        if not follower_user:
            return Response({"error": "Follower does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the follower is trying to follow themselves
        if follower_user == followee_user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the follow relationship exists
        try:
            followee = users.objects.get(username=followee_username)  # Look up the user by username
            existing_follow = follow.objects.filter(follower=follower_user, followee_id=followee_user.user_id).first()
        except users.DoesNotExist:
            # Handle the case when the followee username doesn't exist
            existing_follow = None

        
        if existing_follow:
            # If the relationship exists, unfollow (delete)
            existing_follow.delete()
            return Response({
                "Followed": False,
                "error": False,
                "Response": f"{follower_id} unfollowed {followee_user.user_id} ({followee_user.username})"
            })
        else:
            # If the relationship does not exist, follow (create)
            follow.objects.create(follower=follower_user, 
                                  followee_id=followee.user_id)
            return Response({
                "Followed": True,
                "error": False,
                "Response": f"{follower_id} followed {followee_user.user_id} ({followee_user.username})"
            })

    #FIND IF USER FOLLOWED BASED ON FOLLOWEE_ID 
    elif request.method == 'GET':
        user_id = request.GET.get("user_id")
        followee_id = request.GET.get("followee_id")
        follower_user = users.objects.filter(user_id=user_id).first()

        if not follower_user:
            return Response({"error": "Follower does not exist"}, status=status.HTTP_404_NOT_FOUND)

        followings = follow.objects.filter(follower=follower_user)
        for following in followings:
            if following.followee_id == int(followee_id):
                return Response(True)
        
        return Response(False)


# API FOR GETTING A USER'S FOLLOWERS
@api_view(['GET'])
def get_followers(request):
    user_id = request.GET.get("user_id")
    user = users.objects.filter(user_id=user_id).first()
    
    if not user:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    followers = follow.objects.filter(followee_id=user.user_id)
    followers_list = [{"username": follower.username, "user_id": follower.user_id} for follower in users.objects.filter(user_id__in=[f.follower_id for f in followers])]
    
    return Response(followers_list)

#seperated from "following" view 
# API FOR GETTING A USER'S FOLLOWEES
@api_view(['GET'])
def get_followees(request):
    user_id = request.GET.get("user_id")
    follower_user = users.objects.filter(user_id=user_id).first()

    if not follower_user:
        return Response({"error": "Follower does not exist"}, status=status.HTTP_404_NOT_FOUND)

    followings = follow.objects.filter(follower=follower_user)
    followings_list = [{"username": followee.username, "user_id": followee.user_id} for follow in followings for followee in users.objects.filter(user_id=follow.followee_id)]
    
    return Response(followings_list)

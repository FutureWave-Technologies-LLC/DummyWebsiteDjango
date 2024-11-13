from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from random import randrange
from .serializers import *

#API FOR CREATE OR GET A POST
@api_view(['GET','POST'])
def post(request):
    #GET ALL DATA FOR A POST BASED ON ID
    if request.method == 'GET':
        post = posts.objects.filter(post_id=request.GET.get('post_id')).first()
        if post:
            json_data = {"post_id": post.post_id, 
                        "title": post.title, 
                        "description": post.description,
                        "username": post.author.username,
                        "user_id": post.author.user_id,
                        "media": post.media,
                        "creation_date": post.creation_date}
            return JsonResponse(json_data, safe=False)
        else:
            json_data = {"response": "Post with this ID cannot be found", "error": True}
            return JsonResponse(json_data, safe=False)
    #CREATE POST
    elif request.method == 'POST':
        data = request.data.copy()
    
        user = users.objects.filter(user_id=data.get('user_id')).first()

        my_post_info = posts(author = user,   
                             title = data.get('title'),
                             description = data.get('description'),
                             media = data.get('media'))
        my_post_info.save()
        json_data = {"Response": "Post was created", "error": False}
        return JsonResponse(json_data, safe=False, status=status.HTTP_201_CREATED)

#GET ALL POSTS DATA
@api_view(['GET'])
def get_posts(request):
    response_set = []
    for post in posts.objects.all().order_by("creation_date"):
        response_set.append({"post_id": post.post_id, 
                            "title": post.title, 
                            "description": post.description,
                            "username": post.author.username,
                            "media": post.media,
                            "creation_date": post.creation_date})
    return Response(response_set)
    

#GET REPLIES
@api_view(['GET'])
def get_replies(request):
    data = replies.objects.all().values()
    return Response(list(data))

#COMMENTS API
@api_view(['GET','POST'])
def get_comments(request):
    #GET COMMENT FEED BASED ON POST ID
    if request.method == 'GET':
        request_post_id = request.GET.get("post_id")
        comment_feed = []
        comments_of_post = comments.objects.filter(post_id = request_post_id).order_by("creation_date")
        for comment in comments_of_post:
            user = users.objects.filter(user_id = comment.author.user_id).first()
            comment_feed.append({"username": user.username,
                                 "profile_image": user.profile_image,
                                 "user_id": user.user_id,
                                 "comment": comment.comment,
                                 "creation_date": comment.creation_date})
        return Response(comment_feed)
    #CREATE NEW COMMENT
    elif request.method == 'POST':
        print(f'COMMENT:{request.data.get("comment")}')
        user = users.objects.filter(user_id=request.data.get("user_id")).first()
        post = posts.objects.filter(post_id=request.data.get("post_id")).first()
        comment_info = comments(author = user,
                                post = post,
                                comment = request.data.get("comment"))
        comment_info.save()
        print(comment_info.pst_creation_date())
        return JsonResponse({"Response": "Commented created"}, safe=False)

#GET PERSONAL PAGES
# @api_view(['GET'])
# def get_personal_pages(request):
#     data = personal_pages.objects.all().values()
#     return Response(list(data))

# #GET LIKES
# @api_view(['GET'])
# def get_likes(request):
#     data = likes.objects.all().values()
#     return Response(list(data))

# #UPDATE LIKES
# @api_view(['POST'])
# def update_likes(request):
#     my_user = likes.objects.filter(email = "email@gmial.com").first()
#     my_user.like_count += 1 #update like count for this user to be like_count + 1
#     my_user.save()
#     json_data = serializers.serialize('json', [my_user])
#     # Return the JSON response
#     return JsonResponse(json_data, safe=False)
#     #from the previous user check the likes_count
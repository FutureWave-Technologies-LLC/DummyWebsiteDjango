from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
from random import randrange

#CREATES A POST
@api_view(['POST'])
def recieving_posts(request):
    data = request.data
    
    my_post_id = posts.objects.all().count()+1
    user = users.objects.filter(username=data.get('username')).first()

    my_post_info = posts(post_id = my_post_id, 
                         media = "", 
                         text = data.get('postText'), 
                         user_id = user.user_id, 
                         title = data.get('title'), 
                         username = user.username,
                         user_model = user)
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
                     "media": post.media,
                     "creation_date": post.creation_date}
        return JsonResponse(json_data, safe=False)
    else:
        json_data = {"response": "Post with this ID cannot be found", "error": True}
        return JsonResponse(json_data, safe=False)

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
        comments_of_post = comments.objects.filter(post_id = request_post_id)
        for comment in comments_of_post:
            user = users.objects.filter(user_id = comment.user_id).first()
            comment_feed.append({"username": user.username, 
                                 "user_id": user.user_id,
                                 "comment": comment.comment,
                                 "creation_date": comment.creation_date})
        return Response(comment_feed)
    #CREATE NEW COMMENT
    elif request.method == 'POST':
        request_user_id = request.data.get("user_id")
        request_post_id = request.data.get("post_id")
        request_comment = request.data.get("comment")

        new_primary_key = 0
        if (comments.objects.last()):
            new_primary_key = comments.objects.last().comment_id + 1
        user = users.objects.filter(user_id=request_user_id).first()
        post = posts.objects.filter(post_id=request_post_id).first()
        comment_info = comments(comment_id = new_primary_key,
                                user_id = request_user_id,
                                post_id = request_post_id,
                                comment = request_comment,
                                user_model = user,
                                post_model = post)
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
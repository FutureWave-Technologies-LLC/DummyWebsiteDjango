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
            return JsonResponse(json_data, safe=False, status=status.HTTP_404_NOT_FOUND)
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
    sort_type = request.GET.get('sort_type')
    response_set = []
    for post in posts.objects.all().order_by("creation_date"):
            queryset = likes.objects.filter(post_id = post.post_id)
            post_data = {"post_id": post.post_id, 
                                "title": post.title, 
                                "description": post.description,
                                "username": post.author.username,
                                "media": post.media,
                                "creation_date": post.creation_date}
            if sort_type == "recent":
                post_data["recent_like_count"] = queryset.count()
            elif sort_type == "popular":
                post_data["popular_like_count"] = queryset.count()
            response_set.append(post_data)

    return Response(response_set)
    
#LIKES API
@api_view(['GET','POST'])
def likes_view(request):
    #GET TOTAL LIKES AND BOOLEAN IF USER LIKED
    if request.method == 'GET':
        request_user_id = request.GET.get('user_id')
        request_post_id = request.GET.get("post_id")
        queryset = likes.objects.filter(post_id = request_post_id)

        #Total likes
        like_count = queryset.count()

        #Did user like?
        user_liked = False
        query_user_like = queryset.filter(author_id = request_user_id).first()
        if query_user_like:
            user_liked = True
        json_data = {"total_likes": like_count, "user_liked": user_liked} 
        return JsonResponse(json_data, safe=False)
    
    #UPDATE LIKE
    elif request.method == 'POST':
        request_user_id = request.data.get('user_id')
        request_post_id = request.data.get('post_id')

        #Find if user liked or not
        queryset = likes.objects.filter(post_id = request_post_id)
        query_user_like = queryset.filter(author_id = request_user_id).first()

        #User already liked, thus unlike
        if query_user_like:
            query_user_like.delete()
            return Response({
                "Liked": False,
                "error": False,
                "Response": f"{request_user_id} unliked post with id {request_post_id}"
            })
        #User did not like, thus like
        else:
            user = users.objects.filter(user_id = request_user_id).first()
            post = posts.objects.filter(post_id = request_post_id).first()
            likes.objects.create(author = user,
                                 post = post)
            return Response({
                "Liked": True,
                "error": False,
                "Response": f"{request_user_id} liked post with id {request_post_id}"
            })


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
                                 "comment_id": comment.comment_id,
                                 "creation_date": comment.creation_date})
        return Response(comment_feed)
    #CREATE NEW COMMENT
    elif request.method == 'POST':
        request_user_id = request.data.get("user_id")
        request_post_id = request.data.get("post_id")

        user = users.objects.filter(user_id= request_user_id).first()
        post = posts.objects.filter(post_id= request_post_id).first()
        comment_info = comments(author = user,
                                post = post,
                                comment = request.data.get("comment"))
        comment_info.save()
        return JsonResponse({"Response": "Commented created"}, safe=False)

#REPLIES API
@api_view(['GET','POST'])
def get_replies(request):
    #GET MAIN COMMENT AND REPLIES
    if request.method == 'GET':
        request_comment_id = request.GET.get("comment_id")

        comment_feed = []
        
        comment = comments.objects.filter(comment_id = request_comment_id).first()
        
        #Get main comment
        user = users.objects.filter(user_id = comment.author.user_id).first()
        comment_feed.append({"username": user.username,
                                "profile_image": user.profile_image,
                                "user_id": user.user_id,
                                "comment": comment.comment,
                                "comment_id": comment.comment_id,
                                "creation_date": comment.creation_date,
                                "main_comment": True})
        
        #Get replies
        queryset = replies.objects.filter(comment_id = request_comment_id).order_by("creation_date")
        for reply in queryset:
            user = users.objects.filter(user_id = reply.author.user_id).first()
            comment_feed.append({"username": user.username,
                                "profile_image": user.profile_image,
                                "user_id": user.user_id,
                                "reply": reply.reply,
                                "reply_id": reply.reply_id,
                                "creation_date": reply.creation_date})

        return Response(comment_feed)
    
    #CREATE REPLY
    elif request.method == 'POST':        
        request_user_id = request.data.get("user_id")
        request_comment_id = request.data.get("comment_id")
        request_reply_text = request.data.get("reply")

        user = users.objects.filter(user_id = request_user_id).first()
        comment = comments.objects.filter(comment_id = request_comment_id).first()
        
        replies.objects.create(author = user,
                                comment_id = comment.comment_id,
                                reply = request_reply_text)
        return JsonResponse({"Response": "Reply created"}, safe=False)
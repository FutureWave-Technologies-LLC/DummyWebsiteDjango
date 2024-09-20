from django.urls import path
from .views import *

urlpatterns = [
    path('likes/', get_likes, name = 'likes'),
    path('users/', get_users, name = 'users'),  # Define the URL pattern for your API
    path('update_likes/', update_likes, name = 'update likes'),
    path('posts/', get_posts, name = 'posts'),
    path('personal_pages/', get_personal_pages, name = 'personal_pages'),
    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),
    path('messages/', get_messages, name = 'messages'),
]
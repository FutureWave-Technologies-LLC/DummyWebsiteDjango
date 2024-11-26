from django.urls import path
from .views import *

urlpatterns = [
    path('all_posts/', get_posts, name = 'all_posts'),
    path('post/', post, name = 'post'),

    path('likes/', likes_view, name = 'likes'),

    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),
]
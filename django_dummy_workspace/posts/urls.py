from django.urls import path
from .views import *

urlpatterns = [
    path('all_posts/', get_posts, name = 'all_posts'),
    path('post/', post, name = 'post'),

    #path('likes/', get_likes, name = 'likes'),
    #path('update_likes/', update_likes, name = 'update likes'),

    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),
]
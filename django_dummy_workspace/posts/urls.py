from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', get_posts, name = 'posts'),
    path('get_post/', get_post, name = 'post'),
    path('recieving_posts/', recieving_posts, name = 'getting_post_data'),

    #path('likes/', get_likes, name = 'likes'),
    #path('update_likes/', update_likes, name = 'update likes'),

    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),
]
from django.urls import path
from .views import *

urlpatterns = [
    #POST RELATED
    path('recieving_posts/', recieving_posts, name = 'getting_post_data'),
    path('posts/', get_posts, name = 'posts'),
    #path('get_posts/', get_posts, name = 'post'),

    path('likes/', get_likes, name = 'likes'),
    path('update_likes/', update_likes, name = 'update likes'),

    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),
]
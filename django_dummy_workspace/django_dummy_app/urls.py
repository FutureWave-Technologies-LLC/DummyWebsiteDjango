from django.urls import path
from .views import *

urlpatterns = [
    # USERS
    path('users/', get_users, name = 'users'),
    path('get_user_data/', get_user_data, name = 'users'),
    path('authenticate_user/', authenticate_user, name='users'),
    path('search_users/', search_users, name = 'searching users'),

    #FOLLOW
    path('follow/,', followers, name='following'),

    #POST RELATED
    path('posts/', get_posts, name = 'posts'),
    path('recieving_posts/', recieving_posts, name = 'getting_post_data'),

    path('likes/', get_likes, name = 'likes'),
    path('update_likes/', update_likes, name = 'update likes'),

    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),

    #MESSAGE
    path('messages/', get_messages, name = 'messages'),

    #LOGIN/SIGN-UP
    path('login/', login_user, name = 'login'),
    path('sign_up/', signup_user, name = 'sign_up'),

    #OTHER
    path('personal_pages/', get_personal_pages, name = 'personal_pages'),
    
]
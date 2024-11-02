from django.urls import path
from .views import *

urlpatterns = [
    # USERS
    path('users/', get_users, name = 'users'),
    path('get_user_data/', get_user_data, name = 'users'),
    path('authenticate_user/', authenticate_user, name='users'),
    path('search_users/', search_users, name = 'searching users'),

    #FOLLOW
    path('following/', following, name='follow'),
    path('get_followers/', get_followers, name='follow'),

    #POST RELATED
    path('posts/', get_posts, name = 'posts'),
    path('get_post/', get_post, name = 'post'),
    path('recieving_posts/', recieving_posts, name = 'getting_post_data'),
    path('profile_posts/', profile_posts, name = 'profile posts'),

    path('likes/', get_likes, name = 'likes'),
    path('update_likes/', update_likes, name = 'update likes'),

    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),

    #MESSAGE
    path('messages/', get_messages, name = 'messages'),
    path('get_messages/', get_user_messages, name='get_messages'),
    path('send_messages/', send_message, name='send_message'),

    #LOGIN/SIGN-UP
    path('login/', login_user, name = 'login'),
    path('sign_up/', signup_user, name = 'sign_up'),

    #OTHER
    path('personal_pages/', get_personal_pages, name = 'personal_pages'),
    
]
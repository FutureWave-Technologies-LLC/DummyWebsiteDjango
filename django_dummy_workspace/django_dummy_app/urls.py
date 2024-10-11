from django.urls import path
from .views import *

urlpatterns = [
    path('likes/', get_likes, name = 'likes'),
    path('users/', get_users, name = 'users'),  # Define the URL pattern for your API
    path('update_likes/', update_likes, name = 'update likes'),
    path('posts/', get_posts, name = 'posts'),
    path('recieving_posts/', recieving_posts, name = 'getting_post_data'),
    path('personal_pages/', get_personal_pages, name = 'personal_pages'),
    path('comments/', get_comments, name = 'comments'),
    path('replies/', get_replies, name = 'replies'),
    path('messages/', get_messages, name = 'messages'),
    
    path('login_page/', login_page, name = 'login_page'),
    path('messages/chat/<int:chat_id>/', get_messages_for_chat, name = 'getting_messages_for_chat'),
    path('messages/send/', send_message, name='send_message'),
    path('chat_get/', get_chat_info, name ='get_chat_info'),
    path('chat_create/', create_chat, name='create_chat'),

    path('authenticate_user/', authenticate_user, name='users'),
    path('get_user_data/', get_user_data, name = 'users')
]
from django.urls import path
from .views import *

urlpatterns = [
    # USERS
    path('users/', get_users, name = 'users'),
    path('get_user_data/', get_user_data, name = 'users'),
    path('authenticate_user/', authenticate_user, name='users'),
    path('search_users/', search_users, name = 'searching users'),
]
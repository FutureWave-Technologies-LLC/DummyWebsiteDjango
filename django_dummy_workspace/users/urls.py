from django.urls import path
from .views import *

urlpatterns = [
    path('users/', get_users, name = 'users'),
    path('get_user_data/', get_user_data, name = 'get_user_data'),
    path('authenticate_user/', authenticate_user, name='users'),
    path('search_users/', search_users, name = 'searching users'),

    #LOGIN/SIGN-UP
    path('login/', login_user, name = 'login'),
    path('sign_up/', signup_user, name = 'sign_up')
]
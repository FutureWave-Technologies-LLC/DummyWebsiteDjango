from django.urls import path
from .views import *

urlpatterns = [
    path('users/', get_users, name = 'user'),
    path('get_user_data/', get_user_data, name = 'get_user_data'),
    path('search_users/', search_users, name = 'searching_users'),

    #LOGIN/SIGN-UP
    path('login/', login_user, name = 'login'),
    path('sign_up/', signup_user, name = 'sign_up'),

    #AUTHENTICATING
    path('authenticate_user/', authenticate_user, name='authenticate'),
    path('compare_tokens/', compare_token_ids, name='compare token'),

    path('update_settings/', update_settings, name = 'settings')
]
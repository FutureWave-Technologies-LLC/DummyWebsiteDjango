from django.urls import path
from .views import *

urlpatterns = [
    path('following/', following, name='following'),
    path('get_followers/', get_followers, name='get_followers'),
    path('profile_posts/', profile_posts, name = 'profile_posts'),
]

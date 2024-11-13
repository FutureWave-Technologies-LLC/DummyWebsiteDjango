from django.urls import path
from .views import *

urlpatterns = [
    path('following/', following, name='follow'),
    path('get_followers/', get_followers, name='follow'),
    
    path('profile_posts/', profile_posts, name = 'profile posts'),
]

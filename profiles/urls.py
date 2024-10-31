from django.urls import path
from .views import *

urlpatterns = [
    #FOLLOW
    path('following/', following, name='follow'),
    path('get_followers/', get_followers, name='follow'),

    path('profile_posts/', profile_posts, name = 'profile posts'),
    path('personal_pages/', get_personal_pages, name = 'personal_pages'),
]
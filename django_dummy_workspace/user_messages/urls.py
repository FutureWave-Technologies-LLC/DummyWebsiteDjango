from django.urls import path
from .views import *

urlpatterns = [
    #MESSAGE
    path('message/', messages, name = 'messages'),

    path('messagable_users/', get_messageable_users, name = 'messageable_users')
]
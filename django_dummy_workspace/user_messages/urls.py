from django.urls import path
from .views import *

urlpatterns = [
    #MESSAGE
    path('messages/', messages, name = 'messages'),
]
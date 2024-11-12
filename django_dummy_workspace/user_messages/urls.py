from django.urls import path
from .views import *

urlpatterns = [
    #MESSAGE
    path('message/', messages, name = 'messages'),
]
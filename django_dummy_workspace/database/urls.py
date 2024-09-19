from django.urls import path
from .views import *  # Import the view function

urlpatterns = [
    path('dummy-data/', get_users, name = 'dummy data'),  # Define the URL pattern for your API
]
from django.urls import path
from .views import get_client_info  # Import the view function
from .views import get_likes
from .views import update_likes

urlpatterns = [
    path('likes/', get_likes, name = 'likes'),
    path('client-info/', get_client_info, name = 'client info'),  # Define the URL pattern for your API
    path('update_likes/', update_likes, name = 'update likes'),
]
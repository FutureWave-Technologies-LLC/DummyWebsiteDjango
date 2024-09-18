from django.urls import path
from .views import get_dummy_data  # Import the view function

urlpatterns = [
    path('dummy-data/', get_dummy_data, name = 'dummy_data'),  # Define the URL pattern for your API
]
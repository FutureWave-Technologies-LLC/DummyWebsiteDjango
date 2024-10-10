from django.urls import path
from .views import *

# From this tutorial https://youtu.be/Q7N2oJTnThA?si=Nbhy02sBxpZk-g3r. Does not work
urlpatterns = [
    path('', message_view, name="messages"),
]
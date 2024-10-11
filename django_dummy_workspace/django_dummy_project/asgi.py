"""
ASGI config for django_dummy_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django_dummy_app import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_dummy_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # This will handle traditional HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # Define the WebSocket routing from your app's routing.py
        )
    ),
})

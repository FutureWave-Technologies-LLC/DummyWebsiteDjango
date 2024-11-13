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
import django_dummy_project.routing  # Import the routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_dummy_project.settings')

application = ProtocolTypeRouter({
    # HTTP requests will use the default Django ASGI application
    "http": get_asgi_application(),

    # WebSocket requests will use the Channels application
    "websocket": AuthMiddlewareStack(
        URLRouter(
            django_dummy_project.routing.websocket_urlpatterns  # WebSocket URL patterns
        )
    ),
})

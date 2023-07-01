"""
ASGI config for clothing project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from clothing.apps.room import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        # 将WebSocket URL与对应的Consumer关联
        re_path(r'ws/barrage/(?P<room_name>.*)', consumers.Barrage.as_asgi()),
    ])
})
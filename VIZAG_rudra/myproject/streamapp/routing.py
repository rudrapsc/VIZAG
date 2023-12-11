# streamapp/routing.py
from django.urls import re_path
from .consumers import VideoConsumer

websocket_urlpatterns = [
    re_path(r'ws/stream/', VideoConsumer.as_asgi()),
]

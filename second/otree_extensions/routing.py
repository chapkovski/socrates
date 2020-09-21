from django.urls import re_path, path

from . import consumers

websocket_routes = [
    path('waitingroomprocessor/<int:player_pk>', consumers.WPConsumer),
]

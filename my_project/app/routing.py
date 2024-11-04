from django.urls import path
from . import consumers  # Make sure consumers are in the same app

websocket_urlpatterns = [
    path('ws/sc/', consumers.MySyncConsumer.as_asgi()),  # Sync Consumer
    path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),  # Async Consumer
]

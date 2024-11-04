from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})
        print("WebSocket connected")

    def websocket_receive(self, event):
        print("Message received:", event.get('text'))

    def websocket_disconnect(self, event):
        print("WebSocket disconnected")


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        print("WebSocket connected")

    async def websocket_receive(self, event):
        print("Message received:", event.get('text'))

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected")
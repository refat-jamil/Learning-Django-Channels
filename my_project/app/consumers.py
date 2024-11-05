from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})
        print("WebSocket connected", event)

    def websocket_receive(self, event):
        print("Message received:", event)
        self.send({
                "type": "websocket.send",
                "text": "Hi, My friend!",
            })

    def websocket_disconnect(self, event):
        print("WebSocket disconnected", event)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        print("WebSocket connected")

    async def websocket_receive(self, event):
        print("Message received:", event.get('text'))
        await self.send(
            {
                "type": "websocket.send",
                "text": "Hi, My friend!"
            }
        )

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected")
        raise StopConsumer()
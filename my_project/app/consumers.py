from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import time
import asyncio
import json

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})
        print("WebSocket connected", event)

    def websocket_receive(self, event):
        print("Message received:", event['text'])

        for i in range(10):
            self.send({
                'type':'websocket.send',
                'text': json.dumps({"count":i})
            })
            time.sleep(1)

    def websocket_disconnect(self, event):
        print("WebSocket disconnected", event)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        print("WebSocket connected")

    async def websocket_receive(self, event):
        print("Message received:", event.get('text'))
        for i in range(10):
            await self.send({
                'type':'websocket.send',
                'text': str(i)
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected")
        raise StopConsumer()
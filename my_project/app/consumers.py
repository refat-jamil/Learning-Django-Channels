from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import json
import asyncio
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        # Accept the WebSocket connection
        self.send({"type": "websocket.accept"})
        print("WebSocket connected", event)

        # Check for channel layer availability
        if self.channel_layer:
            # Add this channel to the "Programmers" group
            async_to_sync(self.channel_layer.group_add)("Programmers", self.channel_name)
            print("Channel Layer connected:", self.channel_layer)
            print("Channel Name:", self.channel_name)
        else:
            print("Channel layer is not configured.")

    def websocket_receive(self, event):
        print("Message received:", event['text'])
        # Check for channel layer availability
        if self.channel_layer:
            # Send the received message to the "Programmers" group
            async_to_sync(self.channel_layer.group_send)(
                "Programmers",
                {
                    "type": "chat.message",
                    "message": event["text"]
                }
            )

    def chat_message(self, event):
        print(event["message"])
        # Send the message to WebSocket
        self.send({
            "type": "websocket.send",
            "text": event["message"]
        })

    def websocket_disconnect(self, event):
        print("WebSocket disconnected", event)
        # Check for channel layer availability
        if self.channel_layer:
            # Remove the channel from the "Programmers" group
            async_to_sync(self.channel_layer.group_discard)("Programmers", self.channel_name)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # Accept the WebSocket connection
        await self.send({"type": "websocket.accept"})
        print("WebSocket connected")

    async def websocket_receive(self, event):
        print("Message received:", event.get("text"))
        # Send a count from 0 to 19 with a delay
        for i in range(20):
            await self.send({
                "type": "websocket.send",
                "text": json.dumps({"count": i})
            })
            await asyncio.sleep(1)  # Asynchronous sleep

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected")
        raise StopConsumer()

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

# Sync Consumer handling WebSocket connections
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})
        print("WebSocket connected:", event)

        if self.channel_layer:
            # Join the "Programmers" group
            self.channel_layer.group_add("Programmers", self.channel_name)
            print("Connected to channel layer with channel name:", self.channel_name)

    def websocket_receive(self, event):
        print("Received message:", event['text'])
        
        if self.channel_layer:
            # Broadcast message to "Programmers" group
            self.channel_layer.group_send(
                "Programmers",
                {"type": "chat.message", "message": event["text"]}
            )

    def chat_message(self, event):
        print("Broadcasting message:", event["message"])
        # Send message back to WebSocket client
        self.send({
            "type": "websocket.send",
            "text": event["message"]
        })

    def websocket_disconnect(self, event):
        print("WebSocket disconnected:", event)
        
        if self.channel_layer:
            # Leave the "Programmers" group
            self.channel_layer.group_discard("Programmers", self.channel_name)

        raise StopConsumer()


# Async Consumer handling WebSocket connections
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        
        if self.channel_layer:
            # Join the group dynamically based on the group name
            await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def websocket_receive(self, event):
        if self.channel_layer:
            # Send the received message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "chat.message", "message": event.get("text", "")}
            )

    async def chat_message(self, event):
        # Send the message to the WebSocket client
        await self.send({
            "type": "websocket.send",
            "text": event["message"],
        })

    async def websocket_disconnect(self, event):
        if self.channel_layer:
            # Remove the client from the group
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

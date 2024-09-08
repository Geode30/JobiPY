import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['current_user']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'current_user': user
            }
        )

    async def chat_message(self, event):
        message = event['message']
        current_user = event['current_user']

        await self.send(text_data=json.dumps({
            'message': message,
            'current_user': current_user
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.group_id = f'notif_{self.id}'

        await self.channel_layer.group_add(
            self.group_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_id,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notif = text_data_json['notif']

        await self.channel_layer.group_send(
            self.group_id,
            {
                'type': 'send_notif',
                'notif': notif
            }
        )

    async def send_notif(self, event):
        notif = event['notif']

        await self.send(text_data=json.dumps({
            'notif': notif
        }))

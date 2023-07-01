import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django_redis import get_redis_connection


class Barrage(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        conn = get_redis_connection("default")
        conn.incr(room_name)  # 将值加1
        print(conn.get(room_name))
        # 根据room_id判断应该连接到哪个WebSocket组
        if room_name == 'S姐直播间':
            await self.channel_layer.group_add('barrage_group_1', self.channel_name)
        elif room_name == '悦仓直播间':
            await self.channel_layer.group_add('barrage_group_2', self.channel_name)
        elif room_name == '星露直播间':
            await self.channel_layer.group_add('barrage_group_3', self.channel_name)
        else:
            return

        await self.accept()

    async def disconnect(self, close_code):
        room_name = self.scope['url_route']['kwargs']['room_name']
        conn = get_redis_connection("default")
        conn.decr(room_name)  # 将值减1

        # 根据room_id判断应该从哪个WebSocket组中移除连接
        if room_name == 'S姐直播间':
            await self.channel_layer.group_discard('barrage_group_1', self.channel_name)
        elif room_name == '悦仓直播间':
            await self.channel_layer.group_discard('barrage_group_2', self.channel_name)
        elif room_name == '星露直播间':
            await self.channel_layer.group_discard('barrage_group_3', self.channel_name)

    async def receive(self, text_data):
        # 当从Websocket接收到消息时调用
        pass

    async def send_comment(self, event):
        # 从Channels层接收到消息时调用
        content = event['content']

        # 发送消息到Websocket
        await self.send(text_data=json.dumps({
            'content': content
        }))

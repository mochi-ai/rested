from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def signal(user, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'signals.{user.id}', {'type': 'forward', 'data': data})

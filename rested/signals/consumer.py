from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.http import AsgiRequest
from channels.exceptions import DenyConnection
from django.contrib.auth import get_user
from django.utils.module_loading import import_string
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from channels.layers import get_channel_layer


# websocket signal consumer
class SignalConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None
        self.user = None

    def secure(self):
        # use django middleware to get session and authenticate on initial ws connection
        django_middlewhere = [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            # need to check csrf but unable to set that in the http request initiating ws, probably set it in query
        ]

        # build a django request from ws request/scope
        self.scope['method'] = 'WEBSOCKET'
        request = AsgiRequest(self.scope, '')

        # get channel's django middleware
        middleware = [import_string(m)(lambda x: None) for m in django_middlewhere]

        # make sure ws request passes channel's django middleware
        for m in middleware:
            if m.process_request(request): raise DenyConnection()

        # set session and user
        if hasattr(request, 'session'): self.session = request.session
        if hasattr(request, 'user'): self.user = request.user

        # deny if we don't have a session and an authenticated user
        if not self.session or not self.user or not self.user.is_authenticated:
            raise DenyConnection()

    def connect(self):
        self.secure()
        self.accept()
        async_to_sync(self.channel_layer.group_add)(f'signals.{self.user.id}', self.channel_name)

    def disconnect(self, _):
        async_to_sync(self.channel_layer.group_discard)(f'signals.{self.user.id}', self.channel_name)

    # when data is sent a heart beat request respond with empty object
    def receive_json(self, _):
        self.send_json({})

    def forward(self, event):
        # could reload user from session and check is_authenticated
        self.send_json({'data': event['data']})

    def check_session(self, data):
        # could also check session still exists in store self.session.load()
        if data['session_key'] == self.session.session_key:
            self.disconnect('Expired Session')


# when a user logged out disconnect websockets with the now invalidated session
@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    channel_layer = get_channel_layer()
    if not user or not request.session: return
    session_key = request.session.session_key
    if not channel_layer: return
    async_to_sync(channel_layer.group_send)(f'signals.{user.id}', {
        'type': 'check_session',
        'session_key': session_key
    })

# chat/consumers.py
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.http import AsgiRequest
from channels.exceptions import DenyConnection
from django.utils.module_loading import import_string


class SignalConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init(*args, **kwargs)
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

        # if session or user are set store on consumer
        if hasattr(request, 'session'): self.session = request.session
        if hasattr(request, 'user'): self.user = request.user

    def connect(self):
        self.secure()
        self.accept()
        async_to_sync(self.channel_layer.group_add)('signals', self.channel_name)

    def disconnect(self, _):
        async_to_sync(self.channel_layer.group_discard)('signals', self.channel_name)

    def forward(self, event):
        # could reload user from session and check is_authenticated
        self.send_json({'message': event['data']})

    def receive_json(self, data):
        message = data['message']
        self.send_json({'message': message})

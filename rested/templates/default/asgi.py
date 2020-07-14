import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from api import urls
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter(urls.websocketpatterns),
})

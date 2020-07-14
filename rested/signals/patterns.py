from django.urls import path
from rested.signals import SignalConsumer

patterns = [
    path(r'ws/signals', SignalConsumer),
]

import os
import django
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = False
    django.setup('example.settings')

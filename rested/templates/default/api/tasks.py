# Create your tasks here
from __future__ import absolute_import, unicode_literals
from rested.worker import task, scheduled_task


@scheduled_task(1)
def hello():
    print('hello')

@scheduled_task(2)
def goodbye():
    print('goodbye')

@task
def add(x, y):
    print('celery', x + y)
    return x + y

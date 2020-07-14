from django.shortcuts import redirect
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rested import signal
from . import tasks


@csrf_exempt
def index(request):
    print(User.objects.all())
    return redirect('/static/index.html')

@csrf_exempt
def ping(request):
    tasks.add.delay(1, 2)
    return {'data': 'pong'}

@csrf_exempt
def login(request):
    user = User.objects.filter(username='john').first()
    print(user)
    auth.login(request, user)
    return {}

@csrf_exempt
def logout(request):
    auth.logout(request)
    return {}

@csrf_exempt
def message(request):
    signal(request.user, request.data['message'])
    return {'message': request.data['message']}

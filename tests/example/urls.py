from django.contrib import admin
from django.urls import include, path
from rested import rest, authorize, errors
from rested.patterns import *
from functools import wraps
from . import views

def overwriter(overwrite):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            kwargs['count'] = overwrite
            return f(*args, **kwargs)
        return wrapper
    return decorator

urlpatterns = [
    path('index', views.index, name='index'),
]

restpatterns = [
    rest("^ab?$", "get", views.get, pattern='regex'),

    rest("params", "get", views.echo_params),
    rest("params", "post", views.echo_params),
    rest("params", "put", views.echo_params),
    rest("params", "delete", views.echo_params),

    rest("people/<int:id>", "get", views.people_get),
    rest("people", "get", views.people_index),

    rest("data", "get", views.echo_data),
    rest("data", "post", views.echo_data),
    rest("data", "put", views.echo_data),
    rest("data", "delete", views.echo_data),

    rest("okay", "get", views.get),
    rest("okay", "post", views.post),
    rest("okay", "put", views.put),
    rest("okay", "delete", views.delete),

    rest("dupe", "get", views.dupe, kwargs={"count": 1}),
    rest("dupe", "get", views.dupe, kwargs={"count": 2}),

    rest("decorated", "get", views.dupe, overwriter(7)),
    rest("decoratedx2", "get", views.dupe, [overwriter(9), overwriter(8)]),

    rest("boom", "get", views.boom),
    rest("bang", "get", views.bang),
    rest("kaboom", "get", views.kaboom),
    rest("status", "get", views.status),

    rest("auth/public", "get", views.get, authorize.public),
    rest("auth/authenticated", "get", views.get, authorize.authenticated),
    rest("auth/admin", "get", views.get, authorize.admin),
    rest("auth/staff", "get", views.get, authorize.staff),

    rest("insecure", "get", views.insecure),
    rest("csrf", "post", views.csrf),

    rest("vecho", "post", views.vecho),
    rest("vquery", "get", views.vquery),
    rest("vpurl/<int:num>", "get", views.vpurl)
]

from rested import json
from importlib import import_module
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models.query import QuerySet
from functools import lru_cache
from .errors import AbortException


class RestURLPattern:
    def __init__(self, method):
        # get default configuration module
        urlconf = import_module(settings.ROOT_URLCONF)

        # clone url config
        for x in dir(urlconf):
            setattr(self, x, getattr(urlconf, x))

        # copy url patterns and rest patterns that match method (create method scoped urlconf)
        regular_patterns = getattr(urlconf, "urlpatterns", [])
        rest_patterns = [p for p in getattr(urlconf, "restpatterns", []) if p.pattern.method == method.lower()]
        self.urlpatterns = regular_patterns + rest_patterns


@lru_cache(maxsize=None)
def scoped_url_patterns(method):
    return RestURLPattern(method)

def attach_data(request):
    if 'application/json' in request.META.get('CONTENT_TYPE', []):
        try:
            return json.loads(request.body.decode())
        except json.sjson.decoder.JSONDecodeError:
            return {}
    else:
        return {k:request.POST[k] for k in request.POST}

def attach_params(request):
    return {k:request.GET[k] for k in request.GET}

def wrap_response(response):
    # if response is a tuple, then someone is return (status, data), otherwise assume data and implied 200 status
    if isinstance(response, tuple):
        status, data = response
    else:
        status, data = (200, response)

    # convert data and status into json response
    if isinstance(data, HttpResponse):
        return data
    if isinstance(data, dict):
        return JsonResponse(data, status=status, encoder=json.RestedJSONEncoder)
    if hasattr(data, 'to_dict'):
        return JsonResponse(data.to_dict(), status=status, encoder=json.RestedJSONEncoder)
    if isinstance(data, QuerySet):
        return JsonResponse({m.id: m.to_dict() for m in data}, status=status, encoder=json.RestedJSONEncoder)
    return JsonResponse(data, status=status, encoder=json.RestedJSONEncoder)


class RestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.data = attach_data(request)
        request.params = attach_params(request)
        request.urlconf = scoped_url_patterns(request.method)
        response = self.get_response(request)
        return wrap_response(response)

    def process_exception(self, request, exception):
        if type(exception) is AbortException:
            return (exception.status, exception.data)
        return None

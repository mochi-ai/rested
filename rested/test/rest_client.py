from urllib.parse import urlencode
from rested import json
from django.test import Client


class RestClient(Client):

    def get(self, url, params=None, **extra):
        params = '?' + urlencode(params) if params else ''
        response = super().get(url + params, **extra)
        response.data = response.json()
        response.status = response.status_code
        return response

    def put(self, url, data=None, params=None, json_content=True, **extra):
        params = '?' + urlencode(params) if params else ''
        if json_content:
            response = super().put(url + params, json.dumps(data), content_type="application/json", **extra)
        else:
            response = super().put(url + params, data, **extra)
        response.data = response.json()
        response.status = response.status_code
        return response

    def post(self, url, data=None, params=None, json_content=True, **extra):
        params = '?' + urlencode(params) if params else ''
        if json_content:
            response = super().post(url + params, json.dumps(data), content_type="application/json", **extra)
        else:
            response = super().post(url + params, data, **extra)
        response.data = response.json()
        response.status = response.status_code
        return response

    def delete(self, url, params=None, **extra):
        params = '?' + urlencode(params) if params else ''
        response = super().delete(url + params, **extra)
        response.data = response.json()
        response.status = response.status_code
        return response

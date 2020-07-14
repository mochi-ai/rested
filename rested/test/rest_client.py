from urllib.parse import urlencode
from rested import json
from django.test import Client


class RestClient(Client):

    def get(self, url, params=None):
        params = '?' + urlencode(params) if params else ''
        response = super().get(url + params)
        response.data = response.json()
        response.status = response.status_code
        return response

    def put(self, url, data=None, params=None, json_content=True):
        params = '?' + urlencode(params) if params else ''
        if json_content:
            response = super().put(url + params, json.dumps(data), content_type="application/json")
        else:
            response = super().put(url + params, data)
        response.data = response.json()
        response.status = response.status_code
        return response

    def post(self, url, data=None, params=None, json_content=True):
        params = '?' + urlencode(params) if params else ''
        if json_content:
            response = super().post(url + params, json.dumps(data), content_type="application/json")
        else:
            response = super().post(url + params, data)
        response.data = response.json()
        response.status = response.status_code
        return response

    def delete(self, url, params=None):
        params = '?' + urlencode(params) if params else ''
        response = super().delete(url + params)
        response.data = response.json()
        response.status = response.status_code
        return response

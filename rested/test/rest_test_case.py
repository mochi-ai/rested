from urllib.parse import urlencode
from django.test import TestCase
from rested import json

class RestTestCase(TestCase):

    def get(self, url, params=None):
        params = '?' + urlencode(params) if params else ''
        response = self.client.get(url + params)
        response.data = response.json()
        response.status = response.status_code
        return response

    def put(self, url, data=None, params=None):
        params = '?' + urlencode(params) if params else ''
        response = self.client.put(url + params, json.dumps(data), content_type="application/json")
        response.data = response.json()
        response.status = response.status_code
        return response

    def post(self, url, data=None, params=None):
        params = '?' + urlencode(params) if params else ''
        response = self.client.post(url + params, json.dumps(data), content_type="application/json")
        response.data = response.json()
        response.status = response.status_code
        return response

    def delete(self, url, params=None):
        params = '?' + urlencode(params) if params else ''
        response = self.client.delete(url + params)
        response.data = response.json()
        response.status = response.status_code
        return response

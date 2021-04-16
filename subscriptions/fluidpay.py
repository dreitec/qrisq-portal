import requests
import json

from django.conf import settings
from rest_framework.response import Response


class FluidPay(object):

    def __init__(self):
        self.api_key = settings.FLUID_PAY_API_KEY

    def request_handler(self, req_method, params, body={}):
        url_sandbox = settings.FLUID_PAY_SANDBOX_URL
        url = f"{url_sandbox}/{'/'.join(params)}"
        print(url)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'credentials': 'include',
            'Authorization': self.api_key
        }
        if req_method == 'GET':
            results = requests.get(url, headers=headers)
            print('get->', results.text)
        elif req_method == 'POST':
            print('request body->>', body)
            results = requests.post(url, data=body, headers=headers)
            print('post->', results.text)
        elif req_method == 'DELETE':
            print('delete')
            results = requests.delete(url, data=body, headers=headers)
            print('delete->', results)
        print(type(results))
        print(results.status_code)
        if results.status_code == 200:
            return results.json()
        else:
            return Response({'error': "error"})

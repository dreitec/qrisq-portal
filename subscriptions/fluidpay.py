import requests
import json

from django.conf import settings
from rest_framework.response import Response


class FluidPay(object):

    def __init__(self):
        self.api_key = settings.FLUID_PAY_API_KEY
        if settings.FLUIDPAY_TEST:
            self.main_url = settings.FLUID_PAY_SANDBOX_URL
        else:
            self.main_url = settings.FLUID_PAY_PRODUCTION_URL

    def request_handler(self, req_method, params, body={}):
        url = f"{self.main_url}/{'/'.join(params)}"
        print(url)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'credentials': 'include',
            'Authorization': self.api_key
        }
        if req_method == 'GET':
            return requests.get(url, headers=headers)
        elif req_method == 'POST':
            return requests.post(url, data=body, headers=headers)
        elif req_method == 'DELETE':
            return requests.delete(url, data=body, headers=headers)

import sys 
from urllib.parse import quote

from django.conf import settings

from paypalcheckoutsdk.core import SandboxEnvironment, LiveEnvironment, PayPalHttpClient


def paypal_client():
    '''
    Method to select the paypal environment and return paypal client
    '''
    if settings.PAYPAL_TEST:
        environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_KEY)
    else:
        environment = LiveEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_KEY)
    
    return PayPalHttpClient(environment)


class OrderApproveRequest:
    """
    Approve an order, by ID.
    """
    def __init__(self, order_id):
        self.verb = "GET"
        self.path = "/checkoutnow?token={order_id}".replace("{order_id}", quote(str(order_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None

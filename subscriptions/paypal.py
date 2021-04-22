import sys 
from urllib.parse import quote

from django.conf import settings

from paypalcheckoutsdk.core import SandboxEnvironment, LiveEnvironment, PayPalHttpClient
from paypalcheckoutsdk.payments import CapturesGetRequest, CapturesRefundRequest
from paypalhttp.http_error import HttpError

from subscriptions.models import PaymentRefund


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


def paypal_refund_payment(payment_id, payment_gateway, user):
    client = paypal_client()
    try:
        request = CapturesRefundRequest(payment_id)
        response = client.execute(request)
        refund_transaction_id = response.result.id
    except HttpError as err:
        raise err

    PaymentRefund.objects.create(user=user, payment_id=payment_id, payment_gateway=payment_gateway, refund_transaction_id=refund_transaction_id)


class PayPal:
    def __init__(self):
        if settings.PAYPAL_TEST:
            self.environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_KEY)
        else:
            self.environment = LiveEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_KEY)
    
    def paypal_client():
        return PayPalHttpClient(self.environment)
    
    def refund_payment(payment_id, payment_gateway, user):
        client = paypal_client()
        try:
            request = CapturesRefundRequest(payment_id)
            response = client.execute(request)
            refund_transaction_id = response.result.id
        except HttpError as err:
            raise err

        PaymentRefund.objects.create(user=user, payment_id=payment_id, payment_gateway=payment_gateway, refund_transaction_id=refund_transaction_id)
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from paypalcheckoutsdk.core import SandboxEnvironment, LiveEnvironment, PayPalHttpClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

# from paypalhttp.http_client import HttpClient


def _paypal_client():
    '''
    Method to select the paypal environment and return paypal client
    '''
    if settings.PAYPAL_TEST:
        environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_KEY)
    else:
        environment = LiveEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_SECRET_KEY)
    
    return PayPalHttpClient(environment)


@api_view(["POST"])
def create_order(request):
    client = _paypal_client()

    print("--- CLIENT ---")
    print(client)

    create_order = OrdersCreateRequest()
    # billing
    create_order.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "5.00",
            }
        }]
    })
    # try:
    response = client.execute(create_order)
    print("---  Response ---")
    print(response.result._dict)
    print(response.status_code)
    return Response(response.result._dict)
        
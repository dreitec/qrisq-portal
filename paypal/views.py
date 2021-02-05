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
        "intent": 'CAPTURE',
        "payer": {
            "name": {
                "given_name": "PayPal",
                "surname": "Customer"
            },
            "address": {
                "address_line_1": '123 ABC Street',
                "address_line_2": 'Apt 2',
                "city": 'San Jose',
                "state": 'CA',
                "postal_code": '95121',
                "country_code": 'US'
            },
            "email_address": "customer@domain.com",
            "phone": {
            "phone_type": "MOBILE",
            "phone_number": {
                "national_number": "14082508100"
            }
            }
        },
        "purchase_units": [{
            "amount": {
                "value": '5.00',
                "currency_code": 'USD'
            },
        }]
    })
    # try:
    response = client.execute(create_order)
    return Response(response.result._dict)
        
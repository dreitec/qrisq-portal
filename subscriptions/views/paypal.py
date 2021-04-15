from django.conf import settings

import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest, OrdersGetRequest
from paypalcheckoutsdk.payments import CapturesGetRequest, CapturesRefundRequest
from paypalhttp.http_error import HttpError

from subscriptions.paypal import paypal_client, OrderApproveRequest
from subscriptions.models import PaymentRefund

@api_view(["POST"])
def create_order(request):
    client = paypal_client()
    order = OrdersCreateRequest()

    # billing
    order.request_body({
        "intent": 'Authorize',
        "payer": {
            "name": {
                "given_name": "Sumedh",
                "surname": "Shakya"
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
    response = client.execute(order)
    return Response(response.result._dict)


@api_view(["GET"])
def approve_order(request, order_id):
    client = paypal_client()
    approve = OrderApproveRequest(order_id)
    try:
        response = client.execute(approve)
    except requests.HTTPError as error:
        return Response(error.response)
    return Response(response.result._dict)


@api_view(["GET"])
def capture_order(request, order_id):
    client = paypal_client()
    capture = OrdersCaptureRequest(order_id)
    try:
        response = client.execute(capture)
    except requests.HTTPError as error:
        return Response(error.response)
    return Response(response.result._dict)


@api_view(["GET"])
def capture_detail(request, capture_id):
    client = paypal_client()
    capture = CapturesGetRequest(capture_id)
    try:
        response = client.execute(capture)
    except requests.HTTPError as error:
        return Response(error.response)
    return Response(response.result._dict)


@api_view(["POST"])
def refund_payment(request):
    client = paypal_client()
    capture = CapturesRefundRequest()
    try:
        response = client.execute(capture)
    except requests.HTTPError as error:
        return Response(error.response)
    return Response(response.result._dict)


def refund_order(payment_id, payment_gateway, user):
    if payment_gateway == 'paypal':
        client = paypal_client()
        try:
            request = CapturesRefundRequest(payment_id)
            response = client.execute(request)
            refund_transaction_id = response.result.id
        except HttpError as err:
            raise err

    PaymentRefund.objects.create(user=user, payment_id=payment_id, payment_gateway=payment_gateway, refund_transaction_id=refund_transaction_id)
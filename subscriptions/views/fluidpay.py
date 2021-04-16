import requests
import json

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from subscriptions.fluidpay import FluidPay


@api_view(["GET"])
def get_users(request):
    fp = FluidPay()
    users = fp.request_handler('GET', ['users'])  # get all users

    return Response(users)
    # client = paypal_client()
    # approve = OrderApproveRequest(order_id)
    # try:
    #     response = client.execute(approve)
    # except requests.HTTPError as error:
    #     return Response(error.response)
    # return Response(response.result._dict)


@api_view(["POST"])
def process_transaction(request):
    fp = FluidPay()
    transaction_data = {
        "processor_id": settings.FLUID_PAY_PROCESSOR_ID,
        "type": "sale",
        "amount": 1112,
        "tax_amount": 100,
        "shipping_amount": 100,
        "currency": "USD",
        "description": "test transaction",
        "order_id": "someOrderID",
        "po_number": "somePONumber",
        "ip_address": "4.2.2.2",
        "email_receipt": False,
        "email_address": "user@home.com",
        "create_vault_record": True,
        "payment_method": {
            "card": {
                "entry_type": "keyed",
                "number": "4012000098765439",
                "expiration_date": "12/21",
                "cvc": "999"
            }
        },
        "billing_address": {
            "first_name": "John",
            "last_name": "Smith",
            "company": "Test Company",
            "address_line_1": "123 Some St",
            "city": "Wheaton",
            "state": "IL",
            "postal_code": "60187",
            "country": "US",
            "phone": "5555555555",
            "fax": "5555555555",
            "email": "help@website.com"
        },
        "shipping_address": {
            "first_name": "John",
            "last_name": "Smith",
            "company": "Test Company",
            "address_line_1": "123 Some St",
            "city": "Wheaton",
            "state": "IL",
            "postal_code": "60187",
            "country": "US",
            "phone": "5555555555",
            "fax": "5555555555",
            "email": "help@website.com"
        }
    }
    transaction_json_data = json.dumps(transaction_data)
    transaction = fp.request_handler('POST', ['transaction'], body=transaction_json_data)  # handle transaction
    print('transaction', transaction)
    return Response({'message': "Transaction is success"})


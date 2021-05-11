import json
import logging

from django.conf import settings

from rest_framework import serializers

from core.validators import CARD_VALIDATOR, CVC_VALIDATOR, DATE_VALIDATOR, NUMERIC_VALIDATOR

from subscriptions.fluidpay_custom_exception import FluidPayCustomException
from subscriptions.fluidpay import FluidPay
from subscriptions.models import UserPayment, UserSubscription, SubscriptionPlan
from subscriptions.fluidpay_response_mapper import FLUIDPAY_RESPONSE

logger = logging.getLogger(__name__)


class FluidPayTransactionSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=60)
    last_name = serializers.CharField(max_length=60)
    card_number = serializers.CharField(max_length=16, validators=[CARD_VALIDATOR],
                                        error_messages={"required": "Enter card Number."})
    expiration_date = serializers.CharField(
        max_length=5, validators=[DATE_VALIDATOR],
        error_messages={"required": "Enter expiration date."}
    )
    cvc = serializers.CharField(max_length=4, validators=[CVC_VALIDATOR],
                                error_messages={"required": "Enter cvc number."})
    billing_address = serializers.CharField(max_length=99)
    city = serializers.CharField(max_length=50)
    state = serializers.CharField(max_length=30)
    zip_code = serializers.CharField(max_length=5, validators=[NUMERIC_VALIDATOR])
    amount = serializers.DecimalField(max_digits=8, decimal_places=2,
                                      error_messages={"required": "Enter amount."})

    def validate_expiration_date(self, date):
        year = date.split("/")[1]
        from datetime import datetime
        today_year = datetime.now().strftime("%y")
        if int(year) < int(today_year):
            print('error')
            raise serializers.ValidationError("Expired Card")
        return date

    def create(self, validated_data):
        user = self.context["request"].user
        amount = validated_data.pop('amount')
        transaction_data = {
            "processor_id": settings.FLUID_PAY_PROCESSOR_ID,
            "type": "sale",
            "amount": int(amount * 100),
            "tax_amount": 0,
            "shipping_amount": 0,
            "currency": "USD",
            "description": "test transaction",
            "email_receipt": True,
            "email_address": user.email,
            "create_vault_record": True,
            "payment_method": {
                "card": {
                    "entry_type": "keyed",
                    "number": validated_data.get('card_number'),
                    "expiration_date": validated_data.pop('expiration_date'),
                    "cvc": validated_data.pop('cvc'),
                }
            },
            "billing_address": {
                "first_name": validated_data.get("first_name"),
                "last_name": validated_data.get("last_name"),
                "address_line_1": validated_data.get("billing_address"),
                "city": validated_data.get("city"),
                "state": validated_data.get("state"),
                "postal_code": validated_data.get("zip_code"),
            },
        }

        try:
            logger.info("Processing transaction")
            transaction_json_data = json.dumps(transaction_data)
            
            fp = FluidPay()
            response = fp.request_handler('POST', ['transaction'], body=transaction_json_data)  # handle transaction

            if not response.status_code == 200:
                raise serializers.ValidationError({
                    **response.json()
                })

            transaction = response.json().get('data', {})
            transaction_code = transaction.get('response_code', 0)
            if transaction_code not in [100, 101, 110]:
                raise FluidPayCustomException({
                    'code': transaction_code,
                    **FLUIDPAY_RESPONSE[str(transaction_code)]
                })
            payment = UserPayment.objects.create(
                payment_id=transaction['id'],
                payment_gateway='fluidpay',
                user_id=user.id,
                price=amount,
            )

        except Exception as err:
            logger.warning(f"Failed User instance; Error: {str(err)}")
            raise err

        return payment

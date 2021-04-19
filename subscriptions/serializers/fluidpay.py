import json
import logging
from pprint import pprint

from django.conf import settings

from rest_framework import serializers
from django.core.validators import RegexValidator

from subscriptions.fluidpay_custom_exception import FluidPayCustomException
from subscriptions.fluidpay import FluidPay
from subscriptions.models import UserPayment, UserSubscription, SubscriptionPlan
from subscriptions.fluidpay_response import FLUIDPAY_RESPONSE

logger = logging.getLogger(__name__)

DATE_VALIDATOR = RegexValidator(r'^((0?[1-9]|[1][0-2])\/\d{2})', 'Invalid Expiration date format')
CARD_VALIDATOR = RegexValidator(r'(\d{16})', 'Only numeric characters')
CVC_VALIDATOR = RegexValidator(r'(\d{3,4})', 'Only numeric characters')


class FluidPayTransactionSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, validators=[CARD_VALIDATOR], error_messages={"required": "Enter card Number."})
    expiration_date = serializers.CharField(max_length=5, validators=[DATE_VALIDATOR], error_messages={"required": "Enter expiration date."})
    cvc = serializers.CharField(max_length=4, validators=[CVC_VALIDATOR], error_messages={"required": "Enter cvc number."})
    amount = serializers.DecimalField(max_digits=8, decimal_places=2,
                                      error_messages={"required": "Enter amount."})
    subscription_plan_id = serializers.IntegerField()

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
        card_number = validated_data.pop('card_number')
        expiration_date = validated_data.pop('expiration_date')
        cvc = validated_data.pop('cvc')
        amount = validated_data.pop('amount')
        subscription_plan_id = validated_data.pop('subscription_plan_id')

        try:
            logger.info("Processing transaction")
            fp = FluidPay()
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
                        "number": card_number,
                        "expiration_date": expiration_date,
                        "cvc": cvc
                    }
                },
            }

            transaction_json_data = json.dumps(transaction_data)
            response = fp.request_handler('POST', ['transaction'], body=transaction_json_data)  # handle transaction

            pprint(response.json())
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
            )
            subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
            UserSubscription.objects.create(
                user=user,
                plan=subscription_plan,
                recurring=False
            )

        except Exception as err:
            logger.warning(f"Failed User instance; Error: {str(err)}")
            raise err

        return payment

import logging
from rest_framework import serializers
from core.validators import CARD_VALIDATOR, CVC_VALIDATOR, DATE_VALIDATOR, NUMERIC_VALIDATOR

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
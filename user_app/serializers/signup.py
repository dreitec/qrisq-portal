from email.policy import default
import logging

from django.conf import settings
from django.db import transaction

from rest_framework import serializers

from subscriptions.models import UserSubscription, SubscriptionPlan, UserPayment
from user_app.models import User, UserProfile, NUMERIC_VALIDATOR
from user_app.utils import mail_sender

from .auth import LoginTokenSerializer

logger = logging.getLogger(__name__)


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    address = serializers.JSONField()
    address_line_1 = serializers.CharField(max_length=100)
    address_line_2 = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    street_number = serializers.CharField(max_length=30, required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(max_length=30)
    state = serializers.CharField(max_length=30)
    zip_code = serializers.CharField(max_length=5, validators=[NUMERIC_VALIDATOR])
    subscription_plan_id = serializers.IntegerField()

    def to_representation(self, instance=None):
        serializer = LoginTokenSerializer(data=self.validated_data, context=self.context)
        serializer.is_valid()
        return serializer.data

    def validate(self, data):
        error = {}
        if not data['password'] == data['confirm_password']:
            error['confirm_password'] = "Passwords didn't match."
        
        if User.objects.filter(email=data['email']).exists():
            error['email'] = "User with this email exists."

        address = data.get('address', {})
        if not ('lat' in address and 'lng' in address and 'displayText' in address):
            error['address'] = "Address information invalid. Please add 'lat', 'lng' and 'displayText' to address."

        if not SubscriptionPlan.objects.filter(id=data['subscription_plan_id']).exists():
            error['subscription_plan_id'] = "Subscription plan does not exists"
        
        if error:
            raise serializers.ValidationError(error)

        data.pop('confirm_password')
        return data

    @transaction.atomic()
    def create(self, validated_data):
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')
        subscription_plan_id = validated_data.pop('subscription_plan_id')
        
        try:
            logger.info("Creating User Instance for email " + email)
            user = User.objects.create_user(email=email, password=password,
                                            first_name=first_name, last_name=last_name)
            user_profile = UserProfile.objects.create(user=user, **validated_data)
            UserSubscription.objects.create(user=user, plan_id=subscription_plan_id)

        except Exception as err:
            logger.warning(f"FailNo Environmented User instance; Error: {str(err)}")
            raise err
        
        # Send user registration email
        # context = {
        #     'full_name': f"{first_name} {last_name}",
        #     'domain': settings.DOMAIN
        # }
        # try:
        #     mail_sender(
        #         template='user_app/registration_confirmation.html',
        #         context=context,
        #         subject="User Registered",
        #         recipient_list=[email]
        #     )
        # except Exception as error:
        #     logger.warning(f"Failed sending email to user; Error: {str(error)}")
        #     raise Exception("Error sending email to User.")
        
        logger.info(f"User {email} created successfully.")
        return user

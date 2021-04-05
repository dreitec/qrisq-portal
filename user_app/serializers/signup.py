import logging

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction

from rest_framework import serializers

from core.boto_client import send_message_to_sqs_queue
from subscriptions.models import UserSubscription, SubscriptionPlan, UserPayment

from user_app.models import User, UserProfile, NUMERIC_VALIDATOR
from user_app.utils import mail_sender

logger = logging.getLogger(__name__)


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    address = serializers.JSONField()
    street_number = serializers.CharField(max_length=30)
    city = serializers.CharField(max_length=30)
    state = serializers.CharField(max_length=30)
    zip_code = serializers.CharField(max_length=5, validators=[NUMERIC_VALIDATOR])
    subscription_plan_id = serializers.IntegerField()
    payment_id = serializers.CharField(max_length=30)
    payment_gateway = serializers.ChoiceField(choices = UserPayment.PAYMENT_CHOICES)

    def validate(self, data):
        error = {}
        if not data['password'] == data['confirm_password']:
            error['confirm_password'] = "Passwords didn't match."
        
        if User.objects.filter(email=data['email']).exists():
            error['email'] = "User with this email exists."
        
        if UserPayment.objects.filter(payment_id=data['payment_id']).exists():
            error['payment_id'] = "Payment ID exists."
        
        if not SubscriptionPlan.objects.filter(id=data['subscription_plan_id']).exists():
            error['subscription_plan_id'] = "Subscription plan does not exists"
        
        address = data.get('address', {})
        if not ('lat' in address and 'lng' in address and 'displayText' in address):
            error['address'] = "Address information invalid. Please add 'lat', 'lng' and 'displayText' to address."

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
        payment_id = validated_data.pop('payment_id')
        payment_gateway = validated_data.pop('payment_gateway')

        try:
            logger.info("Creating User Instance for email " + email)
            user = User.objects.create_user(email=email, password=password,
                                            first_name=first_name, last_name=last_name)
            user_profile = UserProfile.objects.create(user=user, **validated_data)

            UserSubscription.objects.create(user=user, plan_id=subscription_plan_id)
            UserPayment.objects.create(user=user, payment_id=payment_id, payment_gateway=payment_gateway)

        except Exception as err:
            logger.warn(f"Failed User instance; Error: {str(err)}")
            raise err

        try:
            send_message_to_sqs_queue(str(user.id), user_profile.address)
        except Exception as err:
            raise Exception("Error sending message to SQS queue.")
        
        context = {
            'full_name': f"{first_name} {last_name}",
            'domain': settings.DOMAIN
        }
        try:
            mail_sender(
                template='user_app/registration_confirmation.html',
                context=context,
                subject="User Registered",
                recipient_list=[email]
            )
        except Exception as error:
            logger.warn("Failed sending email to user; Error: {str(error)}")
            raise Exception("Error sending email to User.")
        
        logger.info(f"User {email} created successfully.")
        return user

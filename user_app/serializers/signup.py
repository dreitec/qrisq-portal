from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from user_app.models import User, UserProfile, NUMERIC_VALIDATOR
from user_app.utils import mail_sender
from subscriptions.models import UsersSubscription, SubscriptionPlan


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


    def validate(self, data):
        error = {}
        if not data['password'] == data['confirm_password']:
            error['confirm_password'] = "Passwords didn't match."
        
        if User.objects.filter(email=data['email']).exists():
            error['email'] = "User with this email exists."
        
        if not SubscriptionPlan.objects.filter(id=data['subscription_plan_id']).exists():
            error['subscription_plan_id'] = "Subscription plan does not exists"

        if error:
            raise serializers.ValidationError(error)

        data.pop('confirm_password')
        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')
        subscription_plan_id = validated_data.pop('subscription_plan_id')
        payment_id = validated_data.pop('payment_id')

        user = User.objects.create_user(email=email, password=password,
                                        **{"first_name": first_name, "last_name": last_name})

        UserProfile.objects.create(user=user, **validated_data)

        UsersSubscription.objects.create(user=user, plan_id=subscription_plan_id)

        return user

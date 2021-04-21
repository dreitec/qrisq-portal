import logging

from django.conf import settings
from django.db import transaction

from rest_framework import serializers
from user_app.models import User, UserProfile
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
        
        try:
            logger.info("Creating User Instance for email " + email)
            user = User.objects.create_user(email=email, password=password,
                                            first_name=first_name, last_name=last_name)
            UserProfile.objects.create(user=user, **validated_data)

        except Exception as err:
            logger.warning(f"Failed User instance; Error: {str(err)}")
            raise err
        
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
            logger.warning("Failed sending email to user; Error: {str(error)}")
            raise Exception("Error sending email to User.")
        
        logger.info(f"User {email} created successfully.")
        return user

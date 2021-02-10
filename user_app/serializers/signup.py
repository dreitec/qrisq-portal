from django.conf import settings
from rest_framework import serializers
from user_app.models import User, UserProfile
from user_app.utils import mail_sender


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    address = serializers.JSONField()

    def validate(self, data):
        error = {}
        if not data['password'] == data['confirm_password']:
            error['password_confirmation'] = "Passwords didn't match."
        
        if User.objects.filter(email=data['email']).exists():
            error['email'] = "User with this email exists."
        
        if error:
            raise serializers.ValidationError(error)
        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')

        profile = {
            "phone_number": validated_data.pop('phone_number'),
            "address": validated_data.pop('address')
        }

        user = User.objects.create_user(email=email,
                                        password=validated_data.pop('password'),
                                        **validated_data)

        UserProfile.objects.create(user=user, **profile)

        # send email confirmation to user
        context = {
            'email': email,
            'full_name': first_name + ' ' + last_name,
            'password': password,
            'logo_url': "https://qrisq.com/wp-content/uploads/2020/10/QRISQ-logo-3D-white.png"
        }
        try:
            mail_sender(
                template='user_app/registration_confirmation.html',
                context=context,
                subject="User Registered",
                recipient_list=[email]
            )
        except Exception as error:
            print(str(error))

        return user

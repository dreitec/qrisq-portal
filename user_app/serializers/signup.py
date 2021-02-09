from django.conf import settings
from rest_framework import serializers
from user_app.models import User
from user_app.utils import mail_sender


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

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

        # send email confirmation to user
        context = {
            'email': email,
            'full_name': first_name + ' ' + last_name,
            'password': password,
            'logo_url': 'localhost:8000/static/images/logo.png'
        }
        try:
            mail_sender(
                template='user_app/registration_confirmation.html',
                context=context,
                subject="User Registered",
                recipient_list=[email]
            )
        except Exception as error:
            pass

        return User.objects.create_user(email=email,
                                        password=validated_data.pop('password'),
                                        **validated_data)

from django.conf import settings
from rest_framework import serializers
from user_app.models import User
# from user_app.utils import mail_sender


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    full_name = serializers.CharField(max_length=60, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, data):
        error = {}
        if not data['password'] == data['confirm_password']:
            error['password_confirmation'] = "Passwords didn't match."
        
        if User.objects.filter(username=data['username']).exists():
            error['username'] = "User with this username exists."
        
        if User.objects.filter(email=data['email']).exists():
            error['email'] = "User with this email exists."
        
        if error:
            raise serializers.ValidationError(error)
        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        return User.objects.create_user(username=validated_data.pop('username'),
                                        email=email,
                                        password=validated_data.pop('password'),
                                        **validated_data)

        # send email confirmation to user
        # context = {
        #     'email': email,
        # }
        # try:
        #     mail_sender(
        #         template='user_app/register_confirmation.html',
        #         context=context,
        #         subject="User Registered",
        #         recipient_list=[email]
        #     )
        # except Exception as error:
        #     pass

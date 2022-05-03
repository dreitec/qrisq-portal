from datetime import datetime
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from subscriptions.serializers import UserSubscriptionSerializer
import dateutil.parser
from .user import UserSerializer
import logging


class LoginTokenSerializer(TokenObtainPairSerializer):

    def to_representation(self, instance):
        user = self.user
        response = self.validated_data
        response['user'] = UserSerializer(user).data
        subscribed_plan = getattr(user, "subscription_plan", None)
        user_subscription = UserSubscriptionSerializer(subscribed_plan).data
        response['user']['subscription'] = user_subscription

        has_paid = False
        payment_expired = False
        if user_subscription is not None:
            payment_expired = user_subscription["expires_at"] is None or dateutil.parser.isoparse(user_subscription["expires_at"]).timestamp() <= datetime.now().timestamp()
            has_paid = not payment_expired

        response['user']['has_paid'] = has_paid
        response['user']['payment_expired'] = payment_expired
        return response


class RefreshTokenSerializer(TokenRefreshSerializer):
    def save(self):
        refresh = self.context['request'].data.get('refresh', '')
        RefreshToken(refresh).blacklist()


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate(self, data):
        if not data['new_password'] == data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': ["Passwords didn't match."]})

        import re
        if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[!@#$%^&*_+=\\<>?,./-]).{12,}$",
                        data['new_password']):
            raise serializers.ValidationError(
                {'password': [
                    "Password must contain at least 12 characters with one number and one special character."
                ]})
        return data

    def create(self, validated_data):
        user = self.context['user']
        user.set_password(validated_data['new_password'])
        user.save()
        return True

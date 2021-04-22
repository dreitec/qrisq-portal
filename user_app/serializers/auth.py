from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from subscriptions.serializers import UserSubscriptionSerializer
from .user import UserSerializer


class LoginTokenSerializer(TokenObtainPairSerializer):

    def to_representation(self, instance):
        response = self.validated_data
        response['user'] = UserSerializer(self.user).data
        subscribed_plan = getattr(self.user, "subscription_plan", None)
        response['user']['subscription'] = UserSubscriptionSerializer(subscribed_plan).data
        response['user']['has_paid'] = self.user.payment.last() and not subscribed_plan.is_cancelled
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
        if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[!@#$%^&*_+=\\<>?,./-]).{8,}$",
                        data['new_password']):
            raise serializers.ValidationError(
                {'password': [
                    "Password must contain at least 8 characters with one number and one special character."
                ]})
        return data

    def create(self, validated_data):
        user = self.context['user']
        user.set_password(validated_data['new_password'])
        user.save()
        return True

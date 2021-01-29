from django.utils.text import gettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .user import UserSerializer


class LoginTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        return super().validate(attrs)
        

class RefreshTokenSerializer(TokenRefreshSerializer):
    def save(self):
        refresh = self.context['request'].data.get('refresh', '')
        RefreshToken(refresh).blacklist()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate(self, data):
        if not data['new_password'] == data['confirm_password']:
            raise serializers.ValidationError({'password_confirmation': ["Passwords didn't match."]})

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

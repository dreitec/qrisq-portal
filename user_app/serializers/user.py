from django.contrib.auth.hashers import check_password
from django.db import transaction

from rest_framework import serializers

from user_app.models import User, UserProfile
from subscriptions.serializers import UserSubscriptionSerializer


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class _UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('id', 'user')
        read_only_fields = ('address_updated',)


class UserBasicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    profile = _UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_admin', 'profile')
        extra_kwargs = {
            'email': {'required': False},
            'is_admin': {'read_only': True}
        }

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile', {})
        if instance.is_admin:
            UserProfile.objects.update_or_create(user=instance, defaults=profile)
        else:
            user_profile = instance.profile
            user_profile.phone_number = profile["phone_number"]
            user_profile.save()
        return super().update(instance, validated_data)


class ClientUserSerializer(serializers.ModelSerializer):
    profile = _UserProfileSerializer()
    subscription_plan = UserSubscriptionSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'profile', 'subscription_plan')


class _EmailUpdateSerializer(serializers.Serializer):
    current_email = serializers.EmailField()
    new_email = serializers.EmailField()
    confirm_email = serializers.EmailField()

    def validate(self, data):
        error = {}
        user = self.context['request'].user

        if not data['new_email'] == data['confirm_email']:
            error['confirm_email'] = "Emails didn't match."

        if User.objects.exclude(id=user.id).filter(email=data['new_email']).exists():
            error['new_email'] = "User with this email exists."

        if not user.email == data['current_email']:
            error['current_email'] = "Current email didn't match."
        
        if error:
            raise serializers.ValidationError(error)

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user.email = validated_data.get('new_email')
        user.save()
        return user


class _PhoneUpdateSerializer(serializers.Serializer):
    current_phone = serializers.CharField(max_length=15)
    new_phone = serializers.CharField(max_length=15)
    confirm_phone = serializers.CharField(max_length=15)

    def validate(self, data):
        error = {}
        if not data['new_phone'] == data['confirm_phone']:
            error['confirm_phone'] = "Phone numbers didn't match."

        if not self.context['request'].user.profile.phone_number == data['current_phone']:
            error['current_phone'] = "Current phone number didn't match."

        if error:
            raise serializers.ValidationError(error)

        return data

    def create(self, validated_data):
        profile = self.context['request'].user.profile
        profile.phone_number = validated_data.get('new_phone')
        profile.save()
        return profile


class _PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def validate(self, data):
        error = {}
        user = self.context['request'].user

        if not data['new_password'] == data['confirm_password']:
            error['confirm_password'] = "Passwords didn't match."

        import re
        if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[!@#$%^&*_+=\\<>?,./-]).{8,}$",
                        data['new_password']):
            error['new_password'] = "Password must contain at least 8 characters with one number and one special character."
        
        if not check_password(data['old_password'], user.password):
            error['old_password'] = "Invalid old password."

        if error:
            raise serializers.ValidationError(error)

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class AccountProfileSerializer(serializers.Serializer):
    email = _EmailUpdateSerializer(allow_null=True)
    phone_number = _PhoneUpdateSerializer(allow_null=True)
    password = _PasswordUpdateSerializer(allow_null=True)

    @transaction.atomic()
    def create(self, validated_data):
        if validated_data.get('email'):
            user = _EmailUpdateSerializer(context=self.context).create(validated_data.pop('email'))
        
        if validated_data.get('phone_number'):
            user = _PhoneUpdateSerializer(context=self.context).create(validated_data.pop('phone_number'))

        if validated_data.get('password'):
            user = _PasswordUpdateSerializer(context=self.context).create(validated_data.pop('password'))
        return user

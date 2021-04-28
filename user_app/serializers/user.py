from rest_framework import serializers

from user_app.models import User, UserProfile
from subscriptions.serializers import UserSubscriptionSerializer


class _UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('id', 'user')


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
        fields = ('id', 'email', 'first_name', 'last_name', 'profile')
        extra_kwargs = {
            'email': {'required': False}
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


class UpdateUserInfoSerializer(serializers.Serializer):
    old_email = serializers.EmailField(required=False, allow_blank=True)
    new_email = serializers.EmailField(required=False,  allow_blank=True)
    confirm_new_email = serializers.EmailField(required=False, allow_blank=True)
    old_phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    new_phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    confirm_new_phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    
    def validate(self, data):
        error = {}
        
        if data['old_email'] != '' or data['new_email'] != '':
            if not data['new_email'] == data['confirm_new_email']:
                error['confirm_new_email'] = "Emails didn't match."

            if User.objects.filter(email=data['new_email']).exists():
                error['new_email'] = "User with this email exists."

            if data['new_email'] == '':
                error['new_email'] = "This field is required."

            if not self.context['request'].user.email == data['old_email']:
                error['old_email'] = "Old email didn't match."

        if data['old_phone_number'] != '' or data['new_phone_number'] != '':
            if not data['new_phone_number'] == data['confirm_new_phone_number']:
                error['confirm_new_phone_number'] = "Phone numbers didn't match."

            if not self.context['request'].user.profile.phone_number == data['old_phone_number']:
                error['old_phone_number'] = "Old phone number didn't match."

            if data['new_phone_number'] == '':
                error['new_phone_number'] = "This field is required."

        if error:
            raise serializers.ValidationError(error)

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        
        if validated_data.get('old_email') is not '':
            user.email = validated_data.get('new_email')
            user.save()
        
        if validated_data.get('old_phone_number') is not '':
            user.profile.phone_number = validated_data.get('new_phone_number')
            user.profile.save()
        
        return validated_data
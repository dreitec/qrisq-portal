from rest_framework import serializers
from user_app.models import User, UserProfile


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
        UserProfile.objects.update_or_create(user=instance, defaults=profile)
        return super().update(instance, validated_data)

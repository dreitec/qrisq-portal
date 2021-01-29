from rest_framework import serializers
from user_app.models import User, UserProfile


class _UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('id', 'user')


class UserBasicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'username')


class UserSerializer(serializers.ModelSerializer):
    profile = _UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'profile')
        extra_kwargs = {
            'email': {'required': False}
        }

    def create(self, validated_data):
        if not validated_data.get('username', ''):
            raise serializers.ValidationError({'username': ['This field is required.']})

        if not validated_data.get('email', ''):
            raise serializers.ValidationError({'email': ['This field is required.']})

        profile = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile)
        return user

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile', {})
        UserProfile.objects.update_or_create(user=instance, defaults=profile)
        return super().update(instance, validated_data)

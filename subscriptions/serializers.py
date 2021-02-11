from rest_framework import serializers
from .models import Subscription, UsersSubscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['name', 'feature', 'price', 'duration']


class UsersSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersSubscription
        fields = ['user', 'subscription']
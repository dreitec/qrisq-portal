from rest_framework import serializers
from .models import SubscriptionPlan, UsersSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer()

    class Meta:
        model = UsersSubscription
        exclude = ('id', 'user')
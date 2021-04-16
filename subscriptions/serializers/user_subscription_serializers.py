from rest_framework import serializers

from subscriptions.models import SubscriptionPlan, UserSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer()

    class Meta:
        model = UserSubscription
        exclude = ('id', 'user')

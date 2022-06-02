from django.db import transaction

from rest_framework import serializers

from subscriptions.models import SubscriptionPlan, UserPayment, UserSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer()

    class Meta:
        model = UserSubscription
        exclude = ('id', 'user')

class UserPaymentSerializer(serializers.ModelSerializer):
    user_subscription = UserSubscriptionSerializer()

    class Meta:
        model = UserPayment
        fields = "__all__"
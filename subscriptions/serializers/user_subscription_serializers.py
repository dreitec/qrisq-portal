from django.db import transaction

from rest_framework import serializers

from subscriptions.models import SubscriptionPlan, UserSubscription, UserPayment


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer()

    class Meta:
        model = UserSubscription
        exclude = ('id', 'user')


class AddPaymentInfoSerializer(serializers.Serializer):
    subscription_plan_id = serializers.IntegerField()
    payment_id = serializers.CharField(max_length=30)
    payment_gateway = serializers.ChoiceField(choices = UserPayment.PAYMENT_CHOICES)

    def validate(self, data):
        error = {}
       
        if UserPayment.objects.filter(payment_id=data['payment_id']).exists():
            error['payment_id'] = "Payment ID exists."
        
        if not SubscriptionPlan.objects.filter(id=data['subscription_plan_id']).exists():
            error['subscription_plan_id'] = "Subscription plan does not exists"
        
        if error:
            raise serializers.ValidationError(error)

        return data

    @transaction.atomic()
    def create(self, validated_data):
        subscription_plan_id = validated_data.get('subscription_plan_id')
        payment_id = validated_data.get('payment_id')
        payment_gateway = validated_data.get('payment_gateway')
        user = self.context['request'].user

        user_subscription = UserSubscription.objects.create(user = user, plan_id=subscription_plan_id)
        UserPayment.objects.create(user = user, payment_id=payment_id, payment_gateway=payment_gateway, price=user_subscription.plan.price)
            
        return user_subscription
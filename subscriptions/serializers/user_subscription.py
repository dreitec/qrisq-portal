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
    payment_id = serializers.CharField(max_length=30, allow_null=True, required=False)
    payment_gateway = serializers.ChoiceField(choices=UserPayment.PAYMENT_CHOICES)

    def validate(self, data):
        error = {}
       
        if UserPayment.objects.filter(payment_id=data['payment_id']).exists():
            error['payment_id'] = "Payment ID exists."
        
        if error:
            raise serializers.ValidationError(error)

        return data

    @transaction.atomic()
    def create(self, validated_data):
        payment_id = validated_data.get('payment_id')
        payment_gateway = validated_data.get('payment_gateway')
        user = self.context['request'].user

        subscribed_plan = user.subscription_plan
        subscribed_plan.is_cancelled = False
        subscribed_plan.cancelled_at = None
        subscribed_plan.save()

        UserPayment.objects.create(
            user=user, payment_id=payment_id,
            payment_gateway=payment_gateway, price=subscribed_plan.plan.price
        )
            
        return user.subscription_plan

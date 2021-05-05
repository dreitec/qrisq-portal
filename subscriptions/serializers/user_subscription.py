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
    payment_id = serializers.CharField(max_length=30)
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

        price = user.subscription_plan.plan.price
        UserPayment.objects.create(
            user=user, payment_id=payment_id,
            payment_gateway=payment_gateway, price=price
        )
            
        return user_subscription

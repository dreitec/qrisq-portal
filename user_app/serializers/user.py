from django.db import transaction

from rest_framework import serializers

from user_app.models import User, UserProfile, NUMERIC_VALIDATOR
from subscriptions.serializers import UserSubscriptionSerializer
from subscriptions.models import UserSubscription, SubscriptionPlan, UserPayment
from core.boto_client import send_message_to_sqs_queue


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


class CompleteProfileSerializer(serializers.Serializer):
    address = serializers.JSONField()
    street_number = serializers.CharField(max_length=30)
    city = serializers.CharField(max_length=30)
    state = serializers.CharField(max_length=30)
    zip_code = serializers.CharField(max_length=5, validators=[NUMERIC_VALIDATOR])
    subscription_plan_id = serializers.IntegerField()
    payment_id = serializers.CharField(max_length=30)
    payment_gateway = serializers.ChoiceField(choices = UserPayment.PAYMENT_CHOICES)

    def validate(self, data):
        error = {}
       
        if UserPayment.objects.filter(payment_id=data['payment_id']).exists():
            error['payment_id'] = "Payment ID exists."
        
        if not SubscriptionPlan.objects.filter(id=data['subscription_plan_id']).exists():
            error['subscription_plan_id'] = "Subscription plan does not exists"
        
        address = data.get('address', {})
        if not ('lat' in address and 'lng' in address and 'displayText' in address):
            error['address'] = "Address information invalid. Please add 'lat', 'lng' and 'displayText' to address."

        if error:
            raise serializers.ValidationError(error)

        return data

    @transaction.atomic()
    def create(self, validated_data):
        subscription_plan_id = validated_data.pop('subscription_plan_id')
        payment_id = validated_data.pop('payment_id')
        payment_gateway = validated_data.pop('payment_gateway')
        user = self.context['request'].user
    
        try:
            user_profile = UserProfile.objects.filter(user = user)
            user_profile.update(**validated_data)
            UserSubscription.objects.create(user = user, plan_id=subscription_plan_id)
            UserPayment.objects.create(user = user, payment_id=payment_id, payment_gateway=payment_gateway)
            
        except Exception as err:
            raise Exception("Error completing profile.")

        try:
            send_message_to_sqs_queue(str(user.id),user_profile[0].address)
        except Exception as err:
            raise Exception("Error sending message to SQS queue.")
        
        return user_profile

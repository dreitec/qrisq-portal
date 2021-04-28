import datetime

from django.contrib.gis.db import models
from user_app.models import User


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=60, unique=True)
    feature = models.TextField(blank=True, default="")
    price = models.FloatField(default=0)
    duration = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription_plan")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="users")
    subscribed_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recurring = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(default=None, null=True)

    def cancel_subscription(self):
        self.is_cancelled = True
        self.cancelled_at = datetime.datetime.now()
        self.save()


class UserPayment(models.Model):
    
    PAYMENT_CHOICES = (
                ('paypal', 'PayPal'),
                ('fluidpay', 'FluidPay'),
            )
            
    payment_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="payment")
    payment_gateway = models.CharField(max_length=30, choices=PAYMENT_CHOICES)
    price = models.FloatField(default=0)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class PaymentRefund(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="refund")
    payment = models.OneToOneField(UserPayment, on_delete=models.DO_NOTHING, related_name="refund")
    # refund_transaction_id = models.CharField(max_length=20, unique=True)
    payment_gateway = models.CharField(max_length=30, choices = UserPayment.PAYMENT_CHOICES)

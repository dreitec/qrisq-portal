from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.gis.db import models
from django.db import transaction

from user_app.models import User


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=60, unique=True)
    feature = models.TextField(blank=True, default="")
    price = models.FloatField(default=0)
    duration = models.PositiveSmallIntegerField(default=0)
    paypal_plan_id = models.CharField(max_length=60, default="")
    fluidpay_plan_id = models.CharField(max_length=60, default="")

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription_plan")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="users")
    subscribed_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(default=None, null=True)
    expires_at = models.DateTimeField(default=None, null=True)
    is_free = models.BooleanField(default=False)

    def cancel_subscription(self):
        self.is_cancelled = True
        self.cancelled_at = datetime.now()
        self.save()


class UserPayment(models.Model):
    
    PAYMENT_CHOICES = (
                ('paypal', 'PayPal'),
                ('fluidpay', 'FluidPay'),
            )
            
    payment_id = models.CharField(max_length=60, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="payment")
    payment_gateway = models.CharField(max_length=30, choices=PAYMENT_CHOICES)
    subscription_id = models.CharField(max_length=60)
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name="user_payments", null=True, default=None)
    price = models.FloatField(default=0)
    paid_at = models.DateTimeField()
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.payment_id

    @transaction.atomic()
    def save(self, *args, **kwargs):
        if not self.id:
            now_time = datetime.now()
            self.paid_at = now_time
        self.user_subscription.expires_at = self.expires_at
        self.user_subscription.save()
        super().save(*args, **kwargs)


class PaymentRefund(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="refund")
    payment = models.OneToOneField(UserPayment, on_delete=models.DO_NOTHING, related_name="refund")
    # refund_transaction_id = models.CharField(max_length=20, unique=True)
    payment_gateway = models.CharField(max_length=30, choices = UserPayment.PAYMENT_CHOICES)

class Discount(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="discount")
    state = models.CharField(max_length=20)
    discount = models.FloatField(default=0)

    def __str__(self):
        return self.state

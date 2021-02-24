from django.contrib.gis.db import models
from user_app.models import User


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=60, unique=True)
    feature = models.TextField(blank=True, default="")
    price = models.FloatField(default=0)
    duration = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class UsersSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription_plan")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="users")
    subscribed_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recurring = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(default=None, null=True)


class PaypalCapture(models.Model):
    capture_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="capture")

    class Meta:
        db_table = "paypal_capture"

from django.contrib.gis.db import models
from user_app.models import User


class SubscriptionPlans(models.Model):
    name = models.CharField(max_length=60)
    feature = models.TextField(blank=True, default="")
    price = models.FloatField(default=0)
    duration = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class UsersSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription_plan")
    plan = models.ForeignKey(SubscriptionPlans, on_delete=models.CASCADE, related_name="users")
    subscribed_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recurring = models.BooleanField(default=False)
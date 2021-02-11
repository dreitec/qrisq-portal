from django.db import models
from user_app.models import User
from django.utils.translation import ugettext_lazy as _
import datetime


class Subscription(models.Model):
    name = models.CharField(_('name'), max_length=60)
    feature = models.TextField(_('feature'), blank=True, default="")
    price = models.FloatField(_('price'), blank=True, default=0)
    duration = models.DurationField(_('duration'), blank=True, default=datetime.timedelta(days=0, hours=0))

    def __str__(self):
        return self.name


class UsersSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
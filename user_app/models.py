from __future__ import unicode_literals
import datetime
import hashlib

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from core.validators import NUMERIC_VALIDATOR

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first_name'), max_length=60, blank=True)
    last_name = models.CharField(_('last_name'), max_length=60, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), auto_now_add=True)
    is_admin = models.BooleanField(_('is_admin'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)
    deleted_at = models.DateTimeField(_('deleted_at'), default=None, null=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now()
        self.save()

            
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.JSONField(default=dict, null=True)
    street_number = models.CharField(max_length=100, blank=True, default="")
    city = models.CharField(max_length=50, blank=True, default="")
    state = models.CharField(max_length=30, blank=True, default="")
    zip_code = models.CharField(max_length=5, validators=[NUMERIC_VALIDATOR], blank=True, default="")
    is_preprocessed = models.BooleanField(default=False)
    address_updated = models.IntegerField(default=0)


class UserPingDragAttempt(models.Model):
    user = models.OneToOneField(User, related_name="pin_drag_attempt", on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0, validators=[MaxValueValidator(5),])

    def save(self, *args, **kwargs):
        if not self.id:
            self.attempts = 1
        else:
            self.attempts += 1
            if self.attempts > 5:
                raise ValidationError("The attempt limit has exceeded.")
        
        super().save(*args, **kwargs)
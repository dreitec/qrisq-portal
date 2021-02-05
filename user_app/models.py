from __future__ import unicode_literals
import hashlib

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first_name'), max_length=60, blank=True)
    last_name = models.CharField(_('last_name'), max_length=60, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=False)
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


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.JSONField(default=dict, null=True)

    def __str__(self):
        return self.user.username

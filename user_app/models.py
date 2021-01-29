from __future__ import unicode_literals
import hashlib

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=30, blank=True)
    email = models.EmailField(_('email'), unique=True)
    full_name = models.CharField(_('full_name'), max_length=60, blank=True)
    date_joined = models.DateTimeField(_('date_joined'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.JSONField(default=dict, null=True)

    def __str__(self):
        return self.user.username

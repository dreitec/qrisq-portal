import random
import string

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def mail_sender(template, context, subject, recipient_list):
    message = render_to_string(template, context)
    send_mail(subject=subject, message='',
              from_email=getattr(settings, 'FROM_EMAIL', ''),
              recipient_list=recipient_list,
              html_message=message)


def generate_password_reset_token(user):
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    return uid, token


def check_reset_token(user, token):
    return PasswordResetTokenGenerator().check_token(user, token)

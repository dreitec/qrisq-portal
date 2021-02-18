from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from user_app.utils import generate_password_reset_token, check_reset_token
from user_app.models import User


class TestUtils(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@gmail.com')

    def test_generate_password_reset_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = PasswordResetTokenGenerator().make_token(self.user)
        response = generate_password_reset_token(self.user)
        self.assertEqual(uid, response[0])
        self.assertEqual(token, response[1])

    def test_check_reset_token_with_correct_token(self):
        token = PasswordResetTokenGenerator().make_token(self.user)
        response = check_reset_token(self.user, token)
        self.assertEqual(response, True)

    def test_check_reset_token_with_incorrect_token(self):
        token = 'abc'
        response = check_reset_token(self.user, token)
        self.assertEqual(response, False)
        
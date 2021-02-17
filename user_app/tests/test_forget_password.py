from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from user_app.models import User
from user_app.views import ChangePasswordView, LoginView


class TestForgetPassword(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="client@test.com", password="admin@123", is_admin=False)
        self.forget_password_url = reverse('forgot-password')

    def test_wrong_forget_password(self):
        data = {"email": 'test@gmail.com'}
        response = self.client.post(self.forget_password_url, data, format='json')
        self.assertEquals(response.status_code, 400)
        self.assertEqual(response.data, {"message":"User not found"})

    def test_forget_password(self):
        data = {"email": 'client@test.com'}
        response = self.client.post(self.forget_password_url, data, format='json')
        self.assertEqual(response.data, {"message":"Password reset email has been sent. Please check your mail inbox."})

    def test_blank_email_forgetpassword(self):
        data = {"email": ''}
        response = self.client.post(self.forget_password_url, data, format='json')
        self.assertEqual(response.data, {"message": "Email is not provided."})

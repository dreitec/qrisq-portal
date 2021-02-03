from django.test import TestCase
from django.urls import reverse
from user_app.models import User
from rest_framework.test import APITestCase, APIClient


class TestAuth(APITestCase):
    def setUp(self):
        self.signin_url = reverse('login')
        self.logout_url = reverse('logout')
        self.forget_password_url = reverse('forgot-password')
        self.change_password_url = reverse('change-password')

    def test_signin(self):
        user = User.objects.create(username='test_name', is_active=True)
        user.set_password('admin@123')
        user.save()

        data = {
               "username": "test_name",
               "password": "admin@123"
               }

        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'refresh')
        self.assertContains(response, 'access')

    def test_credentials_error(self):
        user = User.objects.create(username='test_name')
        user.set_password('admin@123')
        user.save()

        data = {
               "username": "test_name",
               "password": "admin"
               }

        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'msg': 'No active account found with the given credentials.'})

    def test_non_active_user_login(self):
        user = User.objects.create(username='test_name')
        user.set_password('admin@123')
        user.save()

        data = {
               "username": "test_name",
               "password": "admin@123"
               }

        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'msg': 'No active account found with the given credentials.'})

    def login(self):
        user = User.objects.create(username='test_name', is_active=True)
        user.set_password('admin@123')
        user.save()
        data = {
               "username": "test_name",
               "password": "admin@123"
               }
            
        response = self.client.post(self.signin_url, data, format='json')
        return response.data


    def test_logout(self):
        login_credentials = self.login()
        data = {
            "refresh": login_credentials['refresh']
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_credentials['access'])
        response = self.client.post(self.logout_url, data, format='json')

        self.assertEqual(response.data, {'detail': 'Successfully logged out.'})

    def test_wrong_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        data = {
            "refresh": 'abc'
        }
        response = self.client.post(self.logout_url, data, format='json')

        error_message = {
                    "token_class": "AccessToken",
                    "token_type": "access",
                    "message": "Token is invalid or expired"
                }
        
        self.assertEqual(response.data['messages'][0], error_message)


    def test_forget_password(self):
        data = {
            "email": 'test@gmail.com'
        }

        response = self.client.post(self.forget_password_url, data, format='json')
        self.assertEqual(response.data, {"msg":"Password reset email has been sent. Please check your mail inbox."})

    def test_blank_email_forgetpassword(self):
        data = {
            "email": ''
        }

        response = self.client.post(self.forget_password_url, data, format='json')
        self.assertEqual(response.data, {"msg":"Email is not provided."})

    def test_change_password(self):
        login_credentials = self.login()

        data = {
            "old_password": 'admin@123',
            "new_password": "admin@321",
            "confirm_password": "admin@321"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_credentials['access'])
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.data, {'msg': "Your password has been changed successfully."})

    def test_wrong_password_for_change_password(self):
        login_credentials = self.login()

        data = {
            "old_password": 'admin',
            "new_password": "admin@321",
            "confirm_password": "admin@321"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_credentials['access'])
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.data, {'old_password': ['Invalid old password.']})

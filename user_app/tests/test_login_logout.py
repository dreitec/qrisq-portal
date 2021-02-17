from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from user_app.models import User
from user_app.views import ChangePasswordView, LoginView


class TestLoginLogout(APITestCase):
    def setUp(self):
        self.signin_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(email="client@test.com", password="admin@123", is_admin=False)
        self.deleted_user = User.objects.create_user(email="delete@test.com", password="admin@123")
        self.deleted_user.delete()

    def test_signin(self):
        data = {
            "email": "client@test.com",
            "password": "admin@123"
        }
        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'refresh')
        self.assertContains(response, 'access')

    def test_credentials_error(self):
        data = {
            "email": "client@test.com",
            "password": "admin"
        }
        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'message': 'No active account found with the given credentials.'})

    def test_deleted_user_login(self):
        data = {
            "email": "delete@test.com",
            "password": "admin@123"
        }
        response = self.client.post(self.signin_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'message': 'No active account found with the given credentials'})

    def login(self):
        data = {
            "email": "client@test.com",
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

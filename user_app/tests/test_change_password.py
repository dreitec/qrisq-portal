from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from user_app.models import User
from user_app.views import ChangePasswordView, LoginView


class TestChangePassword(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="client@test.com", password="admin@123", is_admin=False)

    def test_change_password(self):
        data = {
            "old_password": 'admin@123',
            "new_password": "admin@321",
            "confirm_password": "admin@321"
        }
        factory = APIRequestFactory()
        request = factory.post('api/auth/change-password', data, format="json")
        force_authenticate(request, self.user)
        response = ChangePasswordView.as_view()(request)
        self.assertTrue(response.status_code==200)
        self.assertEqual(response.data, {'message': "Your password has been changed successfully."})
        
        # Login with old password
        login_request = factory.post(
            "api/auth/login",
            {'email': self.user.email, 'password': data['old_password']},
            format="json"
        )
        login_response = LoginView.as_view()(login_request)
        self.assertTrue(login_response.status_code==401)
        
        # login with new password
        login_request = factory.post(
            "api/auth/login",
            {'email': self.user.email, 'password': data['new_password']},
            format="json"
        )
        login_response = LoginView.as_view()(login_request)
        self.assertTrue(login_response.status_code==200)

    def test_wrong_old_password(self):
        data = {
            "old_password": 'admin',
            "new_password": "admin@321",
            "confirm_password": "admin@321"
        }
        factory = APIRequestFactory()
        request = factory.post('api/auth/change-password', data, format="json")
        force_authenticate(request, self.user)
        response = ChangePasswordView.as_view()(request)
        self.assertTrue(response.status_code==403)
        self.assertEqual(response.data, {'old_password': ['Invalid old password.']})

    def test_unmatched_password(self):
        data = {
            "old_password": 'admin@123',
            "new_password": "admin@321",
            "confirm_password": "admin@32"
        }
        factory = APIRequestFactory()
        request = factory.post('api/auth/change-password', data, format="json")
        force_authenticate(request, self.user)
        response = ChangePasswordView.as_view()(request)
        self.assertTrue(response.status_code==400)
        self.assertEqual(response.data, {'confirm_password': ["Passwords didn't match."]})

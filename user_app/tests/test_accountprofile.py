import json
from collections import OrderedDict
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from user_app.models import User, UserProfile
from user_app.views import AccountProfileView
from user_app.serializers import UserSerializer


class TestAccountProfile(APITestCase):
    def setUp(self):
        self.account_profile_url = reverse('account-profile')
        self.factory = APIRequestFactory()
        self.admin_user = User.objects.create_user(email='admin@test.com', password="admin@123", first_name="", last_name="", is_admin=True)
        self.client_user = User.objects.create_user(email="client@test.com", password="admin@123", first_name="", last_name="", is_admin=False)
        UserProfile.objects.create(
            user=self.client_user,
            phone_number="1234567890",
            address={"lat": 27.021212, "lng": 80.454545},
            state="Utah",
            street_number="24-St.Martin",
            city="Somewhere",
            zip_code="12134"
        )

    def test_get_profile_admin(self):
        request = self.factory.get("api/auth/account-profile")
        force_authenticate(request, self.admin_user)
        response = AccountProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data, {
            'id': self.admin_user.id,
            'email': 'admin@test.com', 
            'first_name': '',
            'last_name': '',
            'profile': None
        })
    

    def test_get_profile_client(self):
        request = self.factory.get("api/auth/account-profile")
        force_authenticate(request, self.client_user)
        response = AccountProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': self.client_user.id,
            'email': 'client@test.com',
            'first_name': '',
            'last_name': '',
            'profile': OrderedDict({
                "phone_number": "1234567890",
                "address": {"lat": 27.021212, "lng": 80.454545},
                "street_number": "24-St.Martin",
                "city": "Somewhere",
                "state": "Utah",
                "zip_code": "12134" 
            })
        })

    def test_unauthorized_get_profile(self):
        self.client.credentials()
        response = self.client.get(self.account_profile_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_update_profile_admin(self):
        data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'profile': {
                "phone_number": "1234567890",
                "address": {"lat": 27.021212, "lng": 80.454545},
                "street_number": "24-St.Martin",
                "city": "Somewhere",
                "state": "Utah",
                "zip_code": "12134" 
            }
        }

        request = self.factory.post("api/auth/account-profile", data, format='json')
        force_authenticate(request, self.admin_user)
        response = AccountProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': self.admin_user.id,
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'profile': OrderedDict({
                "phone_number": "1234567890",
                "address": {"lat": 27.021212, "lng": 80.454545},
                "street_number": "24-St.Martin",
                "city": "Somewhere",
                "state": "Utah",
                "zip_code": "12134"
            })
        })

    def test_update_profile_client(self):
        data = {
            'first_name': 'Client',
            'last_name': 'User',
            'profile': {
                "phone_number": "0123456",
                "address": {"lat": 28.0212, "lng": 82.454545},
                "street_number": "24-St.Mary's",
                "city": "Somewhere on earth",
                "state": "Oregon",
                "zip_code": "12135"
            }
        }

        request = self.factory.post("api/auth/account-profile", data, format='json')
        force_authenticate(request, self.client_user)
        response = AccountProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': self.client_user.id,
            'email': 'client@test.com',
            'first_name': 'Client',
            'last_name': 'User',
            'profile': OrderedDict({
                "phone_number": "0123456",
                "address": {"lat": 27.021212, "lng": 80.454545},
                "street_number": "24-St.Martin",
                "city": "Somewhere",
                "state": "Utah",
                "zip_code": "12134" 
            })
        })
        self.assertNotEqual(response.data, {
            'id': self.client_user.id,
            'email': 'client@test.com',
            'first_name': 'Client',
            'last_name': 'User',
            'profile': OrderedDict({
                "phone_number": "0123456",
                "address": {"lat": 28.0212, "lng": 82.454545},
                "street_number": "24-St.Mary's",
                "city": "Somewhere on earth",
                "state": "Oregon",
                "zip_code": "12135"
            })
        })
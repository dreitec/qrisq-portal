from django.test import TestCase
from django.urls import reverse
from user_app.models import User
from rest_framework.test import APITestCase, APIClient
import json


class TestAccountProfile(APITestCase):
    def setUp(self):
        self.account_profile_url = reverse('account-profile')
        self.signin_url = reverse('login')
        
        self.user = User.objects.create(username='test_name', is_active=True)
        self.user.set_password('admin@123')
        self.user.save()
        self.data = {
               "username": "test_name",
               "password": "admin@123"
            }
            
        self.response = self.client.post(self.signin_url, self.data, format='json')
        self.access_token = self.response.data["access"]

    def test_get_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.account_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': 2, 
                    'username': 'test_name', 
                    'email': '', 
                    'full_name': '', 
                    'profile': None
                    })

    def test_unauthorized_get_profile(self):
        self.client.credentials()
        response = self.client.get(self.account_profile_url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_create_profile(self):
        data= {
            "profile": {
                "user": 1,
                "phone_number": 987654321,
                "address": "test_address"
            }
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.account_profile_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"id": 1, 
                "username": "test_name", 
                "email": "", 
                "full_name": "", 
                "profile": {
                    "phone_number": "987654321", 
                    "address": "test_address"
                }
            })
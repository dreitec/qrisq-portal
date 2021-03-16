import json
from collections import OrderedDict
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from user_app.models import User, UserProfile
from user_app.views import AccountProfileView
from user_app.serializers import UserSerializer


class TestAdminUserCrud(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="admin@123", is_admin=True)
        data = {
            "email": "user@test.com",
            "password": "admin@123"
        }
        self.response = self.client.post('/api/auth/login', data, format='json')
        self.access_token = self.response.data['access']

        self.client_user = User.objects.create_user(email="client@test.com", password="admin@123")
        client_data = {
            "email": "client@test.com",
            "password": "admin@123"
        }
        self.client_response = self.client.post('/api/auth/login', client_data, format='json')
        self.client_access_token = self.client_response.data['access']

    def test_create_user_by_admin(self):
        data= {
            "email": "test11@gmail.com",
            "first_name": "Test",
            "last_name": "test",
            "password": "test@123"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post('/api/users', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Admin User created')
        self.assertEqual(json.loads(response.content)['data']['email'],'test11@gmail.com')
        self.assertEqual(json.loads(response.content)['data']['first_name'],'Test')
        self.assertEqual(json.loads(response.content)['data']['last_name'],'test')

    def test_create_user_by_non_admin(self):
        data= {
            "email": "test2@gmail.com",
            "first_name": "Test",
            "last_name": "test",
            "password": "test@123"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.client_access_token)
        response = self.client.post('/api/users', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {
            "detail": "You do not have permission to perform this action."
        })

    def test_create_user_without_auth(self):
        data= {
            "email": "test2@gmail.com",
            "first_name": "Test",
            "last_name": "test",
            "password": "test@123"
        }
        response = self.client.post('/api/users', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_user_with_empty_email(self):
        data= {
            "email": "",
            "first_name": "Test",
            "last_name": "test",
            "password": "test@123"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post('/api/users', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            "email": [
                "This field may not be blank."
            ]
        })

    def test_create_user_with_wrong_email_format(self):
        data= {
            "email": "test",
            "first_name": "Test",
            "last_name": "test",
            "password": "test@123"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post('/api/users', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            "email": [
                "Enter a valid email address."
            ]
        })

    def test_create_user_without_password(self):
        data= {
            "email": "testtests@test.com",
            "first_name": "Test",
            "last_name": "test",
            "password": ""
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post('/api/users', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            "password": [
                "This field may not be blank."
            ]
        })

    def test_retrieve_user_without_auth(self):
        response = self.client.get('/api/users/'+str(self.user.id))
        self.assertEqual(response.status_code, 401)

    def test_retrieve_user_by_client_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.client_access_token)
        response = self.client.get('/api/users/'+str(self.user.id))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {
            "detail": "You do not have permission to perform this action."
        })

    def test_retrieve_user_by_admin_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get('/api/users/'+str(self.client_user.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": self.client_user.id,
            "email": "client@test.com",
            "first_name": "",
            "last_name": "",
            "profile": None
        })

    def test_update_user_by_admin_user(self):
        data = {
            "first_name": "Test",
            "last_name": "test",
            "profile": {
                "phone_number": "9860111042",
                "address": 'test',
                "street_number": "1",
                "city": "lalitpur",
                "state": "2",
                "zip_code": "44614"
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.put('/api/users/'+str(self.user.id), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": self.user.id,
            "email": "user@test.com",
            "first_name": "Test",
            "last_name": "test",
            "profile": {
                "phone_number": "9860111042",
                "address": 'test',
                "street_number": "1",
                "city": "lalitpur",
                "state": "2",
                "zip_code": "44614"
            }
        })

    def test_update_user_by_non_admin(self):
        data= {
            "first_name": "Test",
            "last_name": "test",
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.client_access_token)
        response = self.client.put('/api/users/'+str(self.user.id), data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {
            "detail": "You do not have permission to perform this action."
        })

    def test_delete_user_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.delete('/api/users/'+str(self.client_user.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "message": "User Deleted Successfully"
        })

    def test_delete_user_by_client_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.client_access_token)
        response = self.client.delete('/api/users/'+str(self.client_user.id))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {
            "detail": "You do not have permission to perform this action."
        })

    def test_delete_user_without_auth(self):
        response = self.client.delete('/api/users/'+str(self.client_user.id))
        self.assertEqual(response.status_code, 401)
        
from django.test import TestCase
from django.urls import reverse
from user_app.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class TestSignup(APITestCase):
    def setUp(self):
        self.url = reverse('signup')

    def test_signup(self):
        data = {
               "username": "test_name",
               "full_name": "test_full_name",
               "email": "test@gmail.com",
               "password": "admin@123",
               "confirm_password": "admin@123"
               }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_name')
        self.assertJSONEqual(str(response.content, encoding='utf8'),
            {'msg': 'User successfully created.'})

    def test_password_and_confirm_password(self):
        data = {
               "username": "test_name",
               "full_name": "test_full_name",
               "email": "test@gmail.com",
               "password": "admin@123",
               "confirm_password": "admin"
               }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
            {'password_confirmation': ["Passwords didn't match."]})

    def test_unique_username_and_email(self):
        user = User.objects.create(username='test_name', email='test@gmail.com')
        user.set_password('admin@123')
        user.save()
        data = {
               "username": "test_name",
               "full_name": "test_full_name",
               "email": "test@gmail.com",
               "password": "admin@123",
               "confirm_password": "admin@123"
               }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
            {'email': ["User with this email exists."],
            'username': ["User with this username exists."]})

    def test_blank_username(self):
        data = {
               "username": "",
               "full_name": "test_full_name",
               "email": "test@gmail.com",
               "password": "admin@123",
               "confirm_password": "admin@123"
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
            {'username': ["This field may not be blank."]})

    def test_blank_fullname(self):
        data = {
               "username": "test_name",
               "full_name": "",
               "email": "test@gmail.com",
               "password": "admin@123",
               "confirm_password": "admin@123"
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
            {'full_name': ["This field may not be blank."]})

    def test_blank_email(self):
        data = {
               "username": "test_name",
               "full_name": "test_full_name",
               "email": "",
               "password": "admin@123",
               "confirm_password": "admin@123"
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
            {'email': ["This field may not be blank."]})
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from rest_framework.test import APITestCase
from rest_framework import status

from user_app.models import User


class SignupTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('signup')
        User.objects.create_user(email="first@last.com", password="asd123!@#", first_name="First", last_name="Last")

    def test_signup(self):
        data = {
            "first_name": "first",
            "last_name": "last",
            "email": "test@gmail.com",
            "password": "admin@123",
            "confirm_password": "admin@123",
            "phone_number": "1234567890",
            "address": {"lat": 27.456123, "lng": "81.1213"},
            "street_number": "24-St. Martin",
            "city": "Patan",
            "state": "Bagmati",
            "zip_code": 44700
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.filter(email=data["email"]).count(), 1)
        self.assertNotEquals(User.objects.last().password, data["password"])
        self.assertTrue(check_password(data["password"], User.objects.get(email=data["email"]).password))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'User successfully created.'}
        )

    def test_unmatched_passwords(self):
        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test@gmail.com",
            "password": "admin@123",
            "confirm_password": "admin",
            "phone_number": "1234567890",
            "address": {"lat": 27.456123, "lng": "81.1213"},
            "street_number": "24-St. Martin",
            "city": "Patan",
            "state": "Bagmati",
            "zip_code": 44700
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'confirm_password': ["Passwords didn't match."]}
        )

    def test_unique_email(self):
        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "first@last.com",
            "password": "admin@123",
            "confirm_password": "admin@123",
            "phone_number": "1234567890",
            "address": {"lat": 27.456123, "lng": "81.1213"},
            "street_number": "24-St. Martin",
            "city": "Patan",
            "state": "Bagmati",
            "zip_code": 44700
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'email': ["User with this email exists."],}
        )

    def test_blank_name(self):
        data = {
            "first_name": "",
            "last_name": "",
            "email": "test@gmail.com",
            "password": "admin@123",
            "confirm_password": "admin@123",
            "phone_number": "1234567890",
            "address": {"lat": 27.456123, "lng": "81.1213"},
            "street_number": "24-St. Martin",
            "city": "Patan",
            "state": "Bagmati",
            "zip_code": 44700
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'first_name': ["This field may not be blank."],
             'last_name': ["This field may not be blank."]}
        )

    def test_invalid_email1(self):
        data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "test@gmail..com",
            "password": "admin@123",
            "confirm_password": "admin@123",
            "phone_number": "1234567890",
            "address": {"lat": 27.456123, "lng": "81.1213"},
            "street_number": "24-St. Martin",
            "city": "Patan",
            "state": "Bagmati",
            "zip_code": 44700
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'email': ["Enter a valid email address."]}
        )

    def test_blank_email(self):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "",
            "password": "admin@123",
            "confirm_password": "admin@123",
            "phone_number": "1234567890",
            "address": {"lat": 27.456123, "lng": "81.1213"},
            "street_number": "24-St. Martin",
            "city": "Patan",
            "state": "Bagmati",
            "zip_code": 44700
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'email': ["This field may not be blank."]}
        )

    def test_invalid_zipcode(self):
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "test@admin.com",
            "password": "admin@123",
            "confirm_password": "admin@123",
            "phone_number": "1234567890",
            "address": {"lat": 27.456123, "lng": "81.1213"},
            "street_number": "24-St. Martin",
            "city": "Patan",
            "state": "Bagmati",
            "zip_code": "asdfa"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'zip_code': ["Only numeric characters"]}
        )
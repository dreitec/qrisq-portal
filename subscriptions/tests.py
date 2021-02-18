import json
import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

from .models import SubscriptionPlan
from user_app.models import User
from subscriptions.views import SubscriptionPlanViewSet


class SubscriptionPlanTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.subscription_plan = SubscriptionPlan.objects.create(
            name = "Free Subscription",
            feature = "test feature",
            price = 0.0,
            duration = 0)
        self.admin_user = User.objects.create_user(email='admin@gmail.com', password="admin@123", is_admin=True)
        self.user = User.objects.create_user(email='user@gmail.com', password="admin@123")

    def test_get_subscription_plan(self):
        response = self.client.get('/api/subscription-plans')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            {
                "id": self.subscription_plan.id,
                "name": "Free Subscription",
                "feature": "test feature",
                "price": 0.0,
                "duration": 0
            }
        ])

    def test_retrieve_existing_subscription_plan(self):
        response = self.client.get('/api/subscription-plans/' + str(self.subscription_plan.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "id": self.subscription_plan.id,
            "name": "Free Subscription",
            "feature": "test feature",
            "price": 0.0,
            "duration": 0
        })

    def test_retrieve_non_existing_subscription_plan(self):
        response = self.client.get('/api/subscription-plans/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content),{'detail': 'Not found.'})

    def test_create_subscription_plan_without_authentication(self):
        response = self.client.post('/api/subscription-plans', {
            "name": "Test Subscription",
            "feature": "test feature",
            "price": 0,
            "duration": 10
        }, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content),{'detail': 'Authentication credentials were not provided.'})

    def test_create_subscription_plan_with_permission(self):
        request = self.factory.post('/api/subscription-plans',  {
            "name": "Test Subscription",
            "feature": "test feature",
            "price": 0,
            "duration": 10
        })
        view = SubscriptionPlanViewSet.as_view({'post':'create'})
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            "id": 2,
            "name": "Test Subscription",
            "feature": "test feature",
            "price": 0.0,
            "duration": 10
        })

    def test_create_subscription_plan_without_permission(self):
        request = self.factory.post('/api/subscription-plans',  {
            "name": "Test Subscription",
            "feature": "test feature",
            "price": 0
        })
        view = SubscriptionPlanViewSet.as_view({'post':'create'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data,{'detail': 'You do not have permission to perform this action.'})  

    def test_create_subscription_without_name(self):
        request = self.factory.post('/api/subscription-plans',  {
            "name": "",
            "feature": "test feature",
            "price": 0
        })
        view = SubscriptionPlanViewSet.as_view({'post':'create'})
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,{"name": [
            "This field may not be blank."
        ]})  


    def test_create_subscription_string_price(self):
        request = self.factory.post('/api/subscription-plans',  {
            "name": "test subscription",
            "feature": "test feature",
            "price": "price"
        })
        view = SubscriptionPlanViewSet.as_view({'post':'create'})
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,{"price": [
            "A valid number is required."
            ]
        }) 

    def test_create_subscription_string_duration(self):
        request = self.factory.post('/api/subscription-plans',  {
            "name": 2,
            "feature": "test feature",
            "price": 1,
            "duration": 'aa'
        })
        view = SubscriptionPlanViewSet.as_view({'post':'create'})
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,{"duration": [
            "A valid integer is required."
            ]
        }) 

    def test_delete_subscription(self):
        data = {
            "email": "admin@gmail.com",
            "password": "admin@123"
        }
        login_response = self.client.post('/api/auth/login', data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_response.data['access'])
        response = self.client.delete('/api/subscription-plans/' + str(self.subscription_plan.id))
        self.assertEqual(response.status_code, 204)
    
    def test_update_subscription_without_auth(self):
        response = self.client.put('/api/subscription-plans/' + str(self.subscription_plan.id), {
            "name": "Test Subscription",
            "feature": "test feature",
            "price": 0
        }, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content),{'detail': 'Authentication credentials were not provided.'})

    def test_update_subscription_plan_without_permission(self):
        request = self.factory.put('/api/subscription-plans',  {
            'name' : "Free Subscription",
            'feature' : "test feature",
            'price' : 0.0,
            'duration' : 0
        })
        view = SubscriptionPlanViewSet.as_view({'put':'update'})
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.subscription_plan.id)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data,{'detail': 'You do not have permission to perform this action.'})

    def test_update_subscription_plan_with_permission(self):
        request = self.factory.put('/api/subscription-plans',  {
            'name' : "Free Subscription",
            'feature' : "test feature",
            'price' : 100.0,
            'duration' : 12
        }, format='json')
        view = SubscriptionPlanViewSet.as_view({'put': 'update'})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.subscription_plan.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id" : self.subscription_plan.id,
            "name": "Free Subscription",
            "feature": "test feature",
            "price": 100.0,
            "duration": 12
        })

    def test_update_subscription_plan_without_name(self):
        request = self.factory.put('/api/subscription-plans',  {
            'name' : "",
            'feature' : "test feature",
            'price' : 100.0,
            'duration' : 0
        }, format='json')
        view = SubscriptionPlanViewSet.as_view({'put': 'update'})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.subscription_plan.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,{"name": [
            "This field may not be blank."
        ]}) 

    def test_update_subscription_plan_with_string_duration(self):
        request = self.factory.put('/api/subscription-plans',  {
            'name' : "Free Subscription",
            'feature' : "test feature",
            'price' : 100,
            'duration' : 'duration'
        }, format='json')
        view = SubscriptionPlanViewSet.as_view({'put': 'update'})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.subscription_plan.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,{"duration": [
            "A valid integer is required."
            ]
        }) 

    def test_update_subscription_plan_with_string_price(self):
        request = self.factory.put('/api/subscription-plans',  {
            'name' : "Free Subscription",
            'feature' : "test feature",
            'price' : "a",
            'duration' : 12
        }, format='json')
        view = SubscriptionPlanViewSet.as_view({'put': 'update'})
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=self.subscription_plan.id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,{"price": [
            "A valid number is required."
            ]
        }) 
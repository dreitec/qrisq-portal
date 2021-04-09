from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status

from user_app.models import User, UserProfile
from subscriptions.models import SubscriptionPlan, UserPayment
from user_app.views import CompleteProfileView


class CompleteProfileTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(email="first@last.com", password="asd123!@#", first_name="First", last_name="Last")
        self.user1 = User.objects.create_user(email="first@last1.com", password="asd123!@#", first_name="First", last_name="Last")
        UserProfile.objects.create(user=self.user, phone_number=9876543210)
        SubscriptionPlan.objects.create(id =1, name="Monthly", price=5.0)
        UserPayment.objects.create(user=self.user1, payment_id="1VY50037AU6854712T", payment_gateway="paypal")

    def test_complete_profile(self):
        data = {
            "address": {
                "lat": 27.7167099,
                "lng": 85.3131018,
                "displayText": "Damkal, Lalitpur 44700, Nepal"
            },
            "street_number": "24 - Pulchowk",
            "city": "Lalitpur",
            "state": "Bagmati",
            "zip_code": "44700",
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "paypal"
        }
        request = self.factory.post("api/complete-profile", data, format='json')
        force_authenticate(request, self.user)
        response = CompleteProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data,{'message': "User profile completed."})

    def test_invalid_zipcode(self):
        data = {
            "address": {
                "lat": 27.7167099,
                "lng": 85.3131018,
                "displayText": "Damkal, Lalitpur 44700, Nepal"
            },
            "street_number": "24 - Pulchowk",
            "city": "Lalitpur",
            "state": "Bagmati",
            "zip_code": "asdf",
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "paypal"
        }
        request = self.factory.post("api/complete-profile", data, format='json')
        force_authenticate(request, self.user)
        response = CompleteProfileView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['zip_code'],
            ["Only numeric characters"]
        )

    def test_invalid_subscription_id(self):
        data = {
            "address": {
                "lat": 27.7167099,
                "lng": 85.3131018,
                "displayText": "Damkal, Lalitpur 44700, Nepal"
            },
            "street_number": "24 - Pulchowk",
            "city": "Lalitpur",
            "state": "Bagmati",
            "zip_code": "44700",
            "subscription_plan_id": 2,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "paypal"
        }
        request = self.factory.post("api/complete-profile", data, format='json')
        force_authenticate(request, self.user)
        response = CompleteProfileView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['subscription_plan_id'],
            ["Subscription plan does not exists"]
        )

    def test_existing_payment_id(self):
        data = {
            "address": {
                "lat": 27.7167099,
                "lng": 85.3131018,
                "displayText": "Damkal, Lalitpur 44700, Nepal"
            },
            "street_number": "24 - Pulchowk",
            "city": "Lalitpur",
            "state": "Bagmati",
            "zip_code": "44700",
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712T",
            "payment_gateway": "paypal"
        }
        request = self.factory.post("api/complete-profile", data, format='json')
        force_authenticate(request, self.user)
        response = CompleteProfileView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user(self):
        data = {
            "address": {
                "lat": 27.7167099,
                "lng": 85.3131018,
                "displayText": "Damkal, Lalitpur 44700, Nepal"
            },
            "street_number": "24 - Pulchowk",
            "city": "Lalitpur",
            "state": "Bagmati",
            "zip_code": "44700",
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "paypal"
        }
        request = self.factory.post("api/complete-profile", data, format='json')
        response = CompleteProfileView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_invalid_payment_gateway(self):
        data = {
            "address": {
                "lat": 27.7167099,
                "lng": 85.3131018,
                "displayText": "Damkal, Lalitpur 44700, Nepal"
            },
            "street_number": "24 - Pulchowk",
            "city": "Lalitpur",
            "state": "Bagmati",
            "zip_code": "44700",
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "testpay"
        }
        request = self.factory.post("api/complete-profile", data, format='json')
        force_authenticate(request, self.user)
        response = CompleteProfileView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['payment_gateway'],
            ["\"testpay\" is not a valid choice."]
        )

    def test_invalid_address(self):
        data = {
            "address": "kathmandu",
            "street_number": "24 - Pulchowk",
            "city": "Lalitpur",
            "state": "Bagmati",
            "zip_code": "44700",
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "fluidpay"
        }

        request = self.factory.post("api/complete-profile", data, format='json')
        force_authenticate(request, self.user)
        response = CompleteProfileView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['address'],
            ["Address information invalid. Please add 'lat', 'lng' and 'displayText' to address."]
        )
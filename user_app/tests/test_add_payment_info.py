from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status

from user_app.models import User, UserProfile
from subscriptions.models import SubscriptionPlan, UserPayment
from subscriptions.views import AddPaymentInfoView


class AddPaymentInfoTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(email="first@last.com", password="asd123!@#", first_name="First", last_name="Last")
        self.user1 = User.objects.create_user(email="first@last1.com", password="asd123!@#", first_name="First", last_name="Last")
        self.url = 'api/add-payment-info'
        UserProfile.objects.create(user=self.user, phone_number=9876543210)
        SubscriptionPlan.objects.create(id =1, name="Monthly", price=5.0)
        UserPayment.objects.create(user=self.user1, payment_id="1VY50037AU6854712T", payment_gateway="paypal")

    def test_add_payment_info(self):
        data = {
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "paypal"
        }
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, self.user)
        response = AddPaymentInfoView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data,{'message': "Successfully added payment info."})

    def test_invalid_subscription_id(self):
        data = {
            "subscription_plan_id": 2,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "paypal"
        }
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, self.user)
        response = AddPaymentInfoView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['subscription_plan_id'],
            ["Subscription plan does not exists"]
        )

    def test_existing_payment_id(self):
        data = {
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712T",
            "payment_gateway": "paypal"
        }
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, self.user)
        response = AddPaymentInfoView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_payment_gateway(self):
        data = {
            "subscription_plan_id": 1,
            "payment_id": "1VY50037AU6854712S",
            "payment_gateway": "testpay"
        }
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, self.user)
        response = AddPaymentInfoView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['payment_gateway'],
            ["\"testpay\" is not a valid choice."]
        )
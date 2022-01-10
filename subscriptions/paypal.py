import datetime
import sys
import base64
import requests
from urllib.parse import quote
import dateutil.parser
import logging
import json

from django.conf import settings

from paypalcheckoutsdk.core import SandboxEnvironment, LiveEnvironment, PayPalHttpClient
from paypalcheckoutsdk.payments import CapturesGetRequest, CapturesRefundRequest
from paypalhttp.http_error import HttpError

import subscriptions.subscription_date_utils as subscription_date_utils

from subscriptions.models import PaymentRefund, UserSubscription, UserPayment, SubscriptionPlan
from user_app.models import User


class OrderApproveRequest:
    """
    Approve an order, by ID.
    """
    def __init__(self, order_id):
        self.verb = "GET"
        self.path = "/checkoutnow?token={order_id}".replace("{order_id}", quote(str(order_id)))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        self.body = None


class PayPal:
    def __init__(self):
        self.paypal_webhook_id = settings.PAYPAL_WEBHOOK_ID
        self.paypal_return_url = settings.PAYPAL_RETURN_URL
        self.paypal_base_url = SandboxEnvironment.SANDBOX_API_URL if settings.PAYPAL_TEST else LiveEnvironment.SANDBOX_API_URL
        auth_code = (settings.PAYPAL_CLIENT_ID + ":" + settings.PAYPAL_SECRET_KEY).encode('ascii')
        auth_code = base64.b64encode(auth_code).decode('ascii')
        headers = {
            'Accept': "application/json",
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept-Language': "en_US",
            'Authorization': "Basic {}".format(auth_code)
        }
        body = "grant_type=client_credentials"
        url = self.paypal_base_url + "/v1/oauth2/token"
        r = requests.post(url, headers=headers, data=body)
        r.raise_for_status()
        response = r.json()
        self.headers = {
            "authorization": "Bearer {}".format(response["access_token"])
        }

    def __paypal_client(self):
        return PayPalHttpClient(self.environment)


    def __post(self, endpoint, body, raw=False):
        url = self.paypal_base_url + endpoint
        if raw:
            r = requests.post(url, headers=self.headers, data=body)
        else:
            r = requests.post(url, headers=self.headers, json=body)
        r.raise_for_status()
        return r.json()

    def __get(self, endpoint):
        url = self.paypal_base_url + endpoint
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    # Creates a subscription in paypal.  User is given link to approve the recurring billing.
    def create_subscription(self, user, subscription_plan):
        today = datetime.date.today()
        paypal_plan_id = subscription_plan.paypal_plan_id
        plan_type = subscription_plan.name.upper()
        plan_cost = subscription_plan.price
        next_billing_date, initial_charge_multiplier = subscription_date_utils.get_initial_subscription_billing_date(plan_type, today)
        body = {
            "custom_id": user.id,
            "plan_id": paypal_plan_id,
            "payment_preferences": {
                "setup_fee": {
                    "value": round(initial_charge_multiplier * plan_cost, 2),
                    "currency_code": "USD"
                }
            }
        }
        if len(self.paypal_return_url) > 0:
            body["appliction_context"] = {
                "return_url": self.paypal_return_url
            }

        logging.info("next billing date: {}, multiplier: {}".format(next_billing_date, initial_charge_multiplier))
        if next_billing_date != today:
            body["start_time"] = next_billing_date.isoformat() + "T00:00:00Z"

        response = self.__post("/v1/billing/subscriptions", body)
        for link in response["links"]:
            if link["rel"] == "approve":
                return link["href"]
        return None

    def verify_webhook_signature(self, raw_hook, headers):
        logging.info("Verifying webhook signature....")
        hook = json.loads(raw_hook)
        body = {
           "auth_algo": headers['paypal-auth-algo'],
           "cert_url": headers["paypal-cert-url"],
           "transmission_id": headers["paypal-transmission-id"],
           "transmission_sig": headers["paypal-transmission-sig"],
           "transmission_time": headers["paypal-transmission-time"],
           "webhook_id": self.paypal_webhook_id,
           "webhook_event": hook
        }
        logging.info("Validating hook...")
        response = self.__post("/v1/notifications/verify-webhook-signature", body)
        if response["verification_status"] != "SUCCESS":
            error_message = "Failed to validate webhook signature."
            logging.warning(error_message)
            logging.warning("Response from Paypal api:")
            logging.warning(response)
            raise Exception(error_message)
        return hook

    def process_subscription_payment_webhook(self, raw_hook, headers):
        hook = self.verify_webhook_signature(raw_hook, headers)
        event_type = hook["event_type"]
        if event_type == "PAYMENT.SALE.COMPLETED" and "resource" in hook and "billing_agreement_id" in hook["resource"] \
                and hook["resource"]["billing_agreement_id"] is not None:
            subscription_id = hook["resource"]["billing_agreement_id"]
            subscription = self.get_subscription(subscription_id)
            user_id = subscription["custom_id"]
            paypal_plan_id = subscription["plan_id"]
            amount_paid = hook["resource"]["amount"]["total"]
            user = User.objects.get(id=user_id)
            user_subscription = UserSubscription.objects.get(user_id=user_id)
            plan = SubscriptionPlan.objects.get(paypal_plan_id=paypal_plan_id)
            expires_at = subscription["billing_info"]["next_billing_time"]
            expires_at = dateutil.parser.isoparse(expires_at)
            payment_id = hook["id"]
            payment_gateway = "paypal"
            if subscription_date_utils.should_suspend_subscription(plan.name.upper(), expires_at):
                expires_at = subscription_date_utils.get_next_start_of_hurricane_season()
                reason = "We are temporarily pausing billing on your QRISQ subscription until the next hurricane season begin on June 1st. You may continue to access the qrisq website in the meantime."
                self.suspend_subscription(subscription_id, reason)
            user_payment = UserPayment(
                user=user,
                payment_id=payment_id,
                payment_gateway=payment_gateway,
                price=amount_paid,
                subscription_id=subscription_id,
                user_subscription=user_subscription,
                expires_at=expires_at.date().isoformat() + "T11:59:59Z"
            )
            return user_payment
        return None

    def get_subscription(self, subscription_id):
        return self.__get("/v1/billing/subscriptions/{}".format(subscription_id))

    def resume_subscription(self, subscription_id, reason):
        body = {
            "reason": reason
        }
        self.__post("/v1/billing/subscriptions/{}/activate".format(subscription_id), body)

    def suspend_subscription(self, subscription_id, reason):
        body = {
            "reason": reason
        }
        self.__post("/v1/billing/subscriptions/{}/suspend".format(subscription_id), body)

    def cancel_subscription(self, subscription_id, reason):
        subscription = self.__get("/v1/billing/subscriptions/{}".format(subscription_id))
        status = subscription["status"]
        if status not in ["CANCELLED", "EXPIRED"]:
            body = {
                "reason": reason
            }
            self.__post("/v1/billing/subscriptions/{}/cancel".format(subscription_id), body)
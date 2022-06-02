import time

import requests
import json
import logging
import hmac
import hashlib
import datetime
import base64
import subscriptions.subscription_date_utils as subscription_date_utils
import dateutil.parser
from django.conf import settings
from subscriptions.models import UserPayment, SubscriptionPlan, UserSubscription
from user_app.models import User, UserProfile


class FluidPay(object):

    def __init__(self):
        self.APPROVAL_RESPONSE_CODE = 100
        self.customer_id_prefix = "f"
        self.api_key = settings.FLUID_PAY_API_KEY
        self.webhook_signature = settings.FLUID_PAY_WEBHOOK_SIGNATURE
        if settings.FLUIDPAY_TEST is True or settings.FLUIDPAY_TEST == 'True':
            self.base_url = settings.FLUID_PAY_SANDBOX_URL
        else:
            self.base_url = settings.FLUID_PAY_PRODUCTION_URL
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'credentials': 'include',
            'Authorization': self.api_key
        }

    def __post(self, endpoint, body, raw=False, attempt=1, retries=0):
        url = self.base_url + endpoint
        try:
            if raw:
                r = requests.post(url, headers=self.headers, data=body)
            else:
                r = requests.post(url, headers=self.headers, json=body)
            # r.raise_for_status()
        except:
            if attempt <= retries:
                logging.info("Retry request to {}".format(url))
                time.sleep(attempt)
                return self.__post(endpoint, body, raw, attempt=attempt+1, retries=retries)
            else:
                raise

        return r.json()

    def __delete(self, endpoint):
        url = self.base_url + endpoint
        r = requests.delete(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def __get(self, endpoint, errorOn400=True, return_raw_response=False):
        url = self.base_url + endpoint
        r = requests.get(url, headers=self.headers)
        if r.status_code != 400 or errorOn400:
            r.raise_for_status()
        if return_raw_response:
            return r
        return r.json()

    def verify_webhook_signature(self, raw_hook, headers):
        logging.info("Verifying webhook signature....")
        hook = json.loads(raw_hook)
        header_signature_base64 = headers["Signature"]
        header_signature_base64 += '=' * (-len(header_signature_base64) % 4)
        header_signature = base64.urlsafe_b64decode(header_signature_base64).hex()
        auth_sig = hmac.new(self.webhook_signature.encode('ascii'), raw_hook, hashlib.sha256).hexdigest()

        if header_signature != auth_sig:
            logging.warning("Webhook authorization failed.")
            raise Exception("not authorized")

        return hook

    def process_subscription_payment_webhook(self, raw_hook, headers):
        hook = self.verify_webhook_signature(raw_hook, headers)
        data = hook["data"]
        if data["status"] in ["settled"] and "subscription_id" in "data" and len(data["subscription_id"]) > 0:
            subscription_id = data["subscription_id"]
            user_id = data["customer_id"]
            subscription = self.get_subscription(subscription_id)["data"]
            fluidpay_plan_id = subscription["plan_id"]
            amount_paid = data["amount"]
            expires_at = subscription["next_bill_date"],
            payment_id = data["id"]
            payment_gateway = "fluidpay"

            user = User.objects.objects.get(id=user_id)
            user_subscription = UserSubscription.objects.get(user_id=user_id)
            plan = SubscriptionPlan.objects.get(fluidpay_plan_id=fluidpay_plan_id)

            expires_at = dateutil.parser.isoparse(expires_at)

            if subscription_date_utils.should_suspend_subscription(plan.name.upper(), expires_at):
                expires_at = subscription_date_utils.get_next_start_of_hurricane_season()
                self.update_subscription_bill_date(subscription_id, expires_at)

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

    def update_subscription_bill_date(self, subscription_id, new_bill_date):
        subscription = self.__get("recurring/subscription/{}".format(subscription_id))["data"]
        # We do need to provide a decent subset of data for fluidpay to accept thd updated plan
        updated_subscription = {
            "id": subscription_id,
            "plan_id": subscription["data"]["plan_id"],
            "amount": subscription["data"]["amount"],
            "billing_cycle_interval": subscription["data"]["billing_cycle_interval"],
            "billing_frequency": subscription["data"]["billing_frequency"],
            "billing_days": subscription["data"]["billing_days"],
            "duration": subscription["data"]["duration"],
            "next_bill_date": new_bill_date.strftime('%Y-%m-%d')
        }
        self.__post("recurring/subscription/{}".format(subscription_id), updated_subscription)

    def create_subscription(self, user, validated_data, subscription_plan):
        update_payment_method = False
        customer_id = self.customer_id_prefix + str(user.id)
        user_email = user.email
        tokenizer_token = validated_data.get("token")
        user_subscription = UserSubscription.objects.get(user_id=user.id)
        user_user = User.objects.get(id=user.id)
        user_profile = UserProfile.objects.get(user_id=user.id)

        debug_info = {"customer_id": customer_id}
        response = self.__get("/vault/{}".format(customer_id), errorOn400=False, return_raw_response=True)
        if response.status_code == 400:
            # Customer doesn't exist? Need to create it
            body = {
                "id": customer_id,
                "default_payment": {
                    "token": tokenizer_token
                },
                "default_billing_address": {
                    "first_name": user_user.first_name,
                    "last_name": user_user.last_name,
                    "address_line_1": user_profile.address_line_1,
                    "city": user_profile.city,
                    "state": user_profile.state,
                    "country": "US",
                    "postal_code": user_profile.zip_code,
                    "email": user_email
                }
            }
            response = self.__post("/vault/customer", body, retries=3)
            debug_info["customer_response"] = response
        else:
            response.raise_for_status()
            response = response.json()
            debug_info["customer_response"] = response

        payment_method_id = response["data"]["data"]["customer"]["payments"]["cards"][0]["id"]
        billing_address_id = response["data"]["data"]["customer"]["addresses"][0]["id"]
        today = datetime.date.today()
        plan_type = subscription_plan.name.upper()
        plan_cost = int(subscription_plan.price * 100)
        next_billing_date, initial_charge_multiplier = subscription_date_utils.get_initial_subscription_billing_date(plan_type, today)

        # Charge them for prorated amount upfront
        transaction_data = {
            "processor_id": settings.FLUID_PAY_PROCESSOR_ID,
            "type": "sale",
            "amount": round(initial_charge_multiplier * plan_cost),
            "tax_amount": 0,
            "shipping_amount": 0,
            "currency": "USD",
            "description": "Prorated subscription charge for subscription",
            "email_receipt": True,
            "email_address": user_email,
            "create_vault_record": False,
            "payment_method": {
                "token": tokenizer_token
                # "customer": {
                #     "id": customer_id,
                #     "payment_method_type": "card",
                #     "payment_method_id": payment_method_id,
                #     "billing_address_id": billing_address_id
                # }
            },
            "billing_address": {
                "first_name": user_user.first_name,
                "last_name": user_user.last_name,
                "address_line_1": user_profile.address_line_1,
                "city": user_profile.city,
                "state": user_profile.state,
                "country": "US",
                "postal_code": user_profile.zip_code,
                "email": user_email
            }
        }
        response = self.__post("/transaction", transaction_data)

        if "data" not in response:
            raise Exception(f"Invalid Fluidpay transaction response: {response}")

        debug_info["payment_response"] = response
        payment_id = response["data"]["id"]
        payment_gateway = "fluidpay"
        response_code = response["data"]["response_code"]

        if response_code != self.APPROVAL_RESPONSE_CODE:
            raise Exception("Response code of {} was received from the server, but expected {}".format(response_code, self.APPROVAL_RESPONSE_CODE))

        # Create the subscription record
        body = {
            "plan_id": str(subscription_plan.fluidpay_plan_id),
            "customer": {
                "id": customer_id,
                "payment_method_id": payment_method_id,
                "payment_method_type": "card",
                "billing_address_id": billing_address_id
            },
            "billing_cycle_interval": subscription_plan.duration,
            "billing_days": "1",
            "next_bill_date": next_billing_date.strftime('%Y-%m-%d')
        }
        response = self.__post("/recurring/subscription", body)
        debug_info['subscription_response'] = response
        if "data" not in response:
            raise Exception(f"Invalid Fluidpay subscription response: {response}")
        subscription_id = response["data"]["id"]
        amount_paid = transaction_data["amount"] * .01
        user_payment = UserPayment(
            user=user,
            payment_id=payment_id,
            payment_gateway=payment_gateway,
            price=amount_paid,
            subscription_id=subscription_id,
            user_subscription=user_subscription,
            expires_at=next_billing_date.isoformat() + "T11:59:59Z"
        )
        return user_payment, debug_info

    def get_subscription(self, subscription_id):
        return self.__get("/recurring/subscription/{}".format(subscription_id))

    def suspend_subscription(self, subscription_id):
        return self.__get("/recurring/subscription/{}/status/paused".format(subscription_id))

    def cancel_subscription(self, subscription_id):
        return self.__get("/recurring/subscription/{}/status/cancelled".format(subscription_id))

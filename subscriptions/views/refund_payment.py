import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from subscriptions.fluidpay import FluidPay
from user_app.permissions import IsAdminUser
from user_app.models import User
from user_app.utils import mail_sender

from subscriptions.models import SubscriptionPlan, UserPayment, UserSubscription
from subscriptions.paypal import PayPal

logger = logging.getLogger(__name__)


class RefundPaymentView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get('uid'), is_deleted=False)

            user_payment = UserPayment.objects.filter(user=user).last()
        except ObjectDoesNotExist:
            return Response({
                'message': 'No subscribed user found.'
            }, status=HTTP_400_BAD_REQUEST)

        user_subscription = UserSubscription.objects.get(user=user)
        if user_subscription.is_cancelled:
            return Response({
                'message': "Requested user has cancelled their subscription"
            }, status=HTTP_400_BAD_REQUEST)
        if not user_payment:
            return Response({
                'message': "Requested user has not paid yet."
            }, status=HTTP_400_BAD_REQUEST)
        payment_gateway = user_payment.payment_gateway
        last_transaction_id = user_payment.payment_id
        logger.info("Refunding to account " + user.email)
        if payment_gateway == 'paypal':
            try:
                paypal = PayPal()
                paypal.refund_payment(last_transaction_id, payment_gateway, user)

            except Exception as err:
                error = json.loads(err.message)
                logger.error("Failed refunding paypal to account " + json.dumps(error.get('details')))
                return Response({
                    'message': error.get('message'),
                    'error': "Paypal Refund fail."
                }, status=HTTP_400_BAD_REQUEST)
        elif payment_gateway == 'fluidpay':
            fp = FluidPay()
            amount = {
                "amount": int(user_payment.price)
            }
            amount_json_data = json.dumps(amount)

            response = fp.request_handler('POST', ['transaction', last_transaction_id, 'refund'],
                                          body=amount_json_data)  # refund transaction
            if not response.status_code == 200:
                response_body = response.json()
                response_message = response_body.get('msg', 0)
                return Response({'message': response_message}, status=HTTP_400_BAD_REQUEST)

        user_subscription.cancel_subscription()
        context = {
            'full_name': f"{user.first_name} {user.last_name}",
            'domain': settings.DOMAIN
        }
        try:
            mail_sender(
                template='subscriptions/account_refund.html',
                context=context,
                subject="Subscription price refunded.",
                recipient_list=[user.email]
            )
        except Exception as error:
            logger.error("Failed sending email to user")

        return Response({
            "message": "Refund successful."
        })


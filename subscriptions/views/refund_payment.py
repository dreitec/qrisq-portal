import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user_app.permissions import IsAdminUser
from user_app.models import User
from user_app.utils import mail_sender

from subscriptions.models import SubscriptionPlan, UserPayment, UserSubscription
from subscriptions.paypal import PayPal

logger = logging.getLogger(__name__)


class RefundPaymentView(APIView):
    permission_classes = [IsAdminUser,]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data.get('uid'), is_deleted=False)
            user_payment = UserPayment.objects.filter(user=user).last()
            user_subscription = UserSubscription.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response({
                'message': 'No subscribed user found.'
            })

        payment_gateway = user_payment.payment_gateway
        logger.info("Refunding to account " + user.email)
        if payment_gateway == 'paypal':
            try:
                paypal = PayPal()
                paypal.refund_payment(user_payment.payment_id, payment_gateway, user)

            except Exception as err:
                error = json.loads(err.message)
                logger.error("Failed refunding paypal to account " + json.dumps(error.get('details')))
                return Response({
                    'message': error.get('message'),
                    'error': "Paypal Refund fail."
                }, status=HTTP_400_BAD_REQUEST)

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


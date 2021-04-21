import json

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user_app.permissions import IsAdminUser
from user_app.models import User
from user_app.utils import mail_sender

from subscriptions.models import SubscriptionPlan, UserPayment, UserSubscription
from subscriptions.serializers import SubscriptionPlanSerializer
from subscriptions.paypal import paypal_refund_payment


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()
    permission_classes = [IsAdminUser, ]
    http_method_names = ('get', 'post', 'put', 'delete', 'head', 'options')

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


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
        if payment_gateway == 'paypal':
            try:
                paypal_refund_payment(user_payment.payment_id, payment_gateway, user)
            except Exception as err:
                error = json.loads(err.message)
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
            raise Exception("Error sending email to User.")
        
        return Response({
            "message": "Refund successful."
        })


class CancelSubscriptionView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        
        if not UserSubscription.objects.filter(user=user, is_cancelled=False).exists():
            return Response({
                'message': 'You have not subscribed yet.'
            })

        user_subscription = UserSubscription.objects.get(user=user)
        user_subscription.cancel_subscription()

        context = {
            'full_name': f"{user.first_name} {user.last_name}",
            'domain': settings.DOMAIN
            }
        try:
            mail_sender(
                template='subscriptions/subscription_cancel.html',
                context=context,
                subject="Subscription plan cancelled.",
                recipient_list=[user.email]
            )
        except Exception as error:
            raise Exception("Error sending email to User.")
        
        return Response({
            "message": "Subscription cancelled."
        })

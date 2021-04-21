import json

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user_app.permissions import IsAdminUser
from user_app.models import User
from subscriptions.models import SubscriptionPlan, UserPayment, UserSubscription
from subscriptions.serializers import SubscriptionPlanSerializer
from subscriptions.paypal import paypal_refund_payment
from user_app.permissions import IsAdminUser


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


class RefundPayent(APIView):
    permission_classes = [IsAdminUser,]

    def post(self, request):
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
                user_subscription.cancel_subscription()
            except Exception as err:
                error = json.loads(err.message)
                
                return Response({
                'message': "Paypal Refund fail.",
                'error': error.get('message')
                }, status=HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "Refund successful"
        })
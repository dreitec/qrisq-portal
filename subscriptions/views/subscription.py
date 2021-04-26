import json
import logging

from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from user_app.permissions import IsAdminUser
from user_app.models import User
from user_app.utils import mail_sender

from subscriptions.models import SubscriptionPlan, UserSubscription
from subscriptions.serializers import SubscriptionPlanSerializer

logger = logging.getLogger(__name__)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()
    permission_classes = [IsAdminUser, ]
    http_method_names = ('get', 'post', 'put', 'delete', 'head', 'options')

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


class CancelSubscriptionView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        
        if not UserSubscription.objects.filter(user=user, is_cancelled=False).exists():
            return Response({
                'message': 'You have not subscribed yet.'
            }, status=HTTP_400_BAD_REQUEST)

        logger.info('Cancelling subscription of ' + user.email)
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
            logger.error('Error sending email to account: ' + user.email)
        
        return Response({
            "message": "Subscription cancelled."
        })

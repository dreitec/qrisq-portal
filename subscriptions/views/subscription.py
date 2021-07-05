import json
import logging

from django.conf import settings

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from qrisq_api.pagination import CustomPagination

from user_app.permissions import IsAdminUser
from user_app.models import User
from user_app.utils import mail_sender

from subscriptions.models import SubscriptionPlan, UserSubscription
from subscriptions.serializers import SubscriptionPlanSerializer, AddPaymentInfoSerializer

logger = logging.getLogger(__name__)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all().order_by('price')
    permission_classes = (IsAdminUser,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['id', 'name', 'price', 'duration',]
    http_method_names = ('get', 'post', 'put', 'delete', 'head', 'options')

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


class AddPaymentInfoView(CreateAPIView):
    serializer_class = AddPaymentInfoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as error:
            return Response({
                'message': "Error adding payment information.",
                'error': str(error)}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'message': "Successfully added payment info."})


class CancelSubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

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
        except Exception as err:
            logger.error(f"Error sending email to account {user.email}: {str(err)}")
        
        return Response({
            "message": "Subscription cancelled."
        })

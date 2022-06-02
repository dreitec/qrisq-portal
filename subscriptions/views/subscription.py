from datetime import datetime
import json
import logging
import time
from django.conf import settings
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from billing.models import Billing
from core.service_area import check_billing_city_shape
from qrisq_api.pagination import CustomPagination
from user_app.permissions import IsAdminUser
from user_app.models import User
from user_app.utils import mail_sender
from subscriptions.models import Discount, SubscriptionPlan, UserSubscription, UserPayment
from subscriptions.serializers import SubscriptionPlanSerializer, FluidPayTransactionSerializer
import subscriptions.paypal
import subscriptions.fluidpay
logger = logging.getLogger(__name__)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all().order_by('id')
    permission_classes = (IsAdminUser,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['id', 'name', 'price', 'duration',]
    http_method_names = ('get', 'post', 'put', 'delete', 'head', 'options')

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()

class SubscriptionPlanDiscountView(APIView):
    def post(self, request, *args, **kwargs):
        lat = request.data.get('lattitude', '')
        lng = request.data.get('longitude', '')
        city = request.data.get('addressCity', '')
        state = request.data.get('addressState', '')
        all_plans = SubscriptionPlan.objects.all().order_by('id')
        result_plans = []
        for plan in all_plans:
            # get discount by state
            cond1 = Q(state=state)
            cond2 = Q(plan=plan)
            filtered_discounts = Discount.objects.filter(cond1 & cond2)
            discount = 0.0
            if len(filtered_discounts) > 0:
                discount = filtered_discounts[0].discount
            
            # get the highest discount by city
            cond3 = Q(city=city)
            cond4 = Q(discount__gt=discount)
            filtered_billings = Billing.objects.filter((cond1 | cond3) & cond4).order_by('-discount')
            for billing_item in filtered_billings:
                if billing_item.shape_file:
                    print(billing_item.shape_file)
                    if check_billing_city_shape('./' + billing_item.shape_file, lat, lng):
                        discount = billing_item.discount
            result_plans.append({
                "id": plan.id,
                "name": plan.name,
                "feature": plan.feature,
                "price": plan.price,
                "duration": plan.duration,
                "discount": discount
            })
            
        return Response(result_plans)

class CancelSubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        logging.info('Cancelling subscription of user ' + str(user.id))
        user_payment = UserPayment.objects.filter(user=user).last()
        cancel_reason = "User requested cancellation."
        logging.info("Remote sub id to cancel... {}".format(user_payment.subscription_id))
        if user_payment.payment_gateway.upper() == "PAYPAL":
            paypal_handler = subscriptions.paypal.PayPal()
            paypal_handler.cancel_subscription(user_payment.subscription_id, cancel_reason)
        elif user_payment.payment_gateway.upper() == "FLUIDPAY":
            fluidpay_handler = subscriptions.fluidpay.FluidPay()
            fluidpay_handler.cancel_subscription(user_payment.subscription_id)

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


class CreateSubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        plan_id = request.data["subscription_plan_id"]
        payment_type = request.data["payment_gateway"].lower()

        if payment_type not in ["paypal", "fluidpay"]:
            return Response({
                'message': "Invalid payment type."
            })

        if not SubscriptionPlan.objects.filter(id=plan_id).exists():
            return Response({
                'message': 'Invalid subscription plan.'
            }, status=HTTP_400_BAD_REQUEST)

        subscription_plan = SubscriptionPlan.objects.get(id=plan_id)

        if payment_type == "paypal":
            paypal_handler = subscriptions.paypal.PayPal()
            approval_url = paypal_handler.create_subscription(user, subscription_plan)
            return Response({
                "approvalUrl": approval_url
            })
        elif payment_type == "fluidpay":
            serializer = FluidPayTransactionSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            fluidpay_handler = subscriptions.fluidpay.FluidPay()
            user_subscription, debug_info = fluidpay_handler.create_subscription(user, request.data, subscription_plan)
            user_subscription.save()
            return Response({
                "message": "approved!",
                **debug_info,
            })


class VerifySubscriptionPaymentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        max_time_seconds = 90
        stop_time = time.time() + max_time_seconds

        # Wait for a payment to be completed (this may take a few moments because of webhooks).
        while time.time() < stop_time:
            # Process the subscription id returned from paypal, if applicable.  This lets us confirm payment immediately
            # rather than wait on webhooks for the first payment, which can take a couple of minutes and potentially leave
            # the user stuck
            paypal_subscription_id = request.GET.get('paypal_subscription_id', None)
            if paypal_subscription_id is not None:
                paypal_handler = subscriptions.paypal.PayPal()
                user_payment = paypal_handler.process_initial_subscription_payment(request.user, paypal_subscription_id)
                if user_payment is not None:
                    user_payment.save()


            user_subscription = UserSubscription.objects.get(user_id=user_id)
            if user_subscription.expires_at is not None and user_subscription.expires_at.timestamp() > datetime.now().timestamp():
                return Response({
                    "expired": False
                })
            time.sleep(3)

        raise Exception("User's payment could not be confirmed.")


class FluidPayWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def has_permission(self, request, view):
        return True

    def post(self, request, *args, **kwargs):
        fluidpay_handler = subscriptions.fluidpay.FluidPay()
        user_payment = fluidpay_handler.process_subscription_payment_webhook(request.body, request.headers)
        if user_payment is not None:
            user_payment.save()
        return Response({ "message": "success" })


class PaypalWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def has_permission(self, request, view):
        return True

    def post(self, request, *args, **kwargs):
        paypal_handler = subscriptions.paypal.PayPal()
        user_payment = paypal_handler.process_subscription_payment_webhook(request.body, request.headers)
        if user_payment is not None:
            user_payment.save()
        return Response({ "message": "success" })

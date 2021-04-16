from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionPlanViewSet, create_order, approve_order, capture_order
from subscriptions.views.fluidpay import get_users, process_transaction

router = SimpleRouter(trailing_slash=False)
router.register('subscription-plans', SubscriptionPlanViewSet, basename="subscription-plans")
# router.register('users-subscriptions', UsersSubscriptionViewSet, basename="users-subscription")

urlpatterns = router.urls

urlpatterns += [
    path("paypal/order", create_order, name="paypal-create-order"),
    path("paypal/approve/<str:order_id>", approve_order, name="paypal-approve-order"),
    path("paypal/capture/<str:order_id>", capture_order, name="paypal-capture-order"),

    path("fluidpay/get-users", get_users, name="fluid_pay_get_users"),
    path("fluidpay/process-transaction", process_transaction, name="fluid_pay_process_transaction"),
]

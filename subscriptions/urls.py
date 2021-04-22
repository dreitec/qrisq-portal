from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionPlanViewSet, RefundPaymentView, CancelSubscriptionView

router = SimpleRouter(trailing_slash=False)
router.register('subscription-plans', SubscriptionPlanViewSet, basename="subscription-plans")
# router.register('users-subscriptions', UsersSubscriptionViewSet, basename="users-subscription")


urlpatterns = router.urls

urlpatterns += [
    # path("paypal/order", create_order, name="paypal-create-order"),
    # path("paypal/approve/<str:order_id>", approve_order, name="paypal-approve-order"),
    # path("paypal/capture/<str:order_id>", capture_order, name="paypal-capture-order"),
    path("refund-payment", RefundPaymentView.as_view(), name="paypal-refund-order"),
    path("cancel-subscription", CancelSubscriptionView.as_view(), name="cancel-subscription"),
]

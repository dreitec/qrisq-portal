from django.urls import path
from rest_framework.routers import SimpleRouter

from subscriptions.views import SubscriptionPlanViewSet, RefundPaymentView, CancelSubscriptionView, \
    AddPaymentInfoView, FluidPayTransaction  # , fluidpay_refund

router = SimpleRouter(trailing_slash=False)
router.register('subscription-plans', SubscriptionPlanViewSet, basename="subscription-plans")
# router.register('users-subscriptions', UsersSubscriptionViewSet, basename="users-subscription")


urlpatterns = router.urls

urlpatterns += [
    path("refund-payment", RefundPaymentView.as_view(), name="refund-payment"),
    path("cancel-subscription", CancelSubscriptionView.as_view(), name="cancel-subscription"),
    path("process-transaction", FluidPayTransaction.as_view(), name="credit-card-process"),
    path('add-payment-info', AddPaymentInfoView.as_view(), name="add_payment_info"),
]

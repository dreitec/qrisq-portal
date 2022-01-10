from django.urls import path
from rest_framework.routers import SimpleRouter

from subscriptions.views import SubscriptionPlanViewSet, CancelSubscriptionView, CreateSubscriptionView, PaypalWebhookView, FluidPayWebhookView, VerifySubscriptionPaymentView

router = SimpleRouter(trailing_slash=False)
router.register('subscription-plans', SubscriptionPlanViewSet, basename="subscription-plans")
# router.register('users-subscriptions', UsersSubscriptionViewSet, basename="users-subscription")


urlpatterns = router.urls

urlpatterns += [
    path("create-subscription", CreateSubscriptionView.as_view(), name="create-subscription"),
    path("cancel-subscription", CancelSubscriptionView.as_view(), name="cancel-subscription"),
    path('webhook-paypal', PaypalWebhookView.as_view(), name="webhook-paypal"),
    path('webhook-fluidpay', FluidPayWebhookView.as_view(), name="webhook-fluidpay"),
    path('verify-subscription-payment', VerifySubscriptionPaymentView.as_view(), name="verify-subscription-payment")
]



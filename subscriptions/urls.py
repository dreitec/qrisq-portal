from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionPlanViewSet

router = SimpleRouter(trailing_slash=False)
router.register('subscription-plans', SubscriptionPlanViewSet, basename="subscription-plans")
# router.register('users-subscriptions', UsersSubscriptionViewSet, basename="users-subscription")

urlpatterns = router.urls

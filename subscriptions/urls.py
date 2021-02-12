from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionViewSet, UsersSubscriptionViewSet

router = SimpleRouter(trailing_slash=False)
router.register('subscriptions', SubscriptionViewSet, basename="subscription")
# router.register('users-subscriptions', UsersSubscriptionViewSet, basename="users-subscription")

urlpatterns = router.urls

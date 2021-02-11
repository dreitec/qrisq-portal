from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionViewSet, UsersSubscriptionViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'/users-subscriptions/?', UsersSubscriptionViewSet, basename="users-subscription")
router.register(r'/?', SubscriptionViewSet, basename="subscription")

urlpatterns = router.urls
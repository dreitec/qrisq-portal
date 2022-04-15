from django.urls import include, path
from rest_framework import routers
from billing.views import BillingViewSet

router = routers.DefaultRouter()
router.register(r"billing", BillingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

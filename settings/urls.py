from django.urls import include, path
from rest_framework import routers
from settings.views import GlobalConfigViewSet

router = routers.DefaultRouter()
router.register(r"global-config", GlobalConfigViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

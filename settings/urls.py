from django.urls import include, path
from rest_framework import routers
from settings.views import GlobalConfigViewSet

urlpatterns = [
  path('global-config', GlobalConfigViewSet.as_view(), name="global-config"),
]

from django.urls import path
from settings.views import GlobalConfigViewSet

urlpatterns = [
  path('global-config', GlobalConfigViewSet.as_view(), name="global-config"),
]

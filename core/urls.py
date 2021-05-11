from django.urls import path
from .views import healthcheck_view, CheckServiceArea
    

urlpatterns = [
    path('health-check', healthcheck_view, name="health-check"),
    path('check-service-area', CheckServiceArea.as_view(), name="check-service-area"),
]

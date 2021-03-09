from django.urls import path
from .views import CheckServiceArea
    

urlpatterns = [
    path('check-service-area', CheckServiceArea.as_view(), name="check-service-area")
]
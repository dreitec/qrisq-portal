from django.urls import path
from .views import CheckServiceArea, PingDragAddress
    

urlpatterns = [
    path('check-service-area', CheckServiceArea.as_view(), name="check-service-area"),

    path('pin-drag', PingDragAddress.as_view(), name="pin-drag-address"),
]

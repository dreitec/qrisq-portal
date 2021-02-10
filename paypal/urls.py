from django.urls import path
from .views import create_order, approve_order, capture_order

urlpatterns = [
    path("order", create_order, name="paypal-create-order"),
    path("approve/<str:order_id>", approve_order, name="paypal-approve-order"),
    path("capture/<str:order_id>", capture_order, name="paypal-capture-order"),
]
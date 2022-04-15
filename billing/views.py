from rest_framework import viewsets
from user_app.permissions import IsAdminUser
from billing.models import Billing
from billing.serializers import BillingSerializer


class BillingViewSet(viewsets.ModelViewSet):
    serializer_class = BillingSerializer
    permission_classes = [IsAdminUser]
    queryset = Billing.objects.all()

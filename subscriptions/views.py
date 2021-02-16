from rest_framework import viewsets

from user_app.permissions import IsAdminUser

from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()
    permission_classes = [IsAdminUser, ]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [permission() for permission in self.permission_classes]

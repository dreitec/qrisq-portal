from rest_framework import viewsets
from user_app.permissions import IsAdminUser
from settings.models import GlobalConfig
from settings.serializers import GlobalConfigSerializer


class GlobalConfigViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalConfigSerializer
    permission_classes = [IsAdminUser]
    queryset = GlobalConfig.objects.all()

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from settings.models import GlobalConfig
from settings.serializers import GlobalConfigSerializer
from user_app.permissions import IsAdminUser

class GlobalConfigViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        global_config = GlobalConfig.objects.all()
        serializer = GlobalConfigSerializer(global_config[0])
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        global_config = GlobalConfig.objects.get(pk=1)
        global_config.lookback_period = request.data.get('lookback_period')
        global_config.lookback_override = request.data.get('lookback_override')
        global_config.active_storm = request.data.get('active_storm')
        global_config.geocode_users = request.data.get('geocode_users')
        global_config.save()

        serializer = GlobalConfigSerializer(global_config)
        return Response(serializer.data)

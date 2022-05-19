from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from settings.models import GlobalConfig
from settings.serializers import GlobalConfigSerializer
from user_app.permissions import IsAdminUser

class GlobalConfigViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    response_data = {}
    def get(self, request, *args, **kwargs):
        global_config = GlobalConfig.objects.all().order_by('-id')
        if len(global_config) < 1:
            default_config = {
                "lookback_period": 24,
                "lookback_override": False,
                "active_storm": False,
                "geocode_users": False,
            }
            serializer = GlobalConfigSerializer(data=default_config)
            serializer.is_valid(raise_exception=True)
            try:
                serializer.save()
            except Exception as error:
                response_data = {}
        else:
            serializer = GlobalConfigSerializer(global_config[0])
            response_data = serializer.data
        return Response(response_data)

    def post(self, request, *args, **kwargs):
        global_config = GlobalConfig.objects.all().order_by('-id')[0]
        global_config.lookback_period = request.data.get('lookback_period')
        global_config.lookback_override = request.data.get('lookback_override')
        global_config.active_storm = request.data.get('active_storm')
        global_config.geocode_users = request.data.get('geocode_users')
        global_config.save()

        serializer = GlobalConfigSerializer(global_config)
        return Response(serializer.data)

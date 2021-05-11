from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from .serializers import ServiceAreaSerializer
from .service_area import service_area_finder as finder


@api_view(['GET'])
@permission_classes([AllowAny,])
def healthcheck_view(request):
    return Response({"message": "QRisq Server is running up!!!"}) 


class CheckServiceArea(APIView):
    serializer_class = ServiceAreaSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return_data = finder(**serializer.validated_data)
        return Response(
            return_data,
            status=HTTP_500_INTERNAL_SERVER_ERROR if return_data['status'] == 500 else HTTP_200_OK
        )

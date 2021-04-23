from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from subscriptions.models import UserPayment
from .serializers import ServiceAreaSerializer, UserProfileSerializer
from .service_area import service_area_finder as finder


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


class PingDragAddress(APIView):
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):

        try:
            if request.user.profile.address_updated >= 1:
                return Response({'message': "Already updated"}, status=HTTP_403_FORBIDDEN)
            if UserPayment.objects.filter(user=request.user).exists():
                return Response({'message': "User payment already exist"}, status=HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            try:
                serializer.save()
            except Exception as error:
                return Response({
                    'message': "pin drag address error",
                    'error': str(error)}, status=HTTP_400_BAD_REQUEST
                )

            return Response({'message': "pin drag address updated"}, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'message': "complete yor profile",
                'error': str(e)}, status=HTTP_400_BAD_REQUEST
            )

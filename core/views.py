from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_201_CREATED, \
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
        subscribed_plan = getattr(request.user, "subscription_plan", None)
        user_payment = getattr(request.user, "capture", None)
        try:
            if request.user.profile.address_updated >= 1:
                return Response({'message': "Already updated"}, status=HTTP_403_FORBIDDEN)
            if user_payment.exists() and not subscribed_plan.is_cancelled:
                serializer = self.serializer_class(data=request.data, context={'request': request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message': "Pin-drag Address Updated"}, status=HTTP_201_CREATED)

            return Response({'message': "Error. Payment does not exist"}, status=HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'message': "User Subscription is Cancelled",
                'error': str(e)}, status=HTTP_403_FORBIDDEN
            )

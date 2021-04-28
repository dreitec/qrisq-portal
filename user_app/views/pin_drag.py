from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from user_app.serializers import PinDragAddressSerializer



class PingDragAddressView(APIView):
    serializer_class = PinDragAddressSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        subscribed_plan = getattr(user, "subscription_plan", None)
        user_payment = getattr(user, "payment", None)

        if user.profile.address_updated >= 1:
            return Response({'message': "Your address has already been changed earlier."}, status=HTTP_403_FORBIDDEN)
        
        if not user_payment.exists() or subscribed_plan.is_cancelled:
            return Response({'message': "Please subscribe for a plan and make the payment."},
                            status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            return Response({
                'message': str(e),
                'error': 'Error Updating Address'}, status=HTTP_400_BAD_REQUEST
            )
        return Response({'message': "Pin-drag Address Updated"})
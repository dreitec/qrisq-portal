from django.core.exceptions import ValidationError

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from user_app.models import UserPingDragAttempt
from user_app.serializers import PinDragAddressSerializer


class PinDragAttemptCounterView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        attempt = UserPingDragAttempt.objects.filter(user=request.user).first()
        return Response({
            'attempt': attempt.attempts if attempt else 0
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            attempt, _ = UserPingDragAttempt.objects.update_or_create(user=user)
            return Response({
                'attempts': attempt.attempts
            })
        except ValidationError as err:
            return Response({
                'message': 'You have exceeded the pin-drag attempts'
            }, status=HTTP_400_BAD_REQUEST)


class PingDragAddressView(CreateAPIView):
    serializer_class = PinDragAddressSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        subscribed_plan = getattr(user, "subscription_plan", None)
        user_payment = getattr(user, "payment", None)

        if not subscribed_plan:
            return Response({'message': "Please subscribe for a plan and make the payment."},
                            status=HTTP_400_BAD_REQUEST)

        if user.profile.address_updated >= 1:
            return Response({'message': "Your address has already been changed earlier."}, status=HTTP_403_FORBIDDEN)

        if (not user_payment.exists() or subscribed_plan.is_cancelled) and (not subscribed_plan.is_free):
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

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from user_app.permissions import IsAdminUser

from subscriptions.models import SubscriptionPlan
from subscriptions.serializers import SubscriptionPlanSerializer, AddPaymentInfoSerializer


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()
    permission_classes = [IsAdminUser, ]
    http_method_names = ('get', 'post', 'put', 'delete', 'head', 'options')

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


class AddPaymentInfoView(CreateAPIView):
    serializer_class = AddPaymentInfoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as error:
            return Response({
                'message': "Error adding payment information.",
                'error': str(error)}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'message': "Successfully added payment info."}, status=HTTP_200_OK)
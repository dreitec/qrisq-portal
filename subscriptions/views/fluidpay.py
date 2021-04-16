from django.db import transaction

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from subscriptions.serializers.fluidpay import FluidPayTransactionSerializer
# from subscriptions.views.paypal import refund_order


class FluidPayTransaction(CreateAPIView):
    serializer_class = FluidPayTransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': "Transaction is success"}, status=HTTP_201_CREATED)

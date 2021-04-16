from django.db import transaction

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from user_app.serializers import SignupSerializer
from subscriptions.views.paypal import refund_order


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as error:
            payment_id = request.data['payment_id']
            refund_order(payment_id)
            return Response({
                'message': "Signup Failed. Please try again in a while",
                'error': str(error)}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'message': "User successfully created. Please check your email"}, status=HTTP_201_CREATED)


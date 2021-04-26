from django.db import transaction

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from user_app.serializers import SignupSerializer


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as error:
            return Response({
                'message': "Signup Failed. Please try again in a while",
                'error': str(error)}, status=HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=HTTP_201_CREATED)



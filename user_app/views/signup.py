from django.db import transaction

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView

from user_app.serializers import SignupSerializer


class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            transaction.savepoint_commit(sid)
        except Exception as error:
            transaction.savepoint_rollback(sid)
            return Response({
                'msg': "Signup Failed.",
                'error': str(error)}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'msg': "User successfully created."}, status=HTTP_200_OK)


from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_app.serializers import UserSerializer, UserBasicSerializer

from user_app.models import User
from django.http import Http404
from rest_framework import status

from user_app.permissions import IsAdminUser

class AccountProfileView(views.APIView):
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserView(views.APIView):
    serializer_class = UserBasicSerializer 
    permission_classes = [IsAdminUser,]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        user.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
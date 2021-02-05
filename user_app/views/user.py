from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserBasicSerializer 
    permission_classes = [IsAdminUser,]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.soft_delete()
        return Response(data='delete success')
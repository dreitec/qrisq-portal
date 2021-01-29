from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_app.serializers import UserSerializer


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
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from user_app.models import User
from user_app.permissions import IsAdminUser
from user_app.serializers import UserSerializer, UserBasicSerializer, ClientUserSerializer
from user_app.utils import mail_sender


class AccountProfileView(APIView):
    permission_classes = [IsAuthenticated,]

    def get_serializer(self, *args, **kwargs):
        self.serializer_class = UserSerializer if self.request.user.is_admin else ClientUserSerializer
        return self.serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer 
    permission_classes = [IsAdminUser,]

    def create(self, request, *args, **kwargs):
        '''
        Create Admin User only
        '''
        self.serializer_class = UserBasicSerializer
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Admin User created",
            "data": response.data
        }
        return response
    
    def perform_create(self, serializer):
        serializer.save(is_admin=True)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.soft_delete()
        return Response({"message": "User Deleted Successfully"})


@api_view(["GET"])
@permission_classes([IsAdminUser,])
def list_admin_users(request):
    queryset = User.objects.filter(is_admin=True, is_deleted=False)
    return Response(UserSerializer(queryset, many=True).data)


@api_view(["GET"])
@permission_classes([IsAdminUser,])
def list_client_users(request):
    queryset = User.objects.filter(is_admin=False, is_deleted=False)
    return Response(ClientUserSerializer(queryset, many=True).data)
 

@api_view(["POST"])
@permission_classes([IsAuthenticated,])
def request_address_change(request):
    new_address = request.data["new_address"]

    if not new_address.strip():
        return Response({'error': "Address field can't be empty"})

    admin_email = settings.ADMIN_EMAIL
    context = {
        'new_address': new_address,
        'old_address': request.user.profile.address,
        'client_email': request.user.email,
        'link': f"{settings.DOMAIN}/api/users/{request.user.id}"
    }
    try:
        mail_sender(
            template='user_app/request_address_change.html',
            context=context,
            subject="Request Address Change",
            recipient_list=[admin_email]
        )
    except Exception as error:
        return Response({'error': "Error sending message."})

    return Response({'message': "Request has been sent to change your address."})

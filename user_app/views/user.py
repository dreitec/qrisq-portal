import json
import requests

from django.conf import settings

from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from django_filters.rest_framework import DjangoFilterBackend

from qrisq_api.pagination import CustomPagination

from user_app.models import User
from user_app.permissions import IsAdminUser
from user_app.serializers import UserSerializer, UserBasicSerializer, ClientUserSerializer, \
    VerifyEmailSerializer, AccountProfileSerializer
from user_app.utils import mail_sender


class AccountProfileView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountProfileSerializer

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_admin:
            return Response(ClientUserSerializer(request.user).data)
        
        return Response(UserSerializer(request.user).data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.data.get('password'):
            user = request.user
            context = {
                'full_name': user.first_name + ' ' + user.last_name,
                'domain': f"{settings.DOMAIN}"
            }
            try:
                mail_sender(
                    template='user_app/password_change.html',
                    context=context,
                    subject="Password Changed Successfully",
                    recipient_list=[user.email]
                )
            except Exception as err:
                logger.error(f"Error sending email: {str(err)}")
        return Response({'message': "Contact Information updated successfully."})


class UserViewSet(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer 
    permission_classes = [IsAdminUser,]
    http_method_names = ('get', 'post', 'put', 'delete', 'head', 'options')

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


class AdminUserListView(ListAPIView):
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser,]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['email', 'first_name', 'last_name', 'id', 'date_joined']
    queryset = User.objects.filter(is_admin=True, is_deleted=False).order_by('id')


class ClientUserListView(ListAPIView):
    serializer_class = ClientUserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser,]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['email', 'first_name', 'last_name', 'id', 'date_joined']
    queryset = User.objects.filter(is_admin=False, is_deleted=False).order_by('id')
 

@api_view(["POST"])
def request_address_change(request):
    admin_email = settings.ADMIN_EMAIL
    user = request.user
    context = {
        'phone': user.profile.phone_number,
        'address': user.profile.address,
        'street_number': user.profile.street_number,
        'city': user.profile.city,
        'state': user.profile.state,
        'zip_code': user.profile.zip_code,
        'client_email': user.email,
        'client_name': user.first_name + ' ' + user.last_name,
        'full_name': "Qrisq Admin",
        'domain': settings.DOMAIN
    }

    ctx = {
        'full_name': user.first_name + ' ' + user.last_name,
        'domain': settings.DOMAIN
    }
    try:
        mail_sender(
            template='user_app/request_address_change.html',
            context=context,
            subject="Request for Address Change",
            recipient_list=[admin_email]
        )
        mail_sender(
            template='user_app/request_address_ack_client.html',
            context=ctx,
            subject="Request for Address Change",
            recipient_list=[admin_email]
        )
    except Exception as error:
        return Response({'error': "Error sending email."})

    return Response({'message': "Request has been sent to change your address."})


class VerifyRecaptchaV3(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        recaptcha_v3_token = request.data.get("token")
        if not recaptcha_v3_token:
            return Response({
                'error': {
                    'token': "This field is required."
                }
            }, status=HTTP_400_BAD_REQUEST)

        response_data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_v3_token
        }
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=response_data)
        if response.status_code == requests.codes.ok:
            success = response.json().get("success")
            if not success:
                message = response.json().get("error-codes")[0]
                return Response({
                'error': {
                    'message': message
                }
            }, status=HTTP_403_FORBIDDEN)

        return Response({ 'success': True })


class VerifyEmail(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({
                'error': {
                    'email': "This field is required."
                }
            }, status=HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({
                'error': {
                    'email': "Email already exists"
                }
            }, status=HTTP_400_BAD_REQUEST)

        return Response({'message': "Email available"})


# class UpdateUserInfoView(APIView):
#     serializer_class = UpdateUserInfoSerializer

#     def put(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data , context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         try:
#             serializer.save()
#         except Exception as error:
#             return Response({
#                 'message': "User update failed.",
#                 'error': str(error)}, status=HTTP_400_BAD_REQUEST)

#         return Response({'message': "User update successfully."})

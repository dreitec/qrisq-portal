import logging

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

from user_app import utils
from user_app.models import User
from user_app.serializers import LoginTokenSerializer, RefreshTokenSerializer, \
    ResetPasswordSerializer, ForgetPasswordSerializer

logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer

    def post(self, request, *args, **kwargs):
        if not User.objects.filter(email=request.data['email'], is_deleted=False).exists():
            return Response({'message': "No active account found with the given credentials"},
                            status=HTTP_401_UNAUTHORIZED)
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

        except Exception as err:
            logger.error(f"Login Failed: {str(err)}")
            return Response({'message': 'No active account found with the given credentials.'},
                            status=HTTP_401_UNAUTHORIZED)


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer


@api_view(['GET',])
def check_token(request):
    return Response({})


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TokenError:
            pass
        return Response({'detail': 'Successfully logged out.'})


class ForgotPasswordView(CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        if not email:
            return Response({"message": "Email is not provided."}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"message": "User not found"}, status=HTTP_400_BAD_REQUEST)

        uid, token = utils.generate_password_reset_token(user)
        context = {
            'email': email,
            'full_name': user.first_name + ' ' + user.last_name,
            'domain': settings.DOMAIN,
            'reset_link': f"{settings.FRONTEND_DOMAIN}/identity/reset-password/?uid={uid}&token={token}",
        }
        try:
            utils.mail_sender(
                template='user_app/reset_password.html',
                context=context,
                subject="Reset Password",
                recipient_list=[email]
            )
        except Exception as error:
            return Response({"message": "Server Error. Please try again in a while."},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Password reset email has been sent. Please check your mail inbox."})


class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        from django.utils.encoding import force_text
        from django.utils.http import urlsafe_base64_decode

        # uid = request.data.get('uid', '')
        uid = self.kwargs.get('uid', '')
        if not uid:
            return Response({'uid': ["This field is required."]}, status=HTTP_400_BAD_REQUEST)
        uid = force_text(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(id=int(uid))
        except Exception:
            return Response({'message': "Requested user not found."}, status=HTTP_403_FORBIDDEN)

        # token = request.data.get('token', '')
        token = self.kwargs.get('token', '')
        if not token:
            return Response({'token': ["This field is required."]}, status=HTTP_400_BAD_REQUEST)

        if not utils.check_reset_token(user=user, token=token):
            return Response({'message': "Invalid token."}, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        context = {
            'full_name': user.first_name + ' ' + user.last_name,
            'domain': f"{settings.DOMAIN}",
        }
        try:
            utils.mail_sender(
                template='user_app/reset_password_success.html',
                context=context,
                subject="Password Reset Successfully",
                recipient_list=[user.email]
            )
        except Exception as err:
            logger.error(f"Error sending email: {str(err)}")

        return Response({'message': "Your password has reset successfully."})

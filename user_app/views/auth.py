from django.contrib.auth.hashers import check_password

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

from user_app import utils
from user_app.models import User
from user_app.serializers import LoginTokenSerializer, RefreshTokenSerializer, ResetPasswordSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer

    def post(self, request, *args, **kwargs):
        if not User.objects.filter(username=request.data['username']).exists():
            return Response({'msg': "No active account found with the given credentials"},
                            status=HTTP_401_UNAUTHORIZED)
        try:
            return super().post(request, *args, **kwargs)

        except Exception as error:
            return Response({'msg': 'No active account found with the given credentials.'},
                            status=HTTP_401_UNAUTHORIZED)


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TokenError as e:
            pass
        return Response({'detail': 'Successfully logged out.'})


class ForgotPasswordView(CreateAPIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        if not email:
            return Response({"msg": "Email is not provided."}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            uid, token = utils.generate_password_reset_token(user)
            context = {
                'email': email,
                'username': user.username,
                'full_name': user.full_name,
                'uid': uid,
                'token': token
            }
            # try:
            #     utils.mail_sender(
            #         template='user_app/reset_password.html',
            #         context=context,
            #         subject="Reset Password",
            #         recipient_list=[email]
            #     )
            # except Exception as error:
            #     return Response({"msg": "Server Error. Please try again in a while."},
            #                     status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"msg": "Password reset email has been sent. Please check your mail inbox."})


class ResetPasswordView(CreateAPIView):
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        from django.utils.encoding import force_text
        from django.utils.http import urlsafe_base64_decode

        uid = request.data.get('uid', '')
        if not uid:
            return Response({'uid': ["This field is required."]}, status=HTTP_400_BAD_REQUEST)
        uid = force_text(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(id=int(uid))
        except Exception as err:
            return Response({'msg': "Requested user not found."}, status=HTTP_403_FORBIDDEN)

        token = request.data.get('token', '')
        if not token:
            return Response({'token': ["This field is required."]}, status=HTTP_400_BAD_REQUEST)

        if not utils.check_reset_token(user=user, token=token):
            return Response({'msg': "Invalid token."}, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': "Your password has reset successfully."})


class ChangePasswordView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            old_password = request.data['old_password']
        except KeyError as error:
            return Response({'old_password': ["This field is required"]}, status=HTTP_400_BAD_REQUEST)

        if not check_password(request.data.get('old_password', ''), user.password):
            return Response({'old_password': ["Invalid old password."]}, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # context = {
        #     'full_name': user.full_name,
        #     'username': user.username,
        # }
        # try:
        #     mail_sender(
        #         template='user_app/password_change.html',
        #         context=context,
        #         subject="Password Changed Successfully",
        #         recipient_list=[user.email]
        #     )
        # except Exception as error:
        #     pass

        return Response({'msg': "Your password has been changed successfully."})

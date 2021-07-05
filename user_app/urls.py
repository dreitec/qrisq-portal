from django.urls import path, include

from rest_framework.routers import SimpleRouter

from user_app.views import LoginView, LogoutView, RefreshTokenView, check_token, \
    ResetPasswordView, ForgotPasswordView, SignupView, AccountProfileView, \
    UserViewSet, AdminUserListView, ClientUserListView, \
    request_address_change, VerifyEmail, PingDragAddressView, SendMessageView, \
    PinDragAttemptCounterView


router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet, basename="users")

urlpatterns = router.urls

urlpatterns += [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),
    path('auth/refresh', RefreshTokenView.as_view(), name="refresh-token"),
    path('auth/check-token', check_token, name="check-token"),
    path('auth/forgot-password', ForgotPasswordView.as_view(), name="forgot-password"),
    path('auth/reset-password/<str:uid>/<str:token>', ResetPasswordView.as_view(), name="reset-password"),

    path('auth/signup', SignupView.as_view(), name="signup"),

    path('auth/account-profile', AccountProfileView.as_view(), name='account-profile'),
    path('admins', AdminUserListView.as_view(), name="admin-users"),
    path('clients', ClientUserListView.as_view(), name="client-users"),

    path('pin-drag-address', PingDragAddressView.as_view(), name="pin-drag-address"),
    path('pin-drag-attempt', PinDragAttemptCounterView.as_view(), name="pin-drag-counter"),
    path('request-address-change', request_address_change, name="request-address-change"),
    path('verify-email', VerifyEmail.as_view(), name="verify-email"),

    path('send-message', SendMessageView.as_view(), name="send-message"),
]

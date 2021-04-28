from django.urls import path, include

from rest_framework.routers import SimpleRouter

from user_app.views import LoginView, LogoutView, RefreshTokenView, \
    ChangePasswordView, ResetPasswordView, ForgotPasswordView, \
    SignupView, AccountProfileView, UserViewSet, list_admin_users, list_client_users, \
    request_address_change, verify_email, PingDragAddressView, UpdateUserInfoView
    

router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet, basename="users")

urlpatterns = router.urls

urlpatterns += [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),
    path('auth/refresh', RefreshTokenView.as_view(), name="refresh-token"),
    path('auth/change-password', ChangePasswordView.as_view(), name="change-password"),
    path('auth/forgot-password', ForgotPasswordView.as_view(), name="forgot-password"),
    path('auth/reset-password/<str:uid>/<str:token>', ResetPasswordView.as_view(), name="reset-password"),

    path('auth/signup', SignupView.as_view(), name="signup"),

    path('auth/account-profile', AccountProfileView.as_view(), name='account-profile'),
    path('admins', list_admin_users, name="admin-users"),
    path('clients', list_client_users, name="client-users"),

    path('pin-drag-address', PingDragAddressView.as_view(), name="pin-drag-address"),
    path('request-address-change', request_address_change, name="request-address-change"),

    path('verify-email', verify_email, name="verify-email"),

    path('update-info', UpdateUserInfoView.as_view(), name="update-user-info"),
]

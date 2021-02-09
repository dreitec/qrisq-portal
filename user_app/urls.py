from django.urls import path, include

from rest_framework.routers import SimpleRouter

from user_app.views import LoginView, LogoutView, RefreshTokenView, \
    ChangePasswordView, ResetPasswordView, ForgotPasswordView, \
    SignupView, AccountProfileView, UserViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename="User")

urlpatterns = router.urls

urlpatterns += [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),
    path('auth/refresh', RefreshTokenView.as_view(), name="refresh-token"),
    path('auth/change-password', ChangePasswordView.as_view(), name="change-password"),
    path('auth/forgot-password', ForgotPasswordView.as_view(), name="forgot-password"),
    path('auth/reset-password', ResetPasswordView.as_view(), name="reset-password"),

    path('auth/signup', SignupView.as_view(), name="signup"),

    path('auht/account-profile', AccountProfileView.as_view(), name='account-profile'),
]

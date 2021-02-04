from django.urls import path

from user_app.views import LoginView, LogoutView, RefreshTokenView, \
    ChangePasswordView, ResetPasswordView, ForgotPasswordView, \
    SignupView, AccountProfileView

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('refresh', RefreshTokenView.as_view(), name="refresh-token"),
    path('change-password', ChangePasswordView.as_view(), name="change-password"),
    path('forgot-password', ForgotPasswordView.as_view(), name="forgot-password"),
    path('reset-password', ResetPasswordView.as_view(), name="reset-password"),

    path('signup', SignupView.as_view(), name="signup"),

    path('account-profile', AccountProfileView.as_view(), name='account-profile'),
]
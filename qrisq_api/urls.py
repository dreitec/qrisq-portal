from django.urls import path, include


urlpatterns = [
    path('api/auth/', include('user_app.urls')),
    path('api/paypal/', include('paypal.urls')),
]

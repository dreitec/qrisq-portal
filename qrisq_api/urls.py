from django.urls import path, include


urlpatterns = [
    path('api/', include('user_app.urls')),
    path('api/paypal/', include('paypal.urls')),
]

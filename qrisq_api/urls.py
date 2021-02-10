from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='QRisq v2.0 API')


urlpatterns = [
    # path('api', schema_view, name='list-out'),
    path('api/', include('user_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
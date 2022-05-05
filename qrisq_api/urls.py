from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from .swagger import get_schema
from .static_file_handler import static_file_server


urlpatterns = [
    path('api/', include('core.urls')),
    path('api/', include('user_app.urls')),
    path('api/', include('subscriptions.urls')),
    path('api/', include('storm.urls')),
    path('api/', include('billing.urls')),
    path('api/', include('settings.urls')),
] + static(settings.MEDIA_URL, view=static_file_server, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^api/swagger$', get_schema.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
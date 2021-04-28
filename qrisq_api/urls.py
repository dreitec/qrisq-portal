from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from rest_framework import permissions

from .swagger import get_schema


urlpatterns = [
    path('api/', include('core.urls')),
    path('api/', include('user_app.urls')),
    path('api/', include('subscriptions.urls')),
    path('api/', include('storm.urls')),
]

if settings.DEBUG:
  
    urlpatterns += [
        re_path(r'^api/swagger$', get_schema.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
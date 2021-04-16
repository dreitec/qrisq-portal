"""
view for swagger
"""
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
 
swagger_info = openapi.Info(
    title="Qrisq API",
    default_version='v1',
    description="""Qrisq API""",
    terms_of_service="",
    contact=openapi.Contact(email="engineering@outcodesoftware.com"),
)
 

get_schema = get_schema_view(
    validators=['ssv', 'flex'],
    public=False,
    permission_classes=(permissions.AllowAny,),
)
 
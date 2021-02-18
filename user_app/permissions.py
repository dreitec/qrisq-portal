from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
 
class IsAdminUser(permissions.BasePermission):
    """
    Permission class to allow only superusers and admin user
    """
 
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        user = request.user
        return user.is_superuser or user.is_admin
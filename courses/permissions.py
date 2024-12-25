from rest_framework import permissions
from accounts.models import UserRole


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name=UserRole.TEACHER).exists() or request.user.is_superuser
    
class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
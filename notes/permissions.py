from rest_framework import permissions


class IsOwnerOrAdminOrShared(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """Allow read access to owner, shared users, and admin users."""
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user or request.user in obj.shared_with.all() or request.user.is_staff
        return obj.user == request.user or request.user in obj.shared_with.all() or request.user.is_staff
    
class IsVersionAccessible(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """Allow read access to owner, shared users, and admin users."""
        if request.method in permissions.SAFE_METHODS:
            return obj.note.user == request.user or request.user in obj.note.shared_with.all() or request.user.is_staff
        return obj.note.user == request.user or request.user in obj.note.shared_with.all() or request.user.is_staff
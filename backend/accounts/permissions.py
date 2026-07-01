from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrTechnician(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_technician
        )


class IsOwnerOrStaff(BasePermission):
    """Allow ticket owner (created_by) to read/edit their own ticket; staff (admin/technician) get full access."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin or request.user.is_technician:
            return True
        if request.method in SAFE_METHODS:
            return obj.created_by_id == request.user.id
        return obj.created_by_id == request.user.id

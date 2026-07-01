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
    """Allow ticket owner (created_by) to read their own ticket; only staff (admin/technician) can modify."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin or request.user.is_technician:
            return True
        if request.method in SAFE_METHODS:
            return obj.created_by_id == request.user.id
        return False


def user_can_access_ticket(user, ticket):
    """Staff can access any ticket; regular users only their own."""
    return user.is_admin or user.is_technician or ticket.created_by_id == user.id

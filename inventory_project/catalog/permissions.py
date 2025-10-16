from rest_framework import permissions

class ReadOnlyOrAuthenticatedWrite(permissions.BasePermission):
    """
    SAFE_METHODS (GET/HEAD/OPTIONS) are allowed for everyone.
    Write methods (POST/PUT/PATCH/DELETE) require an authenticated user.
    """

    def has_permission(self, request, view):
        # Allow all safe (read-only) methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Require authentication for write operations
        return bool(request.user and request.user.is_authenticated)

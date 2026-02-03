from rest_framework import permissions


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows read access to anyone (or authenticated),
    but write (update/delete) only to the review's owner.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request (or require auth if you prefer)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for owner
        return obj.user == request.user
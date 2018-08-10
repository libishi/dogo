from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "you must be the Owner of this advertisement!"
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

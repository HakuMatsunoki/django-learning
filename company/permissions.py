from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view: View, obj: object) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

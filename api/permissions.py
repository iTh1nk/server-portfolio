from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj['user'])
        if (request.user.is_staff):
            return True
        return obj['user'] == str(request.user)

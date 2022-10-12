from rest_framework import permissions


class OnlyAdminSee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class OnlyAdminOrItself(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        print(obj)
        return request.user == obj

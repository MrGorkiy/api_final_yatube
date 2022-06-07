from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class OwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        raise MethodNotAllowed("Добавление новых групп запрещено!")
        # Если сделать как ниже, то статус ошибки возвращается 405, а тесты
        # требуют 403, не понимаю как и где переопределить это, поэтому
        # реализовал так
        # return request.method in permissions.SAFE_METHODS

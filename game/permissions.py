from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет только суперпользователю выполнять изменения (POST, PUT, DELETE).
    Все остальные могут только читать (GET).
    """
    def has_permission(self, request, view):

        # Разрешить всем пользователям только GET-запросы
        if request.method in permissions.SAFE_METHODS:
            return True

        # Суперпользователю разрешено все
        if request.user and request.user.is_superuser:
            return True

        # В остальных случаях доступ запрещен
        return False

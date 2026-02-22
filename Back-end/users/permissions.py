from rest_framework.permissions import BasePermission


class IsAdminGroup(BasePermission):
    #Permite acceso solo a usuarios del grupo 'Administradores' o superusuarios.

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser or
            request.user.groups.filter(name='Administradores').exists()
        )


class IsOwnerOrAdmin(BasePermission):
    #Permite acceso al propietario del objeto o a administradores.

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Administradores').exists():
            return True
        return obj == request.user

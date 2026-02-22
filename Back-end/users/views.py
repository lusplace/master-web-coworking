"""
Vistas para la gestión de usuarios.
Incluye autenticación, registro y administración de usuarios.
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    LoginSerializer, AssignGroupSerializer, PasswordChangeSerializer
)
from .permissions import IsAdminGroup, IsOwnerOrAdmin



#VISTAS DE AUTENTICACIÓN


class RegisterView(generics.CreateAPIView):
    """
    Vista para registro de nuevos usuarios.
    POST /api/users/register/
    Acceso público.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Usuario registrado exitosamente.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Vista para iniciar sesión.
    POST /api/users/login/
    Acceso público.
    
    Retorna un token de autenticación que debe enviarse en el header:
    Authorization: Token <token>
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Crear o obtener el token para el usuario
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Inicio de sesión exitoso.',
                    'token': token.key,
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'La cuenta está desactivada.'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'error': 'Credenciales inválidas.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Vista para cerrar sesión.
    POST /api/users/logout/
    Requiere autenticación.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            'message': 'Sesión cerrada exitosamente.'
        }, status=status.HTTP_200_OK)


#VISTAS DE GESTIÓN DE USUARIOS

class UserListView(generics.ListAPIView):
    """
    Vista para listar todos los usuarios.
    GET /api/users/
    Solo administradores.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar o eliminar un usuario.
    GET/PUT/PATCH/DELETE /api/users/<id>/
    - Ver/Actualizar: Admin o el propio usuario
    - Eliminar: Solo admin
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        # Solo administradores pueden eliminar usuarios
        if not (request.user.is_superuser or
                request.user.groups.filter(name='Administradores').exists()):
            return Response({
                'error': 'No tiene permisos para eliminar usuarios.'
            }, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CurrentUserView(APIView):
    """
    Vista para obtener el perfil del usuario actual.
    GET /api/users/me/
    Requiere autenticación.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class PasswordChangeView(APIView):
    """
    Vista para cambiar la contraseña del usuario actual.
    POST /api/users/change-password/
    Requiere autenticación.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response({
            'message': 'Contraseña actualizada exitosamente.'
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminGroup])
def assign_group_view(request, user_id):
    """
    API View para asignar un grupo a un usuario.
    POST /api/users/<user_id>/assign-group/
    Solo administradores.
    
    Body: { "group_name": "Administradores" | "Empleados" }
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({
            'error': f'Usuario con id {user_id} no encontrado.'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AssignGroupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    group_name = serializer.validated_data['group_name']
    group = Group.objects.get(name=group_name)

    user.groups.clear()
    user.groups.add(group)

    return Response({
        'message': f'Usuario {user.username} asignado al grupo {group_name}.',
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_groups_view(request):
    """
    API View para listar todos los grupos disponibles.
    GET /api/users/groups/
    """
    groups = Group.objects.all().values('id', 'name')
    return Response(list(groups), status=status.HTTP_200_OK)


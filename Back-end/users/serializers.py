"""
Serializadores para la gestión de usuarios.
"""

from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Group.
    """
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User.
    Incluye información de grupos.
    """
    groups = GroupSerializer(many=True, read_only=True)
    group_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'groups', 'group_names',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['date_joined', 'last_login', 'is_staff']

    def get_group_names(self, obj):
        """Retorna los nombres de los grupos del usuario."""
        return list(obj.groups.values_list('name', flat=True))


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializador para registro de nuevos usuarios.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]

    def validate(self, attrs):
        """Valida que las contraseñas coincidan."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden.'
            })
        return attrs

    def create(self, validated_data):
        """Crea un nuevo usuario con la contraseña encriptada."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        #Asignar al grupo de empleados por defecto
        empleados_group = Group.objects.filter(name='Empleados').first()
        if empleados_group:
            user.groups.add(empleados_group)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador para actualizar usuarios.
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializador para cambio de contraseña.
    """
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        """Valida que la contraseña actual sea correcta."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('La contraseña actual es incorrecta.')
        return value


class LoginSerializer(serializers.Serializer):
    """
    Serializador para autenticación de usuarios.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )


class AssignGroupSerializer(serializers.Serializer):
    """
    Serializador para asignar grupo a un usuario.
    """
    group_name = serializers.CharField(required=True)

    def validate_group_name(self, value):
        """Valida que el grupo exista."""
        if not Group.objects.filter(name=value).exists():
            raise serializers.ValidationError(f"El grupo '{value}' no existe.")
        return value


from rest_framework import viewsets
from rest_framework.permissions import AllowAny # O IsAuthenticated seguridad
from .models import Sede, Espacio, Reserva, Pago
from .serializers import (
    SedeSerializer, EspacioSerializer, 
    ReservaSerializer, PagoSerializer
)

class SedeViewSet(viewsets.ModelViewSet):
    """
   Gestión de Sedes.
    """
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer
    permission_classes = [AllowAny] # Cualquiera puede ver las sedes en el frontend

class EspacioViewSet(viewsets.ModelViewSet):
    """
   Gestión de Oficinas.
    """
    queryset = Espacio.objects.all()
    serializer_class = EspacioSerializer
    permission_classes = [AllowAny]

class ReservaViewSet(viewsets.ModelViewSet):
    """
    Gestíon de Reservas.
    """
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [AllowAny]

class PagoViewSet(viewsets.ModelViewSet):
    """
    Gestión de pagos.
    """
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [AllowAny]
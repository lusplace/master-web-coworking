from django.db.models import Q
from rest_framework import serializers
from .models import Sede, Espacio, Reserva, Pago

#  Sedes
class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'  

#  Espacios
class EspacioSerializer(serializers.ModelSerializer):
    # Front-end verá el nombre de la sede, no solo el número ID
    sede_nombre = serializers.ReadOnlyField(source='sede.nombre')

    class Meta:
        model = Espacio
        fields = '__all__'
    # VALIDACIÓN
    def validate_capacidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La capacidad debe ser mayor a cero.")
        return value

    def validate_precio_por_hora(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser un valor negativo.")
        return value


#  Reservas
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        
    # VALIDACIÓN: La fecha de fin debe ser posterior a la de inicio
    def validate(self, data):
        if data['fecha_inicio'] >= data['fecha_fin']:
            raise serializers.ValidationError({
                "fecha_fin": "La fecha de finalización debe ser posterior a la fecha de inicio."
            })
        if data['total_calculado'] < 0:
            raise serializers.ValidationError({
                "total_calculado": "El total no puede ser negativo."
            })
        
        # VALIDACIÓN (Lógica de Disponibilidad)
        # Si existe alguna reserva para el mismo espacio que se cruce en fechas
        solapamientos = Reserva.objects.filter(
            espacio=data['espacio'],
            estado='confirmada'
        ).filter(
            # lógica
            Q(fecha_inicio__lt=data['fecha_fin'], fecha_fin__gt=data['fecha_inicio'])
        )

        # Si se está editando una reserva, excluimos la reserva actual de la búsqueda
        if self.instance:
            solapamientos = solapamientos.exclude(pk=self.instance.pk)

        if solapamientos.exists():
            raise serializers.ValidationError(
                "Este espacio ya está reservado en el horario seleccionado."
            )

        return data    

#  Pagos
class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
        
    # VALIDACIÓN
    def validate(self, data):
        # VALIDACIÓN DE MONTO
        # Verificamos que el pago no supere (por mucho) lo que debe la reserva
        reserva = data['reserva']
        if data['monto'] > reserva.total_calculado:
            # Podrías permitirlo si es una propina, pero normalmente es un error humano
            raise serializers.ValidationError({
                "monto": f"El monto ingresado ({data['monto']}) es mayor al total de la reserva ({reserva.total_calculado})."
            })
        
        if data['monto'] <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a cero.")
            
        return data   
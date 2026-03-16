from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SedeViewSet, EspacioViewSet, ReservaViewSet, PagoViewSet

router = DefaultRouter()

# secciones
router.register(r'sedes', SedeViewSet)
router.register(r'espacios', EspacioViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'pagos', PagoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
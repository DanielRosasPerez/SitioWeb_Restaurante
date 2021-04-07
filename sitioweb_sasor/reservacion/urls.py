from django.urls import path
from .views import mesa_reservacion, pago_completado

app_name = "reservacion_app"

urlpatterns = [
    path('', mesa_reservacion, name="MesaReservacion"),
    path('pagos/', pago_completado, name="Pagos"),
]
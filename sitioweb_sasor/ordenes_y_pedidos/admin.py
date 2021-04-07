from django.contrib import admin

# Register your models here.
from .models import OrdenCliente
@admin.register(OrdenCliente)
class OrdenClienteAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "EmailVerificacion")
    list_display = ("Nombre", "Email", "Status", "Costo_Orden", "Celular", "Orden_Lista", "created_at", "Domicilio")
    search_fields = ("Nombre", "Email",)
    list_filter = ("Status", "Orden_Lista")

from .models import OrdenContenido
@admin.register(OrdenContenido)
class OrdenContenidoAdmin(admin.ModelAdmin):
    readonly_fields = ("Nombre",)
    list_display = ("Nombre", "Email", "Platillo_o_Bebida", "Cantidad_Alimento", "Costo_Alimento", "Costo_Total_x_Alimento")
    search_fields = ("Nombre", "Email")
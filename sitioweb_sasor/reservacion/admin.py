from django.contrib import admin

# Register your models here.
from .models import Reservacion, Mesa
# Modelo 1:
@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    readonly_fields = ("creacion", "actualizacion")
    list_display = ("Nombre", "Dia", "Horario", "Numero_Personas", "Mesas_a_Ocupar", "MesasIndividuales", "Email", "Celular")
    ordering = ("Dia", "Horario", "Nombre")
    search_fields = ("Nombre", "Dia", "Email")
    list_filter = ("Horario",)


# Modelo 2:
class MesaAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "Cantidad_asientos")
    list_display = ("etiqueta", "Cantidad_asientos", "booleano")

admin.site.register(Mesa, MesaAdmin)


# Modelo 3:
# @admin.register(ReservacionMesaManager)
# class ReservacionMesaManagerAdmin(admin.ModelAdmin):
#     readonly_fields = ("created_at", "updated_at", "mesas_a_ocupar")  # En el caso de "mesas_a_ocupar", he decididó dejarlo sin editar para
#     # evitar problemas con las demás bases de datos, dado que si se edita a voluntad y al antojo del cliente, la cantidad de casos que hay
#     # abordar sobre las otras bases de datos crece exponecialmente, ya que estan todas relacionadas. EN CUANTO A LA APP "reservacion" SE REFIERE.
#     list_display = ("servicio_reservacion", "mesas_a_ocupar", "mesa")
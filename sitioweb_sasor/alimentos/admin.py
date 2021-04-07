from django.contrib import admin

# Register your models here.

#############################################
from .models import ComidaRapida

class ComidaRapidaAdmin(admin.ModelAdmin):
    readonly_fields = ("Slug",)
    list_display = ("Tipo", "Nombre", "Precio", "Descripcion")
    ordering = ("Tipo", "Nombre")
    search_fields = ("Nombre",)
    list_filter = ("Activo", "Tipo")
    # prepopulated_fields = {"Slug":("Nombre",)}  # Esta configuración ya no es necesaria dado que el método "save()" que hemos sobrescrito en 
    # el modelo "Platillo" de manea automática completa el campo Slug, aún cuando cambiamos el nombre.

admin.site.register(ComidaRapida, ComidaRapidaAdmin)

#############################################
from .models import Bebida

@admin.register(Bebida)  # Realiza la misma función que "admin.site.register()".
class BebidaAdmin(admin.ModelAdmin):
    readonly_fields = ("Slug",)
    list_display = ("Tipo", "Nombre", "Precio", "Descripcion")
    ordering = ("Tipo", "Nombre")
    search_fields = ("Nombre",)
    list_filter = ("Activo", "Tipo")

#############################################
# from .models import Postre

# @admin.register(Postre)  # Realiza la misma función que "admin.site.register()".
# class PostreAdmin(admin.ModelAdmin):
#     readonly_fields = ("Slug",)
#     list_display = ("Tipo", "Nombre", "Descripcion", "Precio")
#     ordering = ("Tipo", "Nombre", "Nombre")

#############################################
# from .models import Entrada

# @admin.register(Entrada)  # Realiza la misma función que "admin.site.register()".
# class EntradaAdmin(admin.ModelAdmin):
#     readonly_fields = ("Slug",)
#     list_display = ("Tipo", "Nombre", "Descripcion", "Precio")
#     ordering = ("Tipo", "Nombre")

#############################################
# from .models import Antojo

# @admin.register(Antojo)
# class AntojoAdmin(admin.ModelAdmin):
#     readonly_fields = ("Slug",)
#     list_display = ("Nombre", "Tamaño", "Descripcion", "Cantidad_Personas", "Tiempo_Preparacion", "Precio")
#     ordering = ("Nombre",)

#############################################
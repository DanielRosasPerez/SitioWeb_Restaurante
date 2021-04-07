from django.db import models
from django.contrib.auth.models import User


# CREATING A CUSTOM FIELD IN ORDER TO ALLOW INSERT FROM 1 TO 50 PEOPLE:
class IntegerPeopleField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=1, max_value=50, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value, "max_value": self.max_value}
        defaults.update(kwargs)
        return super(IntegerPeopleField, self).formfield(**defaults)


# ¡¡¡CREATE YOUR MODELS HERE!!!:


# MODELO "RESERVACIÓN":
import math
from django.core.validators import RegexValidator
class Reservacion(models.Model):
    Nombre = models.CharField(max_length=100, verbose_name="Reservación a Nombre de")
    Dia = models.DateField(verbose_name="Día")
    Numero_Personas = IntegerPeopleField(min_value=1, max_value=50, verbose_name="Número de Personas")  # CUSTOM FIELD.
    Mesas_a_Ocupar = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    # Para validar el campo "Celular":
    validar_cel_regex = RegexValidator(regex=r'55[0-9]{8}$', message="El número de celular debe comenzar con '55' y tener al menos 10 digitos. \
        Ejemplo: 5534325917")
    Celular = models.CharField(validators=[validar_cel_regex], max_length=10)
    # Siguen los campos restantes:
    Horario = models.TimeField()
    opciones = (("juntas", "Juntas"),("separadas", "Separadas"))
    MesasIndividuales = models.CharField(max_length=10, choices=opciones, default="juntas", verbose_name="Configuración de las Mesas")
    #Vigencia = models.BooleanField(default=True, verbose_name="Reservación Vigente")
    creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación de la Reservación")
    actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización de la Reservación")

    class Meta:
        verbose_name = "Reservación"
        verbose_name_plural = "Reservaciones"
        ordering = ["Dia", "Horario", "Nombre"]  # Ordenamos por Día, Horario y Nombre, este último de forma alfabética, de la A a la Z.

    def __str__(self):
        return self.Nombre

    # def save(self, *args, **kwargs):
    #     """
    #     FÓRMULA PARA CÁLCULAR EL NÚMERO DE MESAS CON BASE EN EL NÚMERO DE PERSONAS EN LA RESERVACIÓN: 
    #     Cantidad_Mesas = (No.Personas - 2) / (Asientos_por_Mesa - 2); DONDE: Asientos_por_Mesa != 2.
    #     """
    #     Asientos_por_Mesa = 4  # No de Asientos con los que cuentan cada mesa del sasor.
    #     resultado = abs((self.Numero_Personas - 2)) / (Asientos_por_Mesa - 2)  # Hacemos uso de "abs()" para cuando No_Personas = 1.
    #     self.Mesas_a_Ocupar = math.ceil(resultado)  # Redondemaso al entero próximo cuando la parte decimal sea mayor a 0.

    #     # NOTA: LA FÓRMULA PREVIA SOLO APLICA CUANDO LAS MESAS SON "CUADRADAS". En cuanto a la variable "Asientos_por_Mesa" != 2, 
    #     # no habrá problema ya que es lógico que ninguna mesa cuadrada o rectangular puede albergar a menos de 4 personas. Por lo que
    #     # el número de asientos siempre será >= 4.

    #     return super(Reservacion, self).save(*args, **kwargs)


# MODELO "MESA":
class Mesa(models.Model):  # Solo se crearán N instancias totales de este método, equivalentes al número de mesas existentes en el restaurant.
    # USAREMOS EL "id" QUE CREA DJANGO POR CADA MESA PARA IDENTIFICARLAS.
    etiqueta = models.CharField(max_length=2, verbose_name="Mesa")  # Se tendrán que poner en las respectivas mesas físicas unas etiquetas.
    booleano = models.BooleanField(verbose_name="Disponible", default=True)
    Cantidad_asientos = models.IntegerField(verbose_name="Cantidad de Asientos", default=4, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        ordering = ["etiqueta"]

    def save(self, *args, **kwargs):  # Para guardar la etiqueta en formato mayúscula.
        self.etiqueta = self.etiqueta.upper()
        return super(Mesa, self).save(*args, **kwargs)

    def __str__(self):
        return self.etiqueta


# MODELO "GESTIÓN RESERVACIÓN MESA":
# import math
# class ReservacionMesaManager(models.Model):  # Este modelo se encargá de relacionar el "Cliente" con la "Mesa".
#     mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="access_to", verbose_name="Mesa(s)")
#     servicio_reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE, related_name="access_to", verbose_name="reservacion")
#     mesas_a_ocupar = models.IntegerField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación de la reservación")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización de la reservación")

#     class Meta:
#         verbose_name = "Relación Reservación-Mesa"
#         verbose_name_plural = "Reservación-Mesa Manager"

#     def __str__(self):
#         return self.servicio_reservacion.Nombre

#     def save(self, *args, **kwargs):
#         """
#         FÓRMULA PARA CÁLCULAR EL NÚMERO DE MESAS CON BASE EN EL NÚMERO DE PERSONAS EN LA RESERVACIÓN: 
#         Cantidad_Mesas = (No.Personas - 2) / (Asientos_por_Mesa - 2); DONDE: Asientos_por_Mesa != 2.
#         """
#         Asientos_por_Mesa = 4  # No de Asientos con los que cuentan cada mesa del sasor.
#         No_Personas = self.servicio_reservacion.Numero_Personas  # Obtenemos el número de personas en la reservación.
#         resultado = abs((No_Personas - 2)) / (Asientos_por_Mesa - 2)  # Hacemos uso de "abs()" para cuando No_Personas = 1.
#         self.mesas_a_ocupar = math.ceil(resultado)  # Redondemaso al entero próximo cuando la parte decimal sea mayor a 0.

#         # NOTA: LA FÓRMULA PREVIA SOLO APLICA CUANDO LAS MESAS SON "CUADRADAS". En cuanto a la variable "Asientos_por_Mesa" != 2, 
#         # no habrá problema ya que es lógico que ninguna mesa cuadrada o rectangular puede albergar a menos de 4 personas. Por lo que
#         # el número de asientos siempre será >= 4.

#         return super(ReservacionMesaManager, self).save(*args, **kwargs)
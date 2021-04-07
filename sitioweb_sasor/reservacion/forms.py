from django import forms
from .models import Reservacion

from datetime import datetime, time
import pytz


# FORM 1:
class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ("Nombre", "Dia", "Numero_Personas", "Email", "Celular", "Horario", "MesasIndividuales")

    def clean_Email(self):  # De esta forma, validamos el campo "Email" directamente en el formulario.
        """
        Si el Email brindado ya existe en la base de datos, regresamos None para evitar la multiplicidad
        del mismo correo. Teniendo así, un correo por cliente sin importar el número de reservaciones que
        esté realice.
        """

        Email = self.cleaned_data.get("Email")
        dominio = Email.split('@')[-1].split('.')
        if dominio[0] in ["gmail", "hotmail", "outlook", "yahoo", "live"] and dominio[1] in ["com", "mx", "live"]:
            # Dado que haremos uso de JS para crear el objecto "Reservacion", he decidido no verificar que el Email exista.
            # if Reservacion.objects.filter(Email=Email).exists():
            #     Email = None
            #     return Email
            return Email
        else:
            raise forms.ValidationError("¡Ingresa un correo electrónico valido, ya sea de 'google', 'hotmail', 'outlook' o 'yahoo'!")
    
    # NOTA: ESTE MÉTODO SE COMPONE DE: "clean_<nombre_del_campo>()" Y SIRVE PARA VALIDAR CUALQUIER CAMPO DIRECTAMENTE
    # EN EL FORMULARIO.

    def clean_Horario(self):
        """
        Verificamos que la hora en la reservación sea congurente. Es decir, si son las 15:00 del día de hoy y la persona reserva
        a las 12:00 del día de hoy, la reservación es incongruente. Sin embargo, si reserva las 15:00 de días posteriores la 
        reservación será congruente. También se verificará que la reservación no se este haciendo los fines de semana.
        """
        
        # Obtenemos la fecha y hora actual en la CDMX al momento de la reservación, con el fin de realizar la comparación:
        time_zone = pytz.timezone("America/Mexico_City")
        current_time = datetime.now(time_zone)  # Especificamos la zona horaria con la finalidad de obtener el horario actual de la CDMX.
        current_date = current_time.strftime("%Y:%m:%d").split(':')
        current_hour = current_time.strftime("%H:%M").split(':')
        
        # Creamos el objecto fecha, con la (vaya la redundacia), fecha y hora exactas al momento de dar click en "Reservar Mesa":
        Current_Date = datetime(year=int(current_date[0]), month=int(current_date[1]), day=int(current_date[2]), hour=int(current_hour[0]), 
        minute=int(current_hour[1]), tzinfo=time_zone)  # Específicamos en el arg "tzinfo" la zona horaria.

        # Obtenemos la fecha y hora en la que se desea realizar la reservación:
        fecha_ = self.cleaned_data.get("Dia").strftime("%Y:%m:%d").split(':')
        Horario_ = self.cleaned_data.get("Horario").strftime("%H:%M").split(':')  # Rescatamos el campo "Horario" para realizar la comparación entre este y la hora actual.

        # Creamos otro objecto fecha, con la (vaya la redundacia), fecha y hora en que se desea realizar la reservación:
        Reservation_Date = datetime(year=int(fecha_[0]), month=int(fecha_[1]), day=int(fecha_[2]), hour=int(Horario_[0]), minute=int(Horario_[1]),
        tzinfo=time_zone)  # En el arg "tzinfo" específicamos la zona horaria.

        # Realizamos la comparación entre ambas fechas. De esta forma sabremos si el horario de reservación es congruente o no y que la reservación
        # no se este realizando el fin de semana:
        if Current_Date <= Reservation_Date and self.cleaned_data.get("Dia").strftime("%A") not in ["Sunday", "Saturday"]:
            return self.cleaned_data.get("Horario")  # En caso de que la reservación sea congruente, regresamos el valor del campo "Horario".
        else:  # Si la reservación no es congruente regresamos el siguiente mensaje de error:
            raise forms.ValidationError("¡Verifica que el horario que estas seleccionando sea válido, es decir, que no estes reservando a las\
                12:00 si son las 12:15 del día de hoy. Por otro lado, recuerda que no hay servicio los fines de semana!")

        # NOTA: DEBEMOS ESPECIFICAR LAS ZONAS HORARIAS QUE SERÁN USADAS PARA CREAR EL OBJECTO "datetime". De otro forma, no podremos realizar
        # la comparación, o en su defecto, obtendremos incongruencias en la misma.
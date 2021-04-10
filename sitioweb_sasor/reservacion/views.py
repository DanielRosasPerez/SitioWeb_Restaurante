from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.
from .forms import ReservacionForm
from .models import Reservacion, Mesa

from datetime import datetime
import pytz, math, json

from django.db.models import Count
from itertools import groupby
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy

# Funciones para crear reservaciones, traducir el nombre de los meses y calcular las mesas a ocupar por cada reservación:

# def cantidad_mesas_a_ocupar(Numero_Personas):
#     """Para calcular el número de mesas que usará un cliente."""

#     if Numero_Personas > cantidad_personas_que_soporta_el_sasor():
#         return 1000  # Regresamos un número enorme, simbolizando que no tenemos mesas suficientes, de esta forma, la única condición de la lógica
#         # que se cumplirá, será la Condición 3.
#     Mesas_Sasor = Mesa.objects.all()
#     Grupo_Mesas = [(cantidad_asientos,list(grupo)) for cantidad_asientos,grupo in groupby(Mesas_Sasor, key=lambda instancia: instancia.Cantidad_asientos)]
#     for lugares, grupo in Grupo_Mesas:
#         if Numero_Personas == lugares:
#             return 1

#     Mesas_a_Ocupar, Bandera = 0, True
#     for lugares, grupo in Grupo_Mesas:
#         Asientos_por_Mesa = lugares  # No. de Asientos con los que cuentan cada mesa del sasor.
#         resultado = abs((Numero_Personas - 2)) / (Asientos_por_Mesa - 2)  # Hacemos uso de "abs()" para cuando No_Personas = 1.
#         Mesas_a_Ocupar_x_Grupo = math.ceil(resultado)  # Redondeamos al entero próximo cuando la parte decimal sea mayor a 0.

#         if Mesas_a_Ocupar_x_Grupo <= len(grupo):
#             if Bandera:
#                 return Mesas_a_Ocupar_x_Grupo
#             return Mesas_a_Ocupar + Mesas_a_Ocupar_x_Grupo
        
#         Mesas_a_Ocupar += len(grupo)
#         No_Max_Personas_x_Grupo = ((Asientos_por_Mesa - 2) * len(grupo))
#         Numero_Personas = Numero_Personas - No_Max_Personas_x_Grupo
#         Bandera = False


def cantidad_mesas_a_ocupar(Numero_Personas, MesasIndividuales):
    """Para calcular el número de mesas que usará un cliente."""

    if MesasIndividuales == "juntas":
        Asientos_por_Mesa = 4  # No. de Asientos con los que cuentan cada mesa del sasor.
        resultado = abs((Numero_Personas - 2)) / (Asientos_por_Mesa - 2)  # Hacemos uso de "abs()" para cuando No_Personas = 1.
        Mesas_a_Ocupar = math.ceil(resultado)  # Redondeamos al entero próximo cuando la parte decimal sea mayor a 0.
        return Mesas_a_Ocupar
    else:
        Asientos_por_Mesa = 4  # No. de Asientos con los que cuentan cada mesa del sasor.
        Mesas_a_Ocupar = math.ceil((Numero_Personas / Asientos_por_Mesa))
        return Mesas_a_Ocupar

# def cantidad_personas_que_soporta_el_sasor():
#     """Para calcular el número máximo de personas que soporta el Sasor basandose en la cantidad de mesas que tiene."""
#     Mesas_Sasor = Mesa.objects.all()
#     Grupo_Mesas = [(cantidad_asientos,list(grupo)) for cantidad_asientos,grupo in groupby(Mesas_Sasor, key = lambda instancia: instancia.Cantidad_asientos)]
#     Maxima_Cantidad_Personas = 0
#     empalmes = 0
#     for lugares, grupo in Grupo_Mesas:
#         Asientos_por_Mesa = lugares
#         Maxima_Cantidad_Personas += ((Asientos_por_Mesa - 2) * len(grupo)) + 2
#         empalmes += 1
#     Maxima_Cantidad_Personas = Maxima_Cantidad_Personas - ((empalmes-1) * 2)
#     return Maxima_Cantidad_Personas

def cantidad_personas_que_soporta_el_sasor(Cantidad_Total_Mesas, MesasIndividuales):
    """Para calcular el número máximo de personas que soporta el Sasor basandose en la cantidad de mesas que tiene."""

    if MesasIndividuales == "juntas":
        Asientos_por_Mesa = 4  # No. de Asientos con los que cuentan cada mesa del sasor.
        No_Max_Personas = ((Asientos_por_Mesa - 2) * Cantidad_Total_Mesas) + 2
        return No_Max_Personas
    else:
        Asientos_por_Mesa = 4  # No. de Asientos con los que cuentan cada mesa del sasor.
        No_Max_Personas = Cantidad_Total_Mesas * Asientos_por_Mesa
        return No_Max_Personas


def crear_reservacion(Nombre, Dia, Numero_Personas, Email, Celular, Horario, Mesas_a_Ocupar, MesasIndividuales):
    nueva_reservacion = Reservacion.objects.create(Nombre=Nombre, Dia=Dia, Numero_Personas=Numero_Personas, Email=Email, Celular=Celular,
    Horario=Horario, Mesas_a_Ocupar=Mesas_a_Ocupar, MesasIndividuales=MesasIndividuales)  # Creamos una instancia del modelo Reservación directamente desde el "view.py".
    nueva_reservacion.save() # Guardamos la nueva instancia creada en la base de datos.

    # print("MEsas UTILIZAR SIN INDEX: ", Mesa.objects.filter(booleano=True).order_by('Cantidad_asientos'))
    # Mesas_A_Utilizar = Mesa.objects.filter(booleano=True).order_by('Cantidad_asientos')[:Mesas_a_Ocupar]
    # print(f"\nMESAS A UTILIZAR:\n{Mesas_A_Utilizar}\n")
    # for Mesa_Sasor in Mesas_A_Utilizar:
    #     Mesa_Sasor.booleano = False
    #     Mesa_Sasor.save()


# def costo_reservacion(Cantidad_Mesas):
#     costo_inicial = 100
#     costo_total = costo_inicial
#     for _ in range(Cantidad_Mesas-1):  # A partir de la segunda mesa se cobrará el 50% por mesa.
#         costo_total += (costo_inicial * 0.5)
#     return str(costo_total)  # Convertimos a string debido a que PayPal en JS solo acepta variables de tipo "str".


def costo_reservacion(Cantidad_Mesas, MesasIndividuales):
    Asientos_por_Mesa = 4
    Costo_x_asiento = 60
    if MesasIndividuales == "separadas":
        costo_total = Costo_x_asiento * Asientos_por_Mesa * Cantidad_Mesas
    else:
        No_Personas = ((Asientos_por_Mesa - 2) * Cantidad_Mesas) + 2
        costo_total = No_Personas * Costo_x_asiento
    return str(costo_total)  # Convertimos a string debido a que PayPal en JS solo acepta variables de tipo "str".

# VISTAS:

def mesa_reservacion(request):
    form_reservacion = ReservacionForm()
    Date_Time = datetime.now(pytz.timezone("America/Mexico_City"))  # De esta forma, sabremos en que día y hora se ha ingresado a la reservación.
    if request.method == "POST":
        form_reservacion = ReservacionForm(data=request.POST)
        #print(f"\nDATA REQUEST:\n{request.POST}\n")
        if form_reservacion.is_valid():  # Verificamos que el formulario se encuentre lleno de manera correcta.
            datos_reservacion = form_reservacion.cleaned_data  # Extraemos los datos del formulario. Se retorna un diccionario.
            Nombre = datos_reservacion["Nombre"]
            Dia = datos_reservacion["Dia"]
            Numero_Personas = datos_reservacion["Numero_Personas"]
            Email = datos_reservacion["Email"]
            Celular = datos_reservacion["Celular"]
            Horario = datos_reservacion["Horario"]
            MesasIndividuales = datos_reservacion["MesasIndividuales"]
            Mesas_a_Ocupar_Cliente = cantidad_mesas_a_ocupar(Numero_Personas, MesasIndividuales)  # Dado que no podemos acceder a esta propiedad hasta que se guarda

            # Logica para saber si hay lugares disponibles o no, en la fecha en que se desea realizar la reservación:
            Cantidad_Mesas = Mesa.objects.all().count()  # Obtenemos el número total de mesas que hay en el restaurante.
            Max_No_Personas = cantidad_personas_que_soporta_el_sasor(Cantidad_Mesas, MesasIndividuales)  # Obtenemos la máxima cantidad de personas que soporta el Sasor.
            Reservaciones = Reservacion.objects.filter(Dia=Dia)  # Nos quedamos solo con las reservaciones del día deseado por el cliente.
            # Obtenemos el número total de mesas ocupadas en el horario deseado por el cliente:
            Mesas_Ocupadas = sum([instancia.Mesas_a_Ocupar if Reservaciones.filter(Horario=Horario) else 0 
                                                    for instancia in Reservaciones.filter(Horario=Horario)])
            # Comparamos cuantas mesas se encuentran disponbles en el horario deseado, con el número de mesas requeridas por el cliente:
            if (Cantidad_Mesas - Mesas_Ocupadas) >= Mesas_a_Ocupar_Cliente:  # Condición 1.
                # Dado que al pasar el objecto a JS, se volverá cadena, opté por convertir de una vez, los datos de tipo "tiempo" 
                # ("Dia" y "Horario"), al formato correspondiente:
                return render(request, 'core/paypal.html', {"Nombre": Nombre, "Dia": Dia.strftime("%Y-%m-%d"), "Numero_Personas": Numero_Personas,
                "Email": Email, "Celular": Celular, "Horario": Horario.strftime("%H:%M"), "Mesas_a_Ocupar": Mesas_a_Ocupar_Cliente,
                "Costo_Reservacion": costo_reservacion(Mesas_a_Ocupar_Cliente, MesasIndividuales), "MesasIndividuales": MesasIndividuales})

            elif Numero_Personas > Max_No_Personas:  # Condición 2.
                # Rederizamos a un nuevo template, en donde imprimimos que no alcanzamos a cubrir la reservación debido a que esta, excede 
                # al número de personas totales, que puede soportar el sasor:
                Max_No_Personas_MJ = cantidad_personas_que_soporta_el_sasor(Cantidad_Mesas, "juntas")
                Max_No_Personas_MS = cantidad_personas_que_soporta_el_sasor(Cantidad_Mesas, "separadas")
                return render(request, "reservacion/exceso_de_personas.html", {"Max_No_Personas": {"mesas_juntas":Max_No_Personas_MJ, 
                                "mesas_separadas": Max_No_Personas_MS}})

            else:  # Condición 3.
                lista_horarios = ["10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00"]  # Listamos los horarios disponibles.

                # Recuperamos las reservaciones en la BD y las agrupamos por "Horario". Únicamente guardamos el "Horario" de aquellas 
                # reservaciones que ya no cuentan con mesas disponibles para cubrir el número de invitados del cliente (si existe alguna): 
                horarios = [hora.strftime("%H:%M") for hora, grupo in groupby(Reservaciones, key=lambda instancia: instancia.Horario) 
                                if (Cantidad_Mesas - sum([g.Mesas_a_Ocupar for g in grupo])) < Mesas_a_Ocupar_Cliente]
                
                # Removemos aquellos horarios restantes en la lista "lista_horarios", en los que las reservaciones están agotadas:
                for hora_reservacion in horarios:
                    lista_horarios.remove(hora_reservacion)

                # Rederizamos a un nuevo template, en donde imprimimos los horarios en donde hay reservaciones disponibles:
                return render(request, "reservacion/disponibilidad_horarios.html", {"disponibilidad": lista_horarios, "dia_reservacion": Dia})

    return render(request, "reservacion/mesa_reservar.html", {"Date_Time": Date_Time, "form": form_reservacion})


from django.contrib import messages
def pago_completado(request):
    body = json.loads(request.body)  # Recuperamos los datos contenidos en body.

    # Una vez el pago ha sido éxitoso, creamos la instancia reservación y la guardamos en la BD:
    crear_reservacion(body["Nombre"], body["Dia"], int(body["Numero_Personas"]), body["Email"], body["Celular"],
    body["Horario"], int(body["Mesas_a_Ocupar"]), body["MesasIndividuales"])

    # Mandamos un correo al cliente con sus datos para que este al pendiente de su reservación:
    # Asunto:
    subject = "¡Reservación Sasor!"

    # Fecha y Horario de la Reservación:
    time_zone = pytz.timezone("America/Mexico_City")
    fecha = body["Dia"].split('-')
    horario = body["Horario"].split(':')
    formato_fecha_reservacion = datetime(year=int(fecha[0]), month=int(fecha[1]), day=int(fecha[2]), hour=int(horario[0]), minute=int(horario[1]),
        tzinfo=time_zone)
    mes_nombre = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    mes_numerico = ("01","02","03","04","05","06","07","08","09","10","11","12")
    mes_en_español = [nombre for nombre,numero in zip(mes_nombre, mes_numerico) if fecha[1] == numero][0]
    fecha_reservacion = formato_fecha_reservacion.strftime(f"%d de {mes_en_español} del %Y a las %H:%M hrs")

    # Email receptor y emisor:
    email_emisor = "daniel020197ss@gmail.com"
    email_destinatario = body["Email"]

    # Mensaje:
    Nota = "Si demora más de 35 minutos en su reservación, Café Sasor volverá a habilitar la(s) mesa(s) para atender a los clientes que lleguen"
    Nota += "\nal restaurante.\nSi desea cancelar su reservación, hágalo con 3 o más días anticipación, de lo contrario, no habrá ningun reembolso."
    Nota += "\nPor su atención, gracias."

    message = f"¡Tu reservación fue registrada con éxito!\nSus datos son los siguientes:\n\nReservación a nombre de:\n{body['Nombre']}"
    message += f"\n\nReservación para el:\n{fecha_reservacion}\n\nCosto de la Reservación:\n${body['Costo']} MXN. (El cargo ya ha sido cubierto)."
    message += f"\n\nNúmero de Personas: {body['Numero_Personas']}\n\nCorreo Sasor:\n{email_emisor}\n\nTel. Sasor:\n(55)58646592"
    if int(body['Numero_Personas']) >= 5:
        message += f"\n\nConfiguración de las Mesas:\n{body['MesasIndividuales'].title()}"
    message += f"\n\n\nNOTA:\n{Nota}\n\n\n¡Ha sido un placer atenderle :)!"

    try:
        send_mail(subject, message, email_emisor, [email_destinatario], fail_silently=False)
    except Exception:
        # mensaje_error = "Hola, SU RESERVACIÓN NO HA SIDO AGENDADA, por favor, NOTIFIQUE AL RESTAURANTE SASOR QUE LA CUENTA DE CORREO NO SE ENCUENTRA"
        # mensaje_error += "\nFUNCIONANDO CORRECTAMENTE.\nEl teléfono de atención se encuentra en la pestaña 'CONTACTANOS'.\nDisculpe las molestias."
        # messages.warning(request, mensaje_error)

        # NO ELIMINAREMOS LA RESERVACIÓN DE LA BD, DEBIDO A QUE EL CARGO POR "PAYPAL" YA SE HA EFECTUADO. ADEMÁS, LO ÚNICO QUE DEBE HACER EL CLIENTE
        # ES MARCAR PARA QUE SE LE PUEDAN BRINDAR SUS RESPECTIVOS DATOS CORRECTAMENTE:
        # reservacion_a_eliminar = Reservacion.objects.filter(Nombre=body["Nombre"]).filter(Email=body["Email"])
        # reservacion_a_eliminar = reservacion_a_eliminar[len(reservacion_a_eliminar)-1]
        # reservacion_a_eliminar.delete()

        response = JsonResponse({"bandera": "there was an error"})
        response.status_code = 500 # To announce that the user isn't allowed to publish
        return response

    response = JsonResponse({"bandera": "LA RESERVACIÓN SE REALIZÓ CON ÉXITO"})
    return response  # NOTA: Dado que estoy ocupando JS para redireccionarnos de forma 
    # directa a la vista "Home", no tiene caso retornar algún valor. Sin embargo, para evitar errores, retornamos una JsonResponse(),
    # esto solo se hace en este tipo de casos, en cualquier otro, SIEMPRE DEBEMOS RETORNAR ALGO, DADO QUE SE TRATA DE UNA VISTA.
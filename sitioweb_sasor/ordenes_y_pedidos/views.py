from django.shortcuts import render
from alimentos.models import ComidaRapida, Bebida
from .models import OrdenCliente, OrdenContenido
from .forms import OrdenClienteForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import send_mail

# NOTA: ¡¡¡AUNQUE ALGUNAS VISTAS ESTEN COMENTADAS, ES IMPORTANTE CHECARLAS PORQUE HAY FORMAS NUEVAS DE USAR COMANDOS EN ELLAS!!!

# NOTA 2: ¡SIEMPRE QUE HAGAMOS USO DE "render()" en lugar de HttpResponseRedirect, NO PODREMOS REGRESAR AL TEMPLATE EN DONDE ESTAMOS RENDERIZANDO
# LOS DATOS QUE QUEREMOS. ESTO ES BASTANTE ÚTIL CUANDO NO QUEREMOS QUE EL USUARIO PUEDA RETORNAR A CUESTIONARIOS, ETC. SIN EMBARGO, SIEMPRE
# QUE SE HAGA USO DE UNA "URL", YA SEA DINÁMICA O ESTÁTICA, EL USUARIO SÍ PODRA RETORNAR AL CUESTIONARIO.!

# Create your views here.

# def acerca(request):
#     return render(request, "ordenes_y_pedidos/acerca_de.html")

# def principal_vista(request):
#     return render(request, "ordenes_y_pedidos/principal.html")


# def carro_compras(request, slug):
#     try:
#         Alimento = ComidaRapida.objects.get(Slug=slug)
#     except:
#         Bebida_ = Bebida.objects.get(Slug=slug)
#         Alimento = None  # Dado que en este caso, Alimento da como resultado error, debemos igualar a un valor booleano.
#     Item = Alimento if Alimento else Bebida_  # Obtenemos el Alimento o Bebida, según corresponda.

#     return render(request, "ordenes_y_pedidos/carrito2.html", {"Alimento": Item})

########################################################################################################

def canasta_compras(request):
    return render(request, 'ordenes_y_pedidos/canasta.html')

########################################################################################################

import json
from django.utils.text import slugify
from django.http import JsonResponse
import numpy as np
def datos_pedido(request):
    try:
        Items = json.loads(request.body)  # Obtenemos la información del pedido. El formato que devuelve es:
        # {'Informacion_Pedido': [{'id': 'Cereal', 'precio': 38, 'CantidadEnCanasta': '7'}, {'id': 'Chilaquiles Verdes', 'precio': 58, 
        # 'CantidadEnCanasta': '3'}]}
    except Exception as error:  # En caso de que no se haya enviado absolutamente nada en el diccionario JSON proveniente de JS.
        print(f"\nERROR:\n{error}\n")
        return HttpResponseRedirect(reverse_lazy("core_app:Home"))
    # else:
    #     key_items = [key for item in Items["Informacion_Pedido"] for key in item.keys()]
    #     print(f"\nKEY ITEMS:\n{key_items}\n")
    #     if 'id' not in key_items:
    #         data_dic = Items["Informacion_Pedido"][0]
    #         N, E = data_dic["Nombre"], data_dic["Email"]
    #         titular_sin_orden = OrdenCliente.objects.filter(Nombre=N).get(Email=E)
    #         titular_sin_orden.delete()  # Dado que el usuario ya ha contestado el cuestionario tiene su canasta vacía, procedemos a borrarlo de la BD.
    #         messages.error(request, "Tu orden no fue procesada debido a que tu canasta esta vacía. Debes volver al 'Menú' y procesar\
    #             nuevamente tu orden.")
    #         return HttpResponseRedirect(reverse_lazy("core_app:Home"))
    
    # Obtenemos los diccionarios secundarios envueltos por los corchetes, es decir, estamos obteniendo una lista con diccionarios:
    Items = Items["Informacion_Pedido"]
    #print(f"\nITEMS:\n{Items}")
    Alimentos, Precios, Cantidades = list(), list(), list()
    for item_diccionario in Items:
        try:
            Alimentos.append(item_diccionario["id"])
            Precios.append(item_diccionario["precio"])
            Cantidades.append(int(item_diccionario["CantidadEnCanasta"]))  # Convertimos a "entero", porque pasamos en JS el valor como str.
        except:  # En caso de que se trate del diccionario con los datos que identifican al cliente que realizo la orden.
            Nombre = item_diccionario["Nombre"]
            Email = item_diccionario["Email"]

    titular = OrdenCliente.objects.filter(Nombre=Nombre).get(Email=Email)  # Dado que "filter()" devuelve un QuerySet en lugar del objeto perse, decidí
    # usar "get()", dado que este último método sí devuelve al objeto en sí.
    Status = titular.Status
    Costo_Total = np.around(sum([precio*cantidad for precio,cantidad in zip(Precios, Cantidades)]), decimals=3)  # Obtenemos el costo total de todo el pedido.
    Costo_Total = Costo_Total + 15.00 if Status == 'sí' else Costo_Total

    # Sustimos el valor por default del costo total del pedido y guardamos los cambios en la BD:
    titular.Costo_Orden = Costo_Total
    titular.save()

    # Mandamos un correo al cliente con sus datos para que este al pendiente y tenga los datos de su ORDEN:

    detalles_pedido = [alimento + ' ($' + str(precio) + ' MXN x unidad)' + " -> Cantidad: " + str(cantidad) + '.' 
    for alimento, precio, cantidad in zip(Alimentos, Precios, Cantidades)]
    detalles_pedido = '\n'.join(detalles_pedido)

    subject = "¡Pedido de Comida Sasor!"
    email_emisor = "cafesasor@gmail.com"
    email_destinatario = Email
    message = f"¡Tu pedido se ha registrado con éxito!\nSus datos son los siguientes:\n\nPedido a nombre de:\n{Nombre}"
    message += f"\n\nElementos del Pedido:\n{detalles_pedido}\n\nPara llevar:\n{Status.upper()}"
    message += f"\n\nCosto Total del Pedido:\n${Costo_Total} MXN. {'Ya se incluyen los $15.00 MXN. Del envío.' if Status == 'sí' else ''}"
    message += f"\n\nCorreo Sasor:\n{email_emisor}\n\nTeléfono Sasor:\n(55)58230198\n\nEN CASO DE QUE SU COMIDA NO SEA PARA LLEVAR, "
    message += "TENEMOS UN LIMITE DE ESPERA DE 2HRS. POR LO QUE, A PARTIR DE QUE REALIZA SU ORDEN TIENE 2HRS PARA ADQUIRIR SU PEDIDO."
    message += "\n\n\nMuchas gracias por su atención !Ha sido un place atenderle :)!"
    send_mail(subject, message, email_emisor, [email_destinatario])

    # Dado que todo ha salido bien, creamos las instancias correspondientes al pedido del cliente en la base de datos:
    for i in range(len(Alimentos)):
        contenido_orden = OrdenContenido.objects.create(id=None, Titular_Orden=titular, Email=Email, Platillo_o_Bebida=Alimentos[i],
                                    Cantidad_Alimento=Cantidades[i], Costo_Alimento=Precios[i], Costo_Total_x_Alimento=Cantidades[i]*Precios[i])
        contenido_orden.save()
    
    return JsonResponse("¡EL PEDIDO SE REALIZÓ CON ÉXITO!", safe=False)

########################################################################################################

import json
from django.contrib import messages
def cuestionario_orden(request):
    Datos_Orden = OrdenClienteForm()  # Creamos una instancia "OrdenClienteForm" para renderizarla en el template dado, en caso
    # de que request.method == "GET".
    if request.method == "POST":  # En caso de que el formulario lleno, haya sido enviado.
        Datos_Orden = OrdenClienteForm(data=request.POST)  # Creamos una instancia "OrdenClienteForm" con los datos del formulario.
        if Datos_Orden.is_valid():
            datos = Datos_Orden.cleaned_data
            Nombre = datos["Nombre"]
            Status = datos["Status"]
            Domicilio = datos["Domicilio"]
            Domicilio = Domicilio if Domicilio and Status == "sí" else None  # En caso de que la comida se quiera consumir o no en el Sasor. 
            Celular = datos["Celular"]
            Email = datos["Email"]
            EV = datos["EmailVerificacion"]

            # Creamos una instancia del modelo "OrdenCliente":
            nueva_orden = OrdenCliente.objects.create(Nombre=Nombre, Status=Status, Domicilio=Domicilio, Celular=Celular, Email=Email, 
                                                        EmailVerificacion = EV)
            nueva_orden.save()  # Guardamos el objeto en la BD.

            messages.success(request, f"¡Tu orden se ha registrado correctamente!\
                {'No tardes, te estamos esperando :)' if Status != 'sí' else 'Llegaremos en breve a tu domicilio :)'}")
            return HttpResponseRedirect(reverse_lazy("core_app:Home"))  # Regresamos a la página "inicio" cuya vista es "Home".

    return render(request, "ordenes_y_pedidos/alimento_orden.html", {"form": Datos_Orden})

########################################################################################################

# from django.contrib import messages
# def comprar_alimento(request, slug):  # La variable "slug" debe tener el mismo nombre y estar escrita en minúsculas que la variable de su
#     # correspondiente "url", para que pueda pasarse a esta vista de forma correcta.
#     # Obtenemos la comida o bebida correspondiente:
#     try:
#         Alimento = ComidaRapida.objects.get(Slug=slug)
#     except:
#         Bebida_ = Bebida.objects.get(Slug=slug)
#         Alimento = None  # Dado que en este caso, Alimento da como resultado error, debemos igualar a un valor booleano.

#     Item = Alimento if Alimento else Bebida_  # Obtenemos el Alimento o Bebida, según corresponda.
#     Datos_Orden = OrdenClienteForm()  # Creamos una instancia "OrdenClienteForm" para renderizarla en el template dado, en caso
#     # de que request.method == "GET".
#     if request.method == "POST":  # En caso de que el formulario lleno, haya sido enviado.
#         Datos_Orden = OrdenClienteForm(data=request.POST)  # Creamos una instancia "OrdenClienteForm" con los datos del formulario.
#         if Datos_Orden.is_valid():
#             datos = Datos_Orden.cleaned_data
#             Nombre = datos["Nombre"]
#             Status = datos["Status"]
#             Domicilio = datos["Domicilio"]
#             Domicilio = Domicilio if Domicilio else None  # En caso de que la comida se desee consumir en el Sasor. 
#             Celular = datos["Celular"]
#             Email = datos["Email"]

#             # Creamos una instancia del modelo "OrdenCliente":
#             Costo = Alimento.Precio if Alimento else Bebida_.Precio  # Obtenemos el costo, ya sea del Alimento o Bebida, según corresponda.
#             nueva_orden = OrdenCliente.objects.create(Nombre=Nombre, Status=Status, Domicilio=Domicilio, Celular=Celular, Email=Email, 
#                                                         Costo_Orden=Costo, Platillo_o_Bebida=Item.Nombre)
#             nueva_orden.save()  # Guardamos el objeto en la BD.

#             # Mandamos un correo al cliente con sus datos para que este al pendiente y tenga los datos de su ORDEN:
#             subject = "¡Pedido de Comida Sasor!"
#             message = f"¡Tu pedido se ha registrado con éxito!\nSus datos son los siguientes:\n\nPedido a nombre de:\n{Nombre}"
#             message += f"\n\nPrecio:\n${Costo} MXN.\n\nNombre {'del Platillo' if Alimento else 'de la Bebida'}:\n{Item}"
#             message += f"\n\nCorreo:\n{Email}\n\n\n¡Ha sido un place atenderle :)!"
#             email_emisor = "cafesasor@gmail.com"
#             email_destinatario = Email
#             send_mail(subject, message, email_emisor, [email_destinatario])

#             messages.success(request, f"¡Tu orden se ha registrado correctamente!\
#                 {'No tardes, te estamos esperando :)' if Status != 'sí' else 'Llegaremos en breve a tu domicilio :)'}")
#             return HttpResponseRedirect(reverse_lazy("core_app:Home"))  # Regresamos a la página "inicio" cuya vista es "Home".

#     return render(request, "ordenes_y_pedidos/alimento_orden.html", {"form": Datos_Orden, "Alimento": Item})

    # NOTA: Siempre que hagamos uso del "CONTEXTO", es decir, que necesitamos renderizar un diccionario de contexto con los objetos
    # recuperados, o cualquier otra variable que deseemos ocupar en los templates; debemos hacer uso de la función "render()". Por otro lado,
    # cuando solo deseamos ser REDIRIGIDOS A UNA VISTA EN ESPECIAL, HAREMOS USO DE LA FUNCIÓN "HttpResponseRedirect()" EN CONJUNTO CON 
    # "reverse_lazy('<nombre_app>:<nombre_vista>')".
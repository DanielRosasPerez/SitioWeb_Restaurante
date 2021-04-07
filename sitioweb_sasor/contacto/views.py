from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse

# Create your views here.
from .forms import ContactoForm
def contacta_con_nosotros(request):
    formulario_informacion = ContactoForm()
    if request.method == "POST":
        formulario_informacion = ContactoForm(data=request.POST)
        if formulario_informacion.is_valid():
            data = formulario_informacion.cleaned_data
            subject = "Nuevo Mensaje de Cliente"
            message = f"Cliente: {data['Nombre']}\nEmail: {data['Email']}\nCelular: {data['Celular'] if data['Celular'] else 'No especificado'}\
                \nMensaje: {data['Mensaje']}"
            email_emisor = "cafesasor@gmail.com"
            email_destinatario = "cafesasor@gmail.com"
            send_mail(subject, message, email_emisor, [email_destinatario])
            return redirect(reverse("contacto_app:Contacto")+"?ok")
        else:
            #return redirect(reverse("contacto_app:Contacto")+"?error")
            return render(request, "contacto/contact.html", {"form": formulario_informacion})
    else:
        return render(request, "contacto/contact.html", {"form": formulario_informacion})
from django import forms
from .models import OrdenCliente

class OrdenClienteForm(forms.ModelForm):
    class Meta:
        model = OrdenCliente
        fields = ("Nombre", "Status", "Domicilio", "Celular", "Email", "EmailVerificacion")

        texto_titular_pedido = "Por favor, brinda tu NOMBRE COMPLETO."  # No es una buena práctica
        # realizar esto, dado que solo se deben declara las variables que influyen directamente en el "form", pero no cabia de forma adecuada el
        # texto completo en el diccionario. ESTA VARIABLE, NO INFLUYE EN ABSOLUTO CON EL FORM, LA USE DE APOYO.

        widgets = {
            "Nombre": forms.TextInput(attrs={"class": "form-control mb-2", "placeholder": texto_titular_pedido, "autocomplete": "off"}),
            "Domicilio": forms.Textarea(attrs={"class": "form-control mb-2", "placeholder": "Ingresa tu domicilio para llevar el pedido."}),
            "Celular": forms.TextInput(attrs={"class": "form-control mb-2", "placeholder": "Ejemplo: 5512598675", "autocomplete": "off"}),
            "Email": forms.EmailInput(attrs={"class":"form-control mb-2", "placeholder":"Ejemplo: correo@gmail.com", "autocomplete":"off"}),
            "EmailVerificacion": forms.EmailInput(attrs={"class":"form-control mb-2", "placeholder":"Ingresa nuevamente tu correo.", 
                                                    "autocomplete":"off"}),
        }

        labels = {
            "EmailVerificacion": "Verificar Email"
        }
    
    def clean_EmailVerificacion(self):
        Email_Original = self.cleaned_data.get("Email")
        Email_Verificacion = self.cleaned_data.get("EmailVerificacion")
        if Email_Original != Email_Verificacion:
            raise forms.ValidationError("¡Los correos no coinciden, por favor, verifica que sean correctos!")
        return Email_Original

from django import forms

from phonenumber_field.formfields import PhoneNumberField
class ContactoForm(forms.Form):
    Nombre = forms.CharField(max_length=80, required=True)
    Email = forms.EmailField(required=True)
    Celular = PhoneNumberField(required=False, help_text="+52 5534363589; No olvides anteponer +52 a tu celular")
    Mensaje = forms.CharField(max_length=2048, required=True)

    # CONCLUSIÓN: Cada que vayamos a usar un FORM previamente realizado en HTML, haremos uso de "forms.Form". Sin embargo,
    # cada que deseemos que Django realice un formulario de forma dinámica basandose en modelo, haremos uso de "forms.ModelForm".
    # Tanto "forms.Form" y "forms.ModelForm" son intercambiables, no hay ningun problema en ello, pero, para mi gusto, funcionan
    # mejor así.

    # NOTA: SI HACEMOS USO DE UN FORMULARIO PREVIAMENTE CREADO, CADA ATRIBUTO "name" DEBE TENER EL MISMO NOMBRE QUE SU RESPECTIO CAMPO
    # EN EL FORM. EL VALOR QUE RELLENA CADA CAMPO, ES AQUEL QUE VA EN EL ATRIBUTO "value". EL CUAL SE OBTIENE DEL CONTENIDO DE CADA CAMPO
    # QUE INGRESA EL USUARIO.
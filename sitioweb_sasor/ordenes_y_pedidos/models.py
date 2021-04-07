from django.db import models

# Create your models here.

from django.core.validators import RegexValidator

class OrdenCliente(models.Model):
    opciones_para_llevar = (("sí", "Sí"),("no", "No"))
    Nombre = models.CharField(max_length=50, verbose_name="Orden a nombre de")
    Status = models.CharField(max_length=2, choices=opciones_para_llevar, default="sí", verbose_name="Pedido Para Llevar")
    Domicilio = models.TextField(blank=True, null=True)
    # Para validar el campo "Celular":
    validar_cel_regex = RegexValidator(regex=r'55[0-9]{8}$', message="El número de celular debe comenzar con '55' y tener al menos 10 digitos. \
        Ejemplo: 5534325917")
    Celular = models.CharField(validators=[validar_cel_regex], max_length=10)
    # Para validar el campo "Email" e "Email_Verificación":
    validar_correo = RegexValidator(regex=r'[\.a-zA-Z0-9_-]*@(gmail|hotmail|outlook|yahoo)\.(com|mx|live)\w*', message="Verifique que haya ingresado\
        de forma correcta su correo. Solo se aceptan correos de 'gmail', 'hotmail', 'outlook' y 'yahoo'.")
    Email = models.EmailField(validators=[validar_correo])
    EmailVerificacion = models.EmailField(verbose_name="Email de Verificación")  # JS se encargará de verificar que no se pueda pegar el correo 
    # original en este campo. La verificacion de que ambos correos sean iguales se hará en "forms.py".
    # Continuan los campos:
    Costo_Orden = models.FloatField(default=1, verbose_name="Costo Total del Pedido")
    # opciones = (("sí", "SÍ"),("no", "NO"))
    # Orden_Lista = models.CharField(max_length=2, choices=opciones, default="no", verbose_name="Orden Lista")  # Para que el personal del Sasor sepa que ordenes ya han sido preparadas.
    Orden_Lista = models.BooleanField(default=False, verbose_name = "Orden Ya Lista")
    # Campos de creación y actualización:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Realización de la Orden")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización de la Orden")

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "1.Ordenes"
        ordering = ["created_at"]  # Ordenamos de la orden más antigua a la más reciente.

    def __str__(self):
        return self.Nombre

    # NOTE: MORE INFO ABOUT "HOW TO STORE PHONE NUMBERS" AT:
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models/27534377


class OrdenContenido(models.Model):
    """
    Este modelo no será usado para calcular costos totales, obtener la totalidad de platillos distintos para un solo cliente, etc.
    """

    # Dado que cada orden puede contener múltiples platillos, decidimos usar ForeignKey:
    Titular_Orden = models.ForeignKey(OrdenCliente, on_delete=models.CASCADE, related_name="orden_contenido")  # Cuando se borre la orden del cliente
    # en el modelo "OrdenCliente", todos sus platillos, etc. Serán borrados también de este modelo.
    
    # Continuan los campos:
    Nombre = models.CharField(max_length=50, verbose_name="Orden a Nombre de")
    Email = models.EmailField()  # La única razón por la que decidimos hacer uso del "MAIL" es para evitar algún posible detalle con los homónimos.
    Platillo_o_Bebida = models.CharField(max_length=100, verbose_name="Platillo o Bebida")
    Cantidad_Alimento = models.IntegerField(default=1, verbose_name="Cantidad")
    Costo_Alimento = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Precio Unitario")
    Costo_Total_x_Alimento = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cantidad x Precio Unitario")

    class Meta:
        verbose_name = "Contenido_Orden"
        verbose_name_plural = "2.Contenido_Ordenes"

    def __str__(self):
        return self.Titular_Orden.Nombre

    def save(self, *args, **kwargs):
        self.Nombre = self.Titular_Orden.Nombre
        super(OrdenContenido, self).save(*args, **kwargs)
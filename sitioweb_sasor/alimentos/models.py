from django.db import models

# Create your models here.

from django.utils.text import slugify
from ckeditor.fields import RichTextField

class CaracteristicasComunes(models.Model):
    Nombre = models.CharField(max_length=255, unique=True)  # Nombre del platillo/postre/bebida/etc. El nombre debe ser ÚNICO.
    Descripcion = RichTextField(max_length=2048, verbose_name="Descripción")
    Precio = models.DecimalField(max_digits=6, decimal_places=2)
    Slug = models.SlugField(max_length=255)  # Este campo nos permitirá crear URLs amigables.
    Activo = models.BooleanField(default=False)  # De esta forma, el admin del Sasor podrá seleccionar que platillos y bebidas habilitar 
    # para tal día. Estos platillos y bebidas son las que se mostrarán en el día deseado.

    class Meta:
        abstract = True  # De esta forma Django no tomará este modelo en cuenta para la migración. No es necesario ya que estamos
        # representando las características comúnes que tienen los productos ofrecidos por la cocina.

#########################################################################################

# class Antojo(CaracteristicasComunes, models.Model):
#     Tamaños = (("grande", "Grande"), ("mediana", "Mediana"), ("chica", "Chica"))
#     Tamaño = models.CharField(max_length=30, choices=Tamaños, default="Mediana")
#     Tiempo_Preparacion = models.CharField(max_length=100, verbose_name="Tiempo de Preparación", default="Antojo Listo")
#     Cantidad_Personas = models.IntegerField(default=1)  # Número de personas para las cuales rinde el antojo.
#     Imagen = models.ImageField(upload_to="antojos/", blank=True, null=True)

#     class Meta:
#         verbose_name = "Antojo"
#         verbose_name_plural = "Antojos"
#         ordering = ["Nombre",]  # Ordenamos alfabéticamente por su nombre de la A a la Z.

#     def __str__(self):
#         return self.Nombre

#     def save(self, *args, **kwargs):
#         self.Slug = slugify(self.Nombre)
#         super().save(*args, **kwargs)

#########################################################################################

class ComidaRapida(CaracteristicasComunes, models.Model):  # Plato fuerte.
    Tipo_de_Alimento = (("desayuno", "Desayuno"), ("comida", "Comida"))
    Tipo = models.CharField(max_length=30, choices=Tipo_de_Alimento, default="Comida")
    Tiempo_Preparacion = models.CharField(max_length=100, verbose_name="Tiempo de Preparación en horas", default="Platillo Listo")
    Imagen = models.ImageField(upload_to="comida_rapida/", blank=True, null=True)  # Este campo tiene la función de guardar una imagen de la comida.
    # La imagen agregada por cada instancia Platillo creada, se guardará dentro "media" en la carpeta "platillos" (está última
    # se creará automáticamente con la primer instancia generada).

    class Meta:
        verbose_name = "Comida Rápida"  # Nombre que se mostrará en la opción (en el panel admin), "AÑADIR <verbose_name> +".
        verbose_name_plural = "Comidas"  # Nombre que tomará esté modelo en la columna de la app "alimentos".
        ordering = ["Tipo", "Nombre"]  # Ordenamos alfabéticamente por su nombre de la A a la Z.

    def __str__(self):
        return self.Nombre  # De esta forma, mostramos como nombre de la instancia el valor contenido en el campo "Nombre".

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Nombre)
        super().save(*args, **kwargs)  # Sobrescribimos el método "save()" de la clase padre "Model" y lo ejecutamos.

# NOTA: CUANDO TENGAMOS PROBLEMAS AL MIGRAR NUESTRO MODELO A LA BASE DE DATOS DEBIDO AL CAMBIO EN LA CARACTERÍSTICA DE UN CAMPO.
# POR EJEMPLO; QUE ANTERIORMENTE UN CAMPO TENGA "NULL", PERO DESPUÉS SUSTITUYAMOS "NULL" POR "DEFAULT=1"; CONSULTAR LA SIGUIENTE LIGA:
# https://stackoverflow.com/questions/40353649/django-migrate-error-typeerror-expected-string-or-bytes-like-object/50463466

#########################################################################################

# class Entrada(CaracteristicasComunes, models.Model):
#     Tipo_de_Entrada = (("desayuno", "Desayuno"), ("comida", "Comida"), ("cena", "Cena"))
#     Tipo = models.CharField(max_length=30, choices=Tipo_de_Entrada, default="Comida")
#     Imagen = models.ImageField(upload_to="entradas/", blank=True, null=True)

#     class Meta:
#         verbose_name = "Entrada"
#         verbose_name_plural = "Entradas"
#         ordering = ["Tipo", "Nombre"]

#     def __str__(self):
#         return self.Nombre

#     def save(self, *args, **kwargs):
#         self.Slug = slugify(self.Nombre)
#         super(Entrada, self).save(*args, **kwargs)

#########################################################################################

# class Postre(CaracteristicasComunes, models.Model):
#     Tipo_de_Postre = (("desayuno", "Desayuno"), ("comida", "Comida"), ("cena", "Cena"))
#     Tipo = models.CharField(max_length=30, choices=Tipo_de_Postre, default="Comida")
#     Imagen = models.ImageField(upload_to="postres/", blank=True, null=True)

#     class Meta:
#         verbose_name = "Postre"
#         verbose_name_plural = "Postres"
#         ordering = ["Tipo", "Nombre"]

#     def __str__(self):
#         return self.Nombre

#     def save(self, *args, **kwargs):
#         self.Slug = slugify(self.Nombre)
#         super().save(*args, **kwargs)  # Sobrescribimos el método save() de la clase padre "Model" y lo ejecutamos.

#########################################################################################

class Bebida(CaracteristicasComunes, models.Model):
    Tipo_de_Bebida = (("café", "Café"), ("refresco", "Refresco"), ("alcohólica", "Alcohólica"), ("agua", "Agua"))
    Tipo = models.CharField(max_length=255, choices=Tipo_de_Bebida, default="Agua")  # El tipo de bebida (refresco, café, etc).
    Imagen = models.ImageField(upload_to="bebidas/", blank=True, null=True)

    class Meta:
        verbose_name = "Bebida"
        verbose_name_plural = "Bebidas"
        ordering = ["Tipo", "Nombre"]

    def __str__(self):
        return self.Nombre

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Nombre)
        super().save(*args, **kwargs)  # Sobrescribimos el método "save()" de la clase padre "Model" y lo ejecutamos.


#############################################################################################

# PARA BORRAR LA IMAGEN PREVIA, EN CASO DE QUE HAYAMOS CAMBIADO LA IMAGEN POR OTRA DIFERENTE:
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

@receiver(pre_save, sender=ComidaRapida)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.id:
        imagen_existente = ComidaRapida.objects.get(id=instance.id)
        if instance.Imagen and imagen_existente.Imagen != instance.Imagen:
            imagen_existente.Imagen.delete(False)

# NOTA: CUANDO TENGAMOS PROBLEMAS AL MIGRAR NUESTRO MODELO A LA BASE DE DATOS DEBIDO AL CAMBIO EN LA CARACTERÍSTICA DE UN CAMPO.
# POR EJEMPLO; QUE ANTERIORMENTE UN CAMPO TENGA "NULL", PERO DESPUÉS SUSTITUYAMOS "NULL" POR "DEFAULT=1"; CONSULTAR LA SIGUIENTE LIGA:
# https://stackoverflow.com/questions/40353649/django-migrate-error-typeerror-expected-string-or-bytes-like-object/50463466
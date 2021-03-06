# Generated by Django 3.1.3 on 2021-04-06 23:07

import django.core.validators
from django.db import migrations, models
import reservacion.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=2, verbose_name='Mesa')),
                ('booleano', models.BooleanField(default=True, verbose_name='Disponible')),
                ('Cantidad_asientos', models.IntegerField(default=4, verbose_name='Cantidad de Asientos')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'ordering': ['etiqueta'],
            },
        ),
        migrations.CreateModel(
            name='Reservacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=100, verbose_name='Reservación a Nombre de')),
                ('Dia', models.DateField(verbose_name='Día')),
                ('Numero_Personas', reservacion.models.IntegerPeopleField(verbose_name='Número de Personas')),
                ('Mesas_a_Ocupar', models.IntegerField(blank=True, null=True)),
                ('Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Celular', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message="El número de celular debe comenzar con '55' y tener al menos 10 digitos.         Ejemplo: 5534325917", regex='55[0-9]{8}$')])),
                ('Horario', models.TimeField()),
                ('MesasIndividuales', models.CharField(choices=[('juntas', 'Juntas'), ('separadas', 'Separadas')], default='juntas', max_length=10, verbose_name='Configuración de las Mesas')),
                ('Vigencia', models.BooleanField(default=True, verbose_name='Reservación Vigente')),
                ('creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación de la Reservación')),
                ('actualizacion', models.DateTimeField(auto_now=True, verbose_name='Última Actualización de la Reservación')),
            ],
            options={
                'verbose_name': 'Reservación',
                'verbose_name_plural': 'Reservaciones',
                'ordering': ['Dia', 'Horario', 'Nombre'],
            },
        ),
    ]

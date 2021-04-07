# Generated by Django 3.1.3 on 2021-04-06 23:07

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bebida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=255, unique=True)),
                ('Descripcion', ckeditor.fields.RichTextField(max_length=2048, verbose_name='Descripción')),
                ('Precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('Slug', models.SlugField(max_length=255)),
                ('Activo', models.BooleanField(default=False)),
                ('Tipo', models.CharField(choices=[('café', 'Café'), ('refresco', 'Refresco'), ('alcohólica', 'Alcohólica'), ('agua', 'Agua')], default='Agua', max_length=255)),
                ('Imagen', models.ImageField(blank=True, null=True, upload_to='bebidas/')),
            ],
            options={
                'verbose_name': 'Bebida',
                'verbose_name_plural': 'Bebidas',
                'ordering': ['Tipo', 'Nombre'],
            },
        ),
        migrations.CreateModel(
            name='ComidaRapida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=255, unique=True)),
                ('Descripcion', ckeditor.fields.RichTextField(max_length=2048, verbose_name='Descripción')),
                ('Precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('Slug', models.SlugField(max_length=255)),
                ('Activo', models.BooleanField(default=False)),
                ('Tipo', models.CharField(choices=[('desayuno', 'Desayuno'), ('comida', 'Comida')], default='Comida', max_length=30)),
                ('Tiempo_Preparacion', models.CharField(default='Platillo Listo', max_length=100, verbose_name='Tiempo de Preparación en horas')),
                ('Imagen', models.ImageField(blank=True, null=True, upload_to='comida_rapida/')),
            ],
            options={
                'verbose_name': 'Comida Rápida',
                'verbose_name_plural': 'Comidas',
                'ordering': ['Tipo', 'Nombre'],
            },
        ),
    ]

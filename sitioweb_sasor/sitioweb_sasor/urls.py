"""sasor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include("core.urls", namespace="core_app")),
    path('reservacion/', include("reservacion.urls", namespace="reservacion_app")),
    path('alimentos/', include("alimentos.urls", namespace="alimentos_app")),
    path('contacto/', include("contacto.urls", namespace="contancto_app")),
    path('pedido/', include("ordenes_y_pedidos.urls", namespace="ordenes_y_pedidos_app")),
    path('admin/', admin.site.urls),
]

# De esta forma, podremos visualizar las imágenes en el servidor de pruebas que nos proporciona Django. Sin embargo,
# Las siguientes lineas de código no son necesarias perse, ya que Django guardará las imágenes en la carpeta específicada
# en "settings.py". Además, los servidores de producción, ya nos brindan la posibilidad de mostrar las imágenes sin hacer
# uso de las siguientes líneas de código.
from . import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
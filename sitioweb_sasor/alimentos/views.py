from django.shortcuts import render
from .models import ComidaRapida, Bebida

# Create your views here.
from datetime import datetime
import pytz

def menu_diario(request):
    desayunos = ComidaRapida.objects.filter(Tipo="desayuno").filter(Activo=True)
    comidas = ComidaRapida.objects.filter(Tipo="comida").filter(Activo=True)
    bebidas = Bebida.objects.filter(Activo=True)
    Date_Time = datetime.now(pytz.timezone("America/Mexico_City"))
    return render(request, "alimentos/menu.html", {"desayunos": desayunos, "comidas": comidas, "bebidas": bebidas, "Date_Time": Date_Time})
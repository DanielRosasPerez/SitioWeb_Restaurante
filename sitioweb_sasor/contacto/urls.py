from django.urls import path
from .views import contacta_con_nosotros

app_name = "contacto_app"

urlpatterns = [
    path('', contacta_con_nosotros, name="Contacto"),
]
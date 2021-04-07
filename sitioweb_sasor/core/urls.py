from django.urls import path
from .views import pagina_inicio

app_name = "core_app"

urlpatterns = [
    path('', pagina_inicio, name="Home"),
]

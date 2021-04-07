from django.urls import path
from .views import menu_diario

app_name = "alimentos_app"

urlpatterns = [
    path('menu/', menu_diario, name="MenuView"),
]
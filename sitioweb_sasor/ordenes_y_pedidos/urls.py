from django.urls import path
from .views import datos_pedido, canasta_compras, cuestionario_orden # carro_compras

app_name = "ordenes_y_pedidos_app"

urlpatterns = [
    # path('carrito/<slug:slug>/', carro_compras, name="Carrito"),  # 'comprar/<tipo_variable:nombre_de_la_variable>/'
    
    path('orden_datos/', datos_pedido, name="DatosOrden"),
    path('canasta/', canasta_compras, name="Canasta"),
    path('cuestionario_pedido/', cuestionario_orden, name="CuestionarioPedido"),
]

# FOR CONVERTING DATA DIRECTLY IN THE URL TO FLOAT:
# https://stackoverflow.com/questions/61860878/how-to-send-floats-as-paramters-in-django-2-0-using-path
# https://www.webforefront.com/django/accessurlparamstemplates.html

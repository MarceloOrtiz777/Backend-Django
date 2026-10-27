from django.urls import path
from clientesApp import views as vclientes

urlpatterns = [
    path('', vclientes.inicio, name="home_clientes"),
    path('clientes/', vclientes.clientes, name="home_clientes_listado"),
    path('clientes/crear/', vclientes.crear_cliente, name="cliente_crear"),
    path('clientes/<int:pk>/modificar/', vclientes.modificar_cliente, name="cliente_modificar"),
    path('clientes/<int:pk>/eliminar/', vclientes.eliminar_cliente, name="cliente_eliminar"),
    path('pedidos/', vclientes.pedidos, name="pedidos"),
    path('pedidos/nuevo/', vclientes.crear_pedido, name="pedido_crear"),
    path('pedidos/<int:pk>/anular/', vclientes.anular_pedido, name="pedido_anular"),
    path('ahora/', vclientes.ahora, name="ahora_clientes"),
]
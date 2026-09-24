from django.urls import path
from clientesApp import views as vclientes

urlpatterns = [
    path('', vclientes.inicio, name="home_clientes"),
    path('clientes/', vclientes.clientes, name="home_clientes_listado"),
    path('ahora/', vclientes.ahora, name="ahora_clientes"),
]

from django.urls import path
from usuariosApp import views as vusuarios

urlpatterns = [
    path('', vusuarios.usuarios, name="usuarios"),
    path('nuevo/', vusuarios.crear_usuario, name="usuario_crear"),
    path('<int:pk>/editar/', vusuarios.editar_usuario, name="usuario_editar"),
]
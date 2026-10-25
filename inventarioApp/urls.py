from django.urls import path
from inventarioApp import views as vinventario

urlpatterns = [
    path('', vinventario.inicio, name="inicio"),
    path('productos/', vinventario.productos, name="productos"),
    path('productos/crear/', vinventario.crear_producto, name="producto_crear"),
    path('productos/<int:pk>/modificar/', vinventario.modificar_producto, name="producto_modificar"),
    path('productos/<int:pk>/eliminar/', vinventario.eliminar_producto, name="producto_eliminar"),
    path('ahora/', vinventario.ahora, name="ahora"),
]
from django.urls import path
from inventarioApp import views as vinventario

urlpatterns = [
    path('', vinventario.inicio, name="inicio"),
    path('productos/', vinventario.productos, name="productos"),
    path('ahora/', vinventario.ahora, name="ahora"),
]

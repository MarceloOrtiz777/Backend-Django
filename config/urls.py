from django.contrib import admin
from django.urls import path, include
from inventarioApp import views as vinventario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invent/', include('inventarioApp.urls')),
    path('clientes/', include('clientesApp.urls')),
    path('', vinventario.inicio, name="home"),
]

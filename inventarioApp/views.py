import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    """Página de presentación de la app Inventario."""
    contexto = {
        'total_productos': Producto.objects.count(),
    }
    return render(request, 'inventario/inicio.html', contexto)

@login_required
def productos(request):
    """Vista que muestra el listado de productos obtenido desde la base de datos vía ORM."""
    lista_productos = Producto.objects.all()

    contexto = {
        'productos': lista_productos,
    }
    return render(request, 'inventario/productos.html', contexto)

@login_required
def ahora(request):
    """Vista auxiliar que informa la fecha y hora actual."""
    fecha = datetime.datetime.now()
    salida = f"<h2>En la tienda hoy es <b>{fecha}</b></h2>"
    return HttpResponse(salida)

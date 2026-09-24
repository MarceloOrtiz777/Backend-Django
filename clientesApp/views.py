import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente


def inicio(request):
    """Página de presentación de la app Clientes."""
    contexto = {
        'total_clientes': Cliente.objects.count(),
    }
    return render(request, 'clientes/inicio.html', contexto)


def clientes(request):
    """Vista que muestra el listado de clientes obtenido desde la base de datos vía ORM."""
    lista_clientes = Cliente.objects.all()

    contexto = {
        'clientes': lista_clientes,
    }
    return render(request, 'clientes/clientes.html', contexto)


def ahora(request):
    """Vista auxiliar que informa la fecha y hora actual."""
    fecha = datetime.datetime.now()
    salida = f"<h2>En la tienda hoy es <b>{fecha}</b></h2>"
    return HttpResponse(salida)

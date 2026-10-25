import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm
from .models import Cliente


@login_required
def inicio(request):
    """Página de presentación de la app Clientes."""
    contexto = {
        'total_clientes': Cliente.objects.count(),
    }
    return render(request, 'clientes/inicio.html', contexto)


@login_required
@permission_required('clientesApp.view_cliente', raise_exception=True)
def clientes(request):
    """Listado de clientes con búsqueda por nombre, apellidos o correo."""
    q = request.GET.get('q', '').strip()
    lista_clientes = Cliente.objects.prefetch_related('pedidos__producto')
    if q:
        lista_clientes = lista_clientes.filter(
            Q(nombre__icontains=q) | Q(apellidos__icontains=q) | Q(email__icontains=q)
        )
    contexto = {
        'clientes': lista_clientes,
        'q': q,
    }
    return render(request, 'clientes/clientes.html', contexto)


@login_required
@permission_required('clientesApp.add_cliente', raise_exception=True)
def crear_cliente(request):
    """Crea un cliente nuevo."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente} creado correctamente.')
            return redirect('home_clientes_listado')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form, 'titulo': 'Agregar cliente'})


@login_required
@permission_required('clientesApp.change_cliente', raise_exception=True)
def modificar_cliente(request, pk):
    """Modifica un cliente existente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente {cliente} modificado correctamente.')
            return redirect('home_clientes_listado')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form, 'titulo': 'Modificar cliente'})


@login_required
@permission_required('clientesApp.delete_cliente', raise_exception=True)
def eliminar_cliente(request, pk):
    """Pide confirmación (GET) y elimina el cliente (POST)."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        nombre = str(cliente)
        cliente.delete()
        messages.success(request, f'Cliente {nombre} eliminado correctamente.')
        return redirect('home_clientes_listado')
    return render(request, 'clientes/cliente_confirmar_eliminar.html', {'cliente': cliente})


@login_required
def ahora(request):
    """Vista auxiliar que informa la fecha y hora actual."""
    fecha = datetime.datetime.now()
    salida = f"<h2>En la tienda hoy es <b>{fecha}</b></h2>"
    return HttpResponse(salida)
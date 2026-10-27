import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from inventarioApp.models import Producto

from .forms import ClienteForm, PedidoForm
from .models import Cliente, Pedido


@login_required
def inicio(request):
    """Página de presentación de la app Clientes."""
    contexto = {
        'total_clientes': Cliente.objects.count(),
    }
    return render(request, 'clientes/inicio.html', contexto)


# ---------------------------------------------------------------- Mantenedor de clientes

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


# ---------------------------------------------------------------- Transacción: pedidos

@login_required
@permission_required('clientesApp.view_pedido', raise_exception=True)
def pedidos(request):
    """Listado de pedidos con búsqueda por cliente o producto y total vendido."""
    q = request.GET.get('q', '').strip()
    lista_pedidos = Pedido.objects.select_related('cliente', 'producto')
    if q:
        lista_pedidos = lista_pedidos.filter(
            Q(cliente__nombre__icontains=q) | Q(cliente__apellidos__icontains=q) | Q(producto__nombre__icontains=q)
        )
    total_general = lista_pedidos.aggregate(
        total=Sum(F('cantidad') * F('producto__precio'))
    )['total'] or 0
    contexto = {
        'pedidos': lista_pedidos,
        'q': q,
        'total_general': total_general,
    }
    return render(request, 'clientes/pedidos.html', contexto)


@login_required
@permission_required('clientesApp.add_pedido', raise_exception=True)
def crear_pedido(request):
    """Registra un pedido y descuenta el stock del producto, todo en una sola transacción."""
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            with transaction.atomic():
                # Se bloquea la fila del producto para que dos ventas simultáneas no se pisen el stock.
                producto = Producto.objects.select_for_update().get(pk=pedido.producto_id)
                if pedido.cantidad > producto.stock:
                    form.add_error('cantidad', f'Stock insuficiente: solo quedan {producto.stock} unidad(es).')
                else:
                    pedido.save()
                    producto.stock -= pedido.cantidad
                    producto.save(update_fields=['stock'])
                    messages.success(
                        request,
                        f'Pedido #{pedido.pk} registrado: {pedido.cantidad} x {producto.nombre} '
                        f'para {pedido.cliente} (total ${pedido.total}).',
                    )
                    return redirect('pedidos')
    else:
        form = PedidoForm()
    return render(request, 'clientes/pedido_form.html', {'form': form, 'titulo': 'Registrar pedido'})


@login_required
@permission_required('clientesApp.delete_pedido', raise_exception=True)
def anular_pedido(request, pk):
    """Anula un pedido y devuelve las unidades al stock, también en una sola transacción."""
    pedido = get_object_or_404(Pedido.objects.select_related('cliente', 'producto'), pk=pk)
    if request.method == 'POST':
        with transaction.atomic():
            producto = Producto.objects.select_for_update().get(pk=pedido.producto_id)
            producto.stock += pedido.cantidad
            producto.save(update_fields=['stock'])
            numero = pedido.pk
            pedido.delete()
        messages.success(request, f'Pedido #{numero} anulado. Se devolvieron {pedido.cantidad} unidad(es) al stock.')
        return redirect('pedidos')
    return render(request, 'clientes/pedido_confirmar_anular.html', {'pedido': pedido})


@login_required
def ahora(request):
    """Vista auxiliar que informa la fecha y hora actual."""
    fecha = datetime.datetime.now()
    salida = f"<h2>En la tienda hoy es <b>{fecha}</b></h2>"
    return HttpResponse(salida)
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


@login_required
def inicio(request):
    """Página de presentación de la app Inventario."""
    contexto = {
        'total_productos': Producto.objects.count(),
    }
    return render(request, 'inventario/inicio.html', contexto)


@login_required
@permission_required('inventarioApp.view_producto', raise_exception=True)
def productos(request):
    """Listado de productos con búsqueda por nombre, categoría o descripción."""
    q = request.GET.get('q', '').strip()
    lista_productos = Producto.objects.all()
    if q:
        lista_productos = lista_productos.filter(
            Q(nombre__icontains=q) | Q(categoria__icontains=q) | Q(descripcion__icontains=q)
        )
    contexto = {
        'productos': lista_productos,
        'q': q,
    }
    return render(request, 'inventario/productos.html', contexto)


@login_required
@permission_required('inventarioApp.add_producto', raise_exception=True)
def crear_producto(request):
    """Crea un producto nuevo."""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto}" creado correctamente.')
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/producto_form.html', {'form': form, 'titulo': 'Agregar producto'})


@login_required
@permission_required('inventarioApp.change_producto', raise_exception=True)
def modificar_producto(request, pk):
    """Modifica un producto existente."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto}" modificado correctamente.')
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/producto_form.html', {'form': form, 'titulo': 'Modificar producto'})


@login_required
@permission_required('inventarioApp.delete_producto', raise_exception=True)
def eliminar_producto(request, pk):
    """Pide confirmación (GET) y elimina el producto (POST)."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = str(producto)
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
        return redirect('productos')
    return render(request, 'inventario/producto_confirmar_eliminar.html', {'producto': producto})


@login_required
def ahora(request):
    """Vista auxiliar que informa la fecha y hora actual."""
    fecha = datetime.datetime.now()
    salida = f"<h2>En la tienda hoy es <b>{fecha}</b></h2>"
    return HttpResponse(salida)
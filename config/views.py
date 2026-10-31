from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.shortcuts import render
from django.utils import timezone

from clientesApp.models import Cliente, Pedido
from inventarioApp.models import Producto

# Un producto se considera con "stock bajo" desde esta cantidad hacia abajo
# (es el mismo criterio que usa Producto.estado_stock).
STOCK_BAJO = 5


def perfil_de(user):
    """Devuelve el perfil del usuario según su grupo (o None si no tiene ninguno)."""
    grupos = {g.name for g in user.groups.all()}
    if user.is_superuser or 'Administrador' in grupos:
        return 'Administrador'
    if 'Supervisor' in grupos:
        return 'Supervisor'
    if 'Administrativo' in grupos:
        return 'Administrativo'
    return None


def total_vendido(pedidos):
    """Suma cantidad x precio de un conjunto de pedidos."""
    return pedidos.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0


@login_required
def dashboard(request):
    """Muestra un panel distinto según el perfil del usuario autenticado."""
    perfil = perfil_de(request.user)
    ultimos_pedidos = Pedido.objects.select_related('cliente', 'producto')[:5]
    stock_bajo = Producto.objects.filter(stock__lte=STOCK_BAJO).order_by('stock', 'nombre')

    if perfil == 'Administrador':
        contexto = {
            'total_productos': Producto.objects.count(),
            'total_clientes': Cliente.objects.count(),
            'total_pedidos': Pedido.objects.count(),
            'total_vendido': total_vendido(Pedido.objects.all()),
            'ultimos_pedidos': ultimos_pedidos,
            'stock_bajo': stock_bajo,
            'total_usuarios': User.objects.count(),
            'usuarios_por_perfil': [
                (nombre, User.objects.filter(groups__name=nombre).count())
                for nombre in ('Administrador', 'Supervisor', 'Administrativo')
            ],
        }
        plantilla = 'dashboard/administrador.html'
    elif perfil == 'Supervisor':
        # Se compara contra el inicio del día local (sin usar __date, que en MySQL/MariaDB
        # depende de tablas de zonas horarias que pueden no estar cargadas).
        inicio_dia = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
        pedidos_hoy = Pedido.objects.filter(fecha_pedido__gte=inicio_dia)
        contexto = {
            'pedidos_hoy': pedidos_hoy.count(),
            'vendido_hoy': total_vendido(pedidos_hoy),
            'total_clientes': Cliente.objects.count(),
            'ultimos_pedidos': ultimos_pedidos,
            'stock_bajo': stock_bajo,
        }
        plantilla = 'dashboard/supervisor.html'
    elif perfil == 'Administrativo':
        contexto = {'ultimos_pedidos': ultimos_pedidos}
        plantilla = 'dashboard/administrativo.html'
    else:
        contexto = {}
        plantilla = 'dashboard/sin_perfil.html'

    contexto['perfil'] = perfil
    return render(request, plantilla, contexto)
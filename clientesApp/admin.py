from django.contrib import admin
from .models import Cliente, Pedido


class PedidoInline(admin.TabularInline):
    """Permite ver/crear pedidos de un cliente directamente desde su ficha."""
    model = Pedido
    extra = 1
    autocomplete_fields = ['producto']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'email', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'apellidos', 'email')
    list_filter = ('fecha_registro',)
    ordering = ('apellidos', 'nombre')
    inlines = [PedidoInline]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'producto', 'cantidad', 'total', 'fecha_pedido')
    list_filter = ('fecha_pedido', 'producto')
    search_fields = ('cliente__nombre', 'cliente__apellidos', 'producto__nombre')
    autocomplete_fields = ['cliente', 'producto']
    ordering = ('-fecha_pedido',)

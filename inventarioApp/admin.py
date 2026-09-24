from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'estado_stock')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria', 'descripcion')
    ordering = ('nombre',)

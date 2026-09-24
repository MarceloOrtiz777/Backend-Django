from django.db import models
from inventarioApp.models import Producto


class Cliente(models.Model):
    """Representa a un cliente registrado en el sistema."""

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['apellidos', 'nombre']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Pedido(models.Model):
    """Representa un pedido realizado por un cliente sobre un producto del inventario."""

    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="pedidos"
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="pedidos"
    )
    cantidad = models.PositiveIntegerField(default=1)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_pedido']
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente} - {self.producto}"

    @property
    def total(self):
        """Calcula el total del pedido (precio del producto x cantidad)."""
        return self.producto.precio * self.cantidad

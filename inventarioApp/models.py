from django.db import models


class Producto(models.Model):
    """Representa un producto disponible en el inventario."""

    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

    @property
    def estado_stock(self):
        """Devuelve una etiqueta legible del nivel de stock, usada en templates."""
        if self.stock <= 5:
            return "Stock bajo"
        elif self.stock <= 20:
            return "Stock medio"
        return "Stock alto"

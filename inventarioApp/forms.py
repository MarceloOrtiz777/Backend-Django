from django import forms
from django.core.exceptions import ValidationError

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'stock', 'descripcion']
        labels = {
            'nombre': 'Nombre del producto',
            'categoria': 'Categoría',
            'precio': 'Precio (CLP)',
            'stock': 'Stock disponible',
            'descripcion': 'Descripción (opcional)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Taladro Percutor 750W'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Herramientas eléctricas'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Ej: 45990'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Ej: 18'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if len(nombre) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        # Evita productos duplicados (sin distinguir mayúsculas), ignorando el propio al modificar.
        duplicado = Producto.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk)
        if duplicado.exists():
            raise ValidationError('Ya existe un producto con ese nombre.')
        return nombre

    def clean_categoria(self):
        categoria = self.cleaned_data['categoria'].strip()
        if len(categoria) < 2:
            raise ValidationError('La categoría debe tener al menos 2 caracteres.')
        return categoria

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 1:
            raise ValidationError('El precio debe ser mayor a 0.')
        if precio > 100_000_000:
            raise ValidationError('El precio es demasiado alto. Revisa el valor ingresado.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock > 100_000:
            raise ValidationError('El stock es demasiado alto. Revisa el valor ingresado.')
        return stock
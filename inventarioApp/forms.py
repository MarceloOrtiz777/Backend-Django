import re

from django import forms
from django.core.exceptions import ValidationError

from inventarioApp.models import Producto

from .models import Cliente, Pedido

SOLO_LETRAS = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellidos', 'email', 'telefono']
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono (opcional)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: María'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez Soto'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@correo.cl'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
        }
        error_messages = {
            'email': {'unique': 'Ya existe un cliente con este correo.'},
        }

    def _validar_texto(self, valor, campo):
        valor = valor.strip()
        if len(valor) < 2:
            raise ValidationError(f'El {campo} debe tener al menos 2 letras.')
        if not SOLO_LETRAS.match(valor):
            raise ValidationError(f'El {campo} solo puede contener letras.')
        return valor

    def clean_nombre(self):
        return self._validar_texto(self.cleaned_data['nombre'], 'nombre')

    def clean_apellidos(self):
        return self._validar_texto(self.cleaned_data['apellidos'], 'apellido')

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not telefono:
            return ''
        limpio = re.sub(r'[\s\-]', '', telefono)
        coincide = re.fullmatch(r'(?:\+?56)?(9\d{8})', limpio)
        if not coincide:
            raise ValidationError('Ingresa un celular chileno válido, por ejemplo +56 9 1234 5678.')
        return f'+56{coincide.group(1)}'


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'producto', 'cantidad']
        labels = {
            'cliente': 'Cliente',
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].empty_label = 'Selecciona un cliente'
        self.fields['producto'].empty_label = 'Selecciona un producto'
        # Solo se ofrecen productos que tengan stock disponible.
        self.fields['producto'].queryset = Producto.objects.filter(stock__gt=0)
        self.fields['producto'].label_from_instance = (
            lambda p: f'{p.nombre} — ${p.precio} (stock: {p.stock})'
        )

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad < 1:
            raise ValidationError('La cantidad debe ser al menos 1.')
        return cantidad

    def clean(self):
        datos = super().clean()
        producto = datos.get('producto')
        cantidad = datos.get('cantidad')
        if producto and cantidad and cantidad > producto.stock:
            self.add_error(
                'cantidad',
                f'Stock insuficiente: solo quedan {producto.stock} unidad(es) de "{producto.nombre}".',
            )
        return datos
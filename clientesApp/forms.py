import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Cliente

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
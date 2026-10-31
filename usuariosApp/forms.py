from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError

PERFILES = ('Administrador', 'Supervisor', 'Administrativo')


class UsuarioForm(forms.ModelForm):
    perfil = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=PERFILES).order_by('name'),
        empty_label='Selecciona un perfil',
        label='Perfil',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    password1 = forms.CharField(
        label='Contraseña',
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        help_text='Mínimo 8 caracteres. No puede ser solo números ni una clave muy común.',
    )
    password2 = forms.CharField(
        label='Repetir contraseña',
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres (opcional)',
            'last_name': 'Apellidos (opcional)',
            'email': 'Correo electrónico',
            'is_active': 'Usuario activo (puede iniciar sesión)',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@correo.cl'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {'username': 'Letras, números y @/./+/-/_ (máximo 150 caracteres).'}

    def __init__(self, *args, es_nuevo=False, es_propio=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.es_nuevo = es_nuevo
        self.fields['email'].required = True

        if es_nuevo:
            self.fields['password1'].required = True
            self.fields['password2'].required = True
        else:
            # El nombre de usuario no se puede cambiar una vez creado.
            self.fields['username'].disabled = True
            self.fields['password1'].label = 'Nueva contraseña (opcional)'
            self.fields['password1'].help_text = 'Déjala vacía si no quieres cambiarla.'
            grupo = self.instance.groups.filter(name__in=PERFILES).first()
            self.initial['perfil'] = grupo.pk if grupo else None

        if es_propio:
            # Evita que un administrador se desactive o se quite el perfil a sí mismo.
            self.fields['perfil'].disabled = True
            self.fields['perfil'].required = False
            self.fields['is_active'].disabled = True

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un usuario con este correo.')
        return email

    def clean(self):
        datos = super().clean()
        password1 = datos.get('password1')
        password2 = datos.get('password2')
        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', 'Las contraseñas no coinciden.')
            else:
                # Se valida con un usuario temporal para poder comparar contra sus datos.
                temporal = User(
                    username=datos.get('username', ''),
                    email=datos.get('email', ''),
                    first_name=datos.get('first_name', ''),
                    last_name=datos.get('last_name', ''),
                )
                try:
                    password_validation.validate_password(password1, temporal)
                except ValidationError as error:
                    self.add_error('password1', error)
        return datos

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            usuario.set_password(password)
        usuario.save()
        perfil = self.cleaned_data.get('perfil')
        if perfil:
            usuario.groups.set([perfil])
        return usuario
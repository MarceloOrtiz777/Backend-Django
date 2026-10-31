from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from config.views import perfil_de

from .forms import UsuarioForm


@login_required
@permission_required('auth.view_user', raise_exception=True)
def usuarios(request):
    """Listado de usuarios con su perfil, con búsqueda por usuario, nombre o correo."""
    q = request.GET.get('q', '').strip()
    lista = User.objects.prefetch_related('groups').order_by('username')
    if q:
        lista = lista.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q)
            | Q(last_name__icontains=q) | Q(email__icontains=q)
        )
    filas = [{'usuario': u, 'perfil': perfil_de(u)} for u in lista]
    return render(request, 'usuarios/usuarios.html', {'filas': filas, 'q': q})


@login_required
@permission_required('auth.add_user', raise_exception=True)
def crear_usuario(request):
    """Crea un usuario y le asigna un perfil (grupo)."""
    if request.method == 'POST':
        form = UsuarioForm(request.POST, es_nuevo=True)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" creado con perfil {perfil_de(usuario)}.')
            return redirect('usuarios')
    else:
        form = UsuarioForm(es_nuevo=True)
    return render(request, 'usuarios/usuario_form.html', {'form': form, 'titulo': 'Agregar usuario'})


@login_required
@permission_required('auth.change_user', raise_exception=True)
def editar_usuario(request, pk):
    """Modifica los datos, el perfil, el estado o la contraseña de un usuario."""
    usuario = get_object_or_404(User, pk=pk)
    # Solo un superusuario puede modificar a otro superusuario.
    if usuario.is_superuser and not request.user.is_superuser:
        raise PermissionDenied
    es_propio = usuario.pk == request.user.pk
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario, es_propio=es_propio)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario "{usuario.username}" modificado correctamente.')
            return redirect('usuarios')
    else:
        form = UsuarioForm(instance=usuario, es_propio=es_propio)
    contexto = {'form': form, 'titulo': 'Modificar usuario', 'es_propio': es_propio}
    return render(request, 'usuarios/usuario_form.html', contexto)
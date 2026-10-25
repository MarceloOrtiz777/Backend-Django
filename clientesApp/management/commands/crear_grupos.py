from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

# Qué acciones puede hacer cada perfil sobre cada modelo.
# Django crea solos los permisos view/add/change/delete de cada modelo al hacer migrate.
PERMISOS_POR_GRUPO = {
    'Administrador': {
        'producto': ['view', 'add', 'change', 'delete'],
        'cliente': ['view', 'add', 'change', 'delete'],
        'pedido': ['view', 'add', 'change', 'delete'],
        'user': ['view', 'add', 'change', 'delete'],
        'group': ['view'],
    },
    'Supervisor': {
        'producto': ['view', 'add', 'change'],
        'cliente': ['view', 'add', 'change'],
        'pedido': ['view', 'add', 'change'],
    },
    'Administrativo': {
        'producto': ['view'],
        'cliente': ['view'],
        'pedido': ['view', 'add'],
    },
}


class Command(BaseCommand):
    help = "Crea (o actualiza) los grupos Administrador, Supervisor y Administrativo con sus permisos."

    def handle(self, *args, **options):
        for nombre_grupo, modelos in PERMISOS_POR_GRUPO.items():
            grupo, _ = Group.objects.get_or_create(name=nombre_grupo)
            permisos = []
            for modelo, acciones in modelos.items():
                for accion in acciones:
                    try:
                        permisos.append(Permission.objects.get(
                            codename=f'{accion}_{modelo}',
                            content_type__model=modelo,
                        ))
                    except Permission.DoesNotExist:
                        raise CommandError(
                            f"No existe el permiso {accion}_{modelo}. ¿Corriste 'python manage.py migrate'?"
                        )
            grupo.permissions.set(permisos)
            self.stdout.write(self.style.SUCCESS(
                f"Grupo '{nombre_grupo}': {len(permisos)} permisos asignados."
            ))
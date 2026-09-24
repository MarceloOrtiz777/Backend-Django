import random
from django.core.management.base import BaseCommand
from clientesApp.models import Cliente, Pedido
from inventarioApp.models import Producto


class Command(BaseCommand):
    help = "Carga clientes y pedidos de ejemplo en la base de datos."

    def handle(self, *args, **options):
        clientes = [
            dict(nombre="Armando", apellidos="Bronca Segura",
                 email="armando.bronca@correo.cl", telefono="+56911111111"),
            dict(nombre="Marcela", apellidos="Vidal Contreras",
                 email="marcela.vidal@correo.cl", telefono="+56922222222"),
            dict(nombre="Felipe", apellidos="Rojas Muñoz",
                 email="felipe.rojas@correo.cl", telefono="+56933333333"),
            dict(nombre="Daniela", apellidos="Soto Araya",
                 email="daniela.soto@correo.cl", telefono="+56944444444"),
        ]

        creados = 0
        objetos_cliente = []
        for datos in clientes:
            cliente, fue_creado = Cliente.objects.get_or_create(
                email=datos["email"], defaults=datos
            )
            objetos_cliente.append(cliente)
            if fue_creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {creados} clientes nuevos creados (de {len(clientes)} definidos)."
        ))

        productos = list(Producto.objects.all())
        if not productos:
            self.stdout.write(self.style.WARNING(
                "No hay productos cargados todavía — ejecuta primero 'python manage.py seed_productos'."
            ))
            return

        pedidos_creados = 0
        if Pedido.objects.count() == 0:
            for cliente in objetos_cliente:
                producto = random.choice(productos)
                Pedido.objects.create(
                    cliente=cliente,
                    producto=producto,
                    cantidad=random.randint(1, 5),
                )
                pedidos_creados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {pedidos_creados} pedidos de ejemplo creados."
        ))

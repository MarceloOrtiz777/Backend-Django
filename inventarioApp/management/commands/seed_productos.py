from django.core.management.base import BaseCommand
from inventarioApp.models import Producto


class Command(BaseCommand):
    help = "Carga productos de ejemplo en la base de datos (mismos datos usados en la Evaluación 1)."

    def handle(self, *args, **options):
        productos = [
            dict(nombre="Taladro Percutor 750W", categoria="Herramientas eléctricas",
                 precio=45990, stock=18,
                 descripcion="Taladro percutor de uso profesional, ideal para perforar concreto, madera y metal."),
            dict(nombre="Set de Destornilladores (12 piezas)", categoria="Herramientas manuales",
                 precio=12990, stock=42,
                 descripcion="Juego de destornilladores planos y de estrella con mango ergonómico."),
            dict(nombre="Escalera de Aluminio 6 peldaños", categoria="Equipos de acceso",
                 precio=39990, stock=7,
                 descripcion="Escalera plegable liviana, soporta hasta 120 kg."),
            dict(nombre="Casco de Seguridad", categoria="Elementos de protección personal",
                 precio=6990, stock=65,
                 descripcion="Casco certificado para trabajos de construcción y bodega."),
            dict(nombre="Cinta Métrica 8m", categoria="Herramientas manuales",
                 precio=4990, stock=3,
                 descripcion="Cinta métrica reforzada con freno automático."),
        ]

        creados = 0
        for datos in productos:
            _, fue_creado = Producto.objects.get_or_create(
                nombre=datos["nombre"], defaults=datos
            )
            if fue_creado:
                creados += 1

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {creados} productos nuevos creados (de {len(productos)} definidos)."
        ))

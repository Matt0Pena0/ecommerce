import random
from django.core.management.base import BaseCommand
from django.db import transaction
from productos.models import Producto, UnidadMedida, Marca, Categoria, Gondola, Codigo

class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de prueba aleatorios (Seeding)'

    def add_arguments(self, parser):
        # Permite elegir cuántos productos crear
        parser.add_argument('cantidad', type=int, help='Cantidad de productos a crear')

    @transaction.atomic # Si algo falla, no guarda nada
    def handle(self, *args, **kwargs):
        cantidad = kwargs['cantidad']
        
        self.stdout.write(self.style.WARNING('Eliminando datos antiguos...'))
        # Limpieza previa (SOLO DEV)
        Producto.objects.all().delete()
        Codigo.objects.all().delete()
        Marca.objects.all().delete()
        Categoria.objects.all().delete()
        Gondola.objects.all().delete()
        UnidadMedida.objects.all().delete()

        self.stdout.write('Creando datos frescos...')

        # 1. Crear Marcas
        marcas = [Marca(nombre=f"Marca {i}") for i in range(1, 6)]
        Marca.objects.bulk_create(marcas)
        marcas_db = list(Marca.objects.all())

        # 2. Crear Categorías
        categorias = [Categoria(nombre=f"Categoría {i}") for i in range(1, 6)]
        Categoria.objects.bulk_create(categorias)
        categorias_db = list(Categoria.objects.all())

        # 3. Crear Góndolas
        gondolas = [Gondola(nombre=f"Góndola {i}") for i in range(1, 4)]
        Gondola.objects.bulk_create(gondolas)
        gondolas_db = list(Gondola.objects.all())

        # 4. Crear Unidades
        nombres_unidad = ["kg", "g", "l", "ml", "u"]
        unidades = [UnidadMedida(nombre=n) for n in nombres_unidad]
        UnidadMedida.objects.bulk_create(unidades)
        unidades_db = list(UnidadMedida.objects.all())

        # 5. Crear Códigos y Productos
        productos_batch = []
        
        self.stdout.write(f'Generando {cantidad} productos...')

        for i in range(1, cantidad + 1):
            # Crea el código primero
            codigo_obj = Codigo.objects.create(codigo=str(1000 + i))
            
            prod = Producto(
                codigo=codigo_obj,
                nombre=f"Producto de Prueba {i}",
                marca=random.choice(marcas_db),
                categoria=random.choice(categorias_db),
                gondola=random.choice(gondolas_db),
                unidad_medida=random.choice(unidades_db),
                precio_unitario=round(random.uniform(10.0, 500.0), 2),
                descripcion=f"Descripción generada para el producto {i}. Ideal para pruebas de layout.",
                stock=random.randint(0, 100),
            )
            productos_batch.append(prod)

        Producto.objects.bulk_create(productos_batch)

        self.stdout.write(self.style.SUCCESS(f'¡Éxito! Se crearon {cantidad} productos nuevos.'))
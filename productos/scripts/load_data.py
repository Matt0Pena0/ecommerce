import os
import json
from decimal import Decimal
# pyrefly: ignore [missing-import]
from django.db import transaction
# pyrefly: ignore [missing-import]
from productos.models import (
    Producto, 
    UnidadMedida, 
    Marca, 
    Categoria, 
    Gondola, 
    Codigo
)

def run(*args):
    """
    Script para ejecutar con:
    python manage.py runscript productos.scripts.load_data
    o desde docker compose:
    docker compose exec web python manage.py runscript productos.scripts.load_data
    """
    # Determinar ruta del archivo json
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'data', 'productos_estructurados.json')

    if not os.path.exists(json_path):
        # Fallback a data.json
        json_path = os.path.join(base_dir, 'data', 'data.json')

    print(f"--> Cargando catálogo desde: {json_path}")

    with open(json_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print(f"--> Se encontraron {len(catalog)} productos para procesar.")

    creados = 0
    actualizados = 0

    with transaction.atomic():
        for item in catalog:
            # 1. Categoría
            cat_obj = None
            if item.get('categoria'):
                cat_obj, _ = Categoria.objects.get_or_create(nombre=item['categoria'].strip())

            # 2. Marca
            marca_obj = None
            if item.get('marca'):
                marca_obj, _ = Marca.objects.get_or_create(nombre=item['marca'].strip())

            # 3. Unidad de Medida (max_length 20)
            unidad_obj = None
            if item.get('unidad_medida'):
                un_nombre = item['unidad_medida'].strip()[:20]
                unidad_obj, _ = UnidadMedida.objects.get_or_create(nombre=un_nombre)

            # 4. Código
            cod_str = str(item.get('codigo', item.get('id', ''))).strip()
            codigo_obj, _ = Codigo.objects.get_or_create(codigo=cod_str)

            # 5. Producto
            precio = Decimal(str(item.get('precio_unitario', '0.00')))
            stock = int(item.get('stock', 100))
            nombre = item['nombre'].strip()
            desc = item.get('descripcion', '').strip()

            prod, is_new = Producto.objects.update_or_create(
                codigo=codigo_obj,
                defaults={
                    'nombre': nombre,
                    'marca': marca_obj,
                    'categoria': cat_obj,
                    'unidad_medida': unidad_obj,
                    'precio_unitario': precio,
                    'descripcion': desc,
                    'stock': stock,
                }
            )

            if is_new:
                creados += 1
            else:
                actualizados += 1

    print(f"✅ Proceso completado exitosamente:")
    print(f"   - Productos creados: {creados}")
    print(f"   - Productos actualizados: {actualizados}")
    print(f"   - Total Categorías en DB: {Categoria.objects.count()}")
    print(f"   - Total Marcas en DB: {Marca.objects.count()}")
    print(f"   - Total Unidades en DB: {UnidadMedida.objects.count()}")
    print(f"   - Total Productos en DB: {Producto.objects.count()}")

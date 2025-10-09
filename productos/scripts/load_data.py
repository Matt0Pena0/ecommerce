import json
import os
from productos.models import Producto, UnidadMedida, Marca, Codigo

# Ruta del .json a cargar (modificar acá)
JSON_PATH = os.path.join("static", "data.json")

def run():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Crea o recupera unidades y marcas
    for item in data:
        unidad_nombre = item["unidad"].strip()
        marca_nombre = item["marca"].strip()

        unidad, _ = UnidadMedida.objects.get_or_create(nombre=unidad_nombre)
        marca = Marca.objects.get_or_create(nombre=marca_nombre)[0] if marca_nombre else None

        # Crea nuevo código autoincremental
        ultimo_codigo = Codigo.objects.order_by("-id").first()
        nuevo_codigo = Codigo.objects.create(codigo=str(ultimo_codigo.id + 1 if ultimo_codigo else 1))

        # Crea el producto
        Producto.objects.create(
            codigo=nuevo_codigo,
            nombre=item["nombre"],
            unidad_medida=unidad,
            marca=marca,
            descripcion=item["descripcion"],
            precio_unitario=0,
            stock=1000
        )

    print(f"✔️ {len(data)} productos cargados correctamente desde '{JSON_PATH}'")

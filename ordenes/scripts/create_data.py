# # scripts/create_data.py

# import random
# from productos.models.producto import Producto
# from productos.models.producto import UnidadMedida
# from productos.models.producto import Marca, Categoria, Gondola, Codigo
# from datetime import date

# def run():
#     # 1) Crear códigos 1…10
#     codigo_objs = []
#     for i in range(1, 11):
#         c = Codigo.objects.create(codigo=str(i))
#         codigo_objs.append(c)
#     print(f"✔️ 10 Códigos creados (1–10)")

#     # 2) Crear Marcas (5 ejemplos)
#     marcas = []
#     for i in range(1, 6):
#         marcas.append(Marca(nombre=f"Marca {i}"))
#     Marca.objects.bulk_create(marcas)
#     marcas = list(Marca.objects.all())
#     print(f"✔️ {len(marcas)} Marcas creadas")

#     # 3) Crear Categorías (5 ejemplos)
#     categorias = []
#     for i in range(1, 6):
#         categorias.append(Categoria(nombre=f"Categoría {i}"))
#     Categoria.objects.bulk_create(categorias)
#     categorias = list(Categoria.objects.all())
#     print(f"✔️ {len(categorias)} Categorías creadas")

#     # 4) Crear Góndolas (3 ejemplos)
#     gondolas = []
#     for i in range(1, 4):
#         gondolas.append(Gondola(nombre=f"Góndola {i}"))
#     Gondola.objects.bulk_create(gondolas)
#     gondolas = list(Gondola.objects.all())
#     print(f"✔️ {len(gondolas)} Góndolas creadas")

#     # 5) Crear Unidades de Medida (ejemplos comunes)
#     nombres_unidad = ["kg", "g", "l", "ml", "unidad"]
#     unidades = [UnidadMedida(nombre=n) for n in nombres_unidad]
#     UnidadMedida.objects.bulk_create(unidades)
#     unidades = list(UnidadMedida.objects.all())
#     print(f"✔️ {len(unidades)} Unidades de Medida creadas")

#     # 6) Crear un Producto por cada Código
#     productos = []
#     for idx, codigo in enumerate(codigo_objs, start=1):
#         prod = Producto(
#             codigo=codigo,
#             nombre=f"Producto {idx}",
#             marca=random.choice(marcas),
#             categoria=random.choice(categorias),
#             gondola=random.choice(gondolas),
#             unidad_medida=random.choice(unidades),
#             precio_unitario=round(random.uniform(10.0, 100.0), 2),
#             descripcion=f"Descripción del producto {idx}",
#             stock=random.randint(0, 50),
#         )
#         productos.append(prod)

#     Producto.objects.bulk_create(productos)
#     print(f"✔️ {len(productos)} Productos creados con códigos asignados")

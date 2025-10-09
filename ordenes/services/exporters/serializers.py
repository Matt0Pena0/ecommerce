from ordenes.models import Orden

class OrdenSerializer:
    """Convierte una Orden en una lista de dicts listos para exportar, optimizando queries."""

    @staticmethod
    def _safe(value):
        """Convierte None o 'Null' en '', y lo devuelve como str."""
        if value is None or str(value).strip().lower() == "null":
            return ""
        return str(value)

    @classmethod
    def serialize(cls, orden: Orden) -> list[dict]:
        rows = []

        items = orden.items.select_related(
            'producto', 
            'producto__marca', 
            'producto__categoria', 
            'producto__unidad_medida', 
            'producto__gondola'
        )

        for item in items:
            prod = item.producto
            rows.append({
                "codigo":           cls._safe(prod.codigo),
                "nombre":           cls._safe(prod.nombre),
                "cantidad":         cls._safe(item.cantidad),
                "precio_unitario":  cls._safe(prod.precio_unitario),
                "unidad":           cls._safe(getattr(prod.unidad_medida, "nombre", None)),
                "marca":            cls._safe(getattr(prod.marca, "nombre", None)),
                "gondola":          cls._safe(getattr(prod.gondola, "nombre", None)),
                "categoria":        cls._safe(getattr(prod.categoria, "nombre", None)),
                "descripcion":      cls._safe(prod.descripcion),
            })
        return rows


# from ordenes.models import Orden


# class OrdenSerializer:
#     """Convierte una Orden en una lista de dicts listos para exportar, optimizando queries."""

#     @staticmethod
#     def serialize(orden: Orden) -> list[dict]:
#         rows = []

#         items = orden.items.select_related(
#             'producto', 
#             'producto__marca', 
#             'producto__categoria', 
#             'producto__unidad_medida', 
#             'producto__gondola'
#         )

#         for item in items:
#             prod = item.producto
#             rows.append({
#                 "codigo":           str(prod.codigo),
#                 "nombre":           prod.nombre,
#                 "cantidad":         item.cantidad,
#                 "precio_unitario":  prod.precio_unitario,
#                 "unidad":           prod.unidad_medida.nombre if prod.unidad_medida else "",
#                 "marca":            prod.marca.nombre if prod.marca else "",
#                 "gondola":          prod.gondola.nombre if prod.gondola else "",
#                 "categoria":        prod.categoria.nombre if prod.categoria else "",
#                 "descripcion":      prod.descripcion or "",
#             })
#         return rows

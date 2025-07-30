from ordenes.models import Orden

class OrdenSerializer:
    """Convierte un Orden en una lista de dicts listos para exportar."""
    @staticmethod
    def serialize(orden: Orden) -> list[dict]:
        rows = []
        for item in orden.items.all():
            prod = item.producto
            rows.append({
                "codigo":           str(prod.codigo),
                "nombre":           prod.nombre,
                "cantidad":         item.cantidad,
                "precio_unitario":  prod.precio_unitario,
                "unidad":           prod.unidad_medida.nombre if prod.unidad_medida else "",
                "marca":            prod.marca.nombre if prod.marca else "",
                "gondola":          prod.gondola.nombre if prod.gondola else "",
                "categoria":        prod.categoria.nombre if prod.categoria else "",
                "descripcion":      prod.descripcion or "",
            })
        return rows

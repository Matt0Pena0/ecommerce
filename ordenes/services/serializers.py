from ordenes.models import Orden
from typing import Any 


class OrdenSerializer:
    """Convierte una Orden en una lista de dicts listos para exportar, optimizando queries."""

    @staticmethod
    def _safe(value):
        """Convierte None o 'Null' en '', y lo devuelve como str."""
        if value is None or str(value).strip().lower() == "null":
            return ""
        return str(value)

    @classmethod
    def serialize(cls, orden: Orden) -> dict[str, Any]:

        items = orden.items.select_related(
            'producto', 
            'producto__marca', 
            'producto__categoria', 
            'producto__unidad_medida', 
            'producto__gondola'
        )

        items_serializadas = []

        for item in items:
            prod = item.producto
            items_serializadas.append({
                "id":               cls._safe(prod.id),
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
        
        orden_serializada = {
            "id": cls._safe(orden.id),
            "fecha_creacion": cls._safe(orden.creado.strftime('%Y-%m-%d')),
            "solicitante_username": cls._safe(orden.solicitante.username),
            "items": items_serializadas
        }

        return orden_serializada

from ordenes.models import Orden, ItemOrden
from ordenes.services.interfaces import IOrdenesService


class OrdenService(IOrdenesService):
    def crear_orden(self, solicitante, items, observaciones=""):
        """
        items: lista de tuplas (producto, cantidad)
        """

        orden = Orden.objects.create(
            solicitante=solicitante,
            observaciones=observaciones
        )

        for prod, cantidad in items:
            ItemOrden.objects.create(
                orden=orden,
                producto=prod,
                cantidad=cantidad
            )
        return orden
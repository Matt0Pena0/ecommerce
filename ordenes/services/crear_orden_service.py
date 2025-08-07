from ordenes.models import Orden, ItemOrden
from ordenes.services.orden_interfaces import IOrdenesService


class OrdenService(IOrdenesService):
    def crear_orden(self, solicitante, items):
        """
        items: lista de tuplas (producto, cantidad)
        """

        orden = Orden.objects.create(solicitante=solicitante)

        for prod, cantidad in items:
            ItemOrden.objects.create(
                orden=orden,
                producto=prod,
                cantidad=cantidad
            )
        return orden
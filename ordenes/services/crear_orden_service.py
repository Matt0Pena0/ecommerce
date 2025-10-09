from ordenes.models import Orden, ItemOrden
from ordenes.services.orden_interfaces import IOrdenesService


class OrdenService(IOrdenesService):
    def crear_orden(self, solicitante, items):
        """
        items: lista de tuplas (producto, cantidad)
        
        se utiliza bulk_create para reducir N consultas INSERT a 1 consulta.
        """

        # Crea la orden principal
        orden = Orden.objects.create(solicitante=solicitante)

        # Prepara los objetos ItemOrden en memoria
        items_a_crear = []
        for prod, cantidad in items:
            # Crea la instancia del modelo, pero NO la guardamos en la DB todavía
            item_orden = ItemOrden(
                orden=orden,
                producto=prod,
                cantidad=cantidad
            )
            items_a_crear.append(item_orden)

        # Inserta todos los ítems de la orden en una sola consulta
        ItemOrden.objects.bulk_create(items_a_crear)

        return orden
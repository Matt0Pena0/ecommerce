from django.db import transaction
from django.db.models import F

from ordenes.services.orden_interfaces import IOrdenesService
from ordenes.models import Orden, ItemOrden
from productos.models import Producto


class OrdenService(IOrdenesService):

    @transaction.atomic
    def crear_orden(self, solicitante, items):
        """
        Crea una orden, sus ítems y descuenta el stock del producto correspondiente.

        items: lista de tuplas (producto, cantidad)
        se utiliza bulk_create para reducir N consultas INSERT a 1 consulta.
        """

        # Crea la orden principal
        orden = Orden.objects.create(solicitante=solicitante)

        # Prepara los objetos ItemOrden en memoria
        items_para_crear = []
        for prod, cantidad in items:
            # Crea la instancia del modelo, pero NO se guarda en DB
            item_orden = ItemOrden(
                orden=orden,
                producto=prod,
                cantidad=cantidad
            )
            items_para_crear.append(item_orden)

        # Inserta todos los ítems de la orden en una sola consulta
        ItemOrden.objects.bulk_create(items_para_crear)

        # Descuenta el stock de los productos emitidos
        for prod, cantidad in items:
            Producto.objects.filter(id=prod.id).update(stock=F('stock') - cantidad)

        return orden
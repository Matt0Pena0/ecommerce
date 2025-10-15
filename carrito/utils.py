from django.db.models import Count

from .models import ItemCarrito


def total_items_carrito(carrito):
    """
    Calcula la cantidad de tipos de productos únicos en un carrito.
    """
    if not carrito:
        return 0

    # Esta es la lógica que quieres reutilizar
    total = ItemCarrito.objects.filter(carrito=carrito).aggregate(
        total=Count('producto', distinct=True)
    )['total'] or 0

    return int(total)
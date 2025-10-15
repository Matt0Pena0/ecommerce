from datetime import datetime

from .utils import total_items_carrito
from .models import Carrito, ItemCarrito


def get_current_year(request):
    current_year = datetime.now().year

    return {
        "current_year": current_year
    }


def get_total_items_carrito(request):
    total_items = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            total_items = total_items_carrito(carrito)
        except Carrito.DoesNotExist:
            pass

    return {'total_items_carrito': total_items}
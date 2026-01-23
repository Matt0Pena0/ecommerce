from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
import json

from carrito.models import Carrito, ItemCarrito
from productos.models import Producto
from ordenes.services.crear_orden_service import OrdenService
from .utils import total_items_carrito


@login_required
def obtener_carrito_usuario(request):
    carrito = Carrito.objects.get_or_create(usuario=request.user)

    return carrito


@login_required
def ver_carrito(request):
    carrito, creado = obtener_carrito_usuario(request)

    return render(request, "carrito/VerCarrito.html", {"carrito": carrito})


@login_required
def finalizar_carrito(request):
    carrito, creado = obtener_carrito_usuario(request)

    if not carrito.items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("productos:listar")

    items = [(item.producto, item.cantidad) for item in carrito.items.select_related('producto')]

    orden_service = OrdenService()

    orden = orden_service.crear_orden(
        solicitante=request.user,
        items=items
    )

    # Limpiar carrito
    carrito.items.all().delete()

    messages.success(request,f"Orden #{orden.id} generada correctamente.")
    return redirect("ordenes:listar")

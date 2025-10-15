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


@require_http_methods(["POST"])
@login_required
def actualizar_item_carrito_api(request):
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad', 0))

        if not producto_id or cantidad is None:
            return JsonResponse({"status": "error", "message": "Datos de producto o cantidad faltantes."}, status=400)

        # Obtiene Carrito y Producto
        carrito, creado = obtener_carrito_usuario(request)
        producto = get_object_or_404(Producto, id=producto_id)

        # Intenta obtener el ítem
        item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()

        mensaje = ""

        # Para eliminar desde "Disminuir cantidad"
        if cantidad == 0:
            if item:
                item.delete()
                mensaje = "Producto eliminado del carrito."

            else:
                mensaje = "El producto no estaba en el carrito"

        # Añade o actualiza productos al carrito
        elif cantidad > 0:

            if item:
                # Actualización
                item.cantidad = cantidad
                item.save()
                mensaje = "Cantidad de producto actualizada."
            else:
                # Creación
                ItemCarrito.objects.create(
                    carrito=carrito,
                    producto=producto,
                    cantidad=cantidad
                )
                mensaje = "Producto agregado al carrito."

        # Recalcula el total de productos únicos DESPUÉS de cualquier operación.
        nuevo_total = total_items_carrito(carrito)

        # Devuelve la respuesta JSON
        return JsonResponse({
            "status": "ok",
            "message": mensaje,
            "nuevo_total_productos": nuevo_total
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Datos JSON inválidos."}, status=400)
    except Producto.DoesNotExist:
        return JsonResponse({"status": "error", "message": "El producto no existe."}, status=404)
    except Exception as e:
        print(f"Error fatal en la API de carrito: {e}")
        return JsonResponse({"status": "error", "message": f"Error interno del servidor: {e}"}, status=500)


@login_required
def actualizar_carrito(request):
    carrito, creado = obtener_carrito_usuario(request)

    if request.method == "POST":
        for item in carrito.items.select_related('producto'):
            # Construye el nombre del campo dinámicamente, igual que en el template
            nombre_campo = f"cantidad_{item.producto.id}"
            # Usar .get() para obtener la cantidad
            cantidad_str = request.POST.get(nombre_campo)
            if cantidad_str:
                try:
                    cantidad = int(cantidad_str)
                    if cantidad > 0:
                        # Valida que la cantidad no exceda el stock
                        if cantidad <= item.producto.stock:
                            item.cantidad = cantidad
                            item.save()
                    else:
                        # Si la cantidad es 0 o menos, elimina el ítem
                        item.delete()
                except (ValueError, TypeError):
                    pass

    return redirect("carrito:ver_carrito") 


@require_http_methods(["POST"]) 
@login_required
def eliminar_item_carrito_api(request, producto_id):
    carrito, creado = obtener_carrito_usuario(request)
    item = carrito.items.filter(producto_id=producto_id).first()

    try:
        if item:
            # Eliminar el ítem del carrito
            item.delete()

            # Llamar a la función encargada de calcular los items para el badge
            nuevo_total = total_items_carrito(carrito)

            return JsonResponse({
                "status": "ok", 
                "message": "Producto eliminado.",
                "nuevo_total_productos": nuevo_total
            }, status=200)

    except Producto.DoesNotExist:
        return JsonResponse({"status": "error", "message": "El producto no existe."}, status=404)
    except Exception as e:
        print(f"Error fatal en la API de carrito: {e}")
        return JsonResponse({"status": "error", "message": f"Error interno del servidor: {e}"}, status=500)


@login_required
def eliminar_item_carrito(request, producto_id):
    carrito, creado = obtener_carrito_usuario(request)
    item = carrito.items.filter(producto_id=producto_id).first()
    if item:
        item.delete()

    return redirect("carrito:ver_carrito")


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

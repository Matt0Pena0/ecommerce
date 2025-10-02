from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
import json


from carrito.models import Carrito, ItemCarrito
from productos.models import Producto
from ordenes.services.crear_orden_service import OrdenService


@login_required
def obtener_carrito_usuario(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    return carrito, creado


@login_required
def agregar_al_carrito_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        # Leer el cuerpo de la petición, llega dentro de JSON
        data = json.loads(request.body)
        producto_codigo = data.get('producto_codigo')
        cantidad = int(data.get('cantidad', 1))
        if not producto_codigo or cantidad <= 0:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

        producto = get_object_or_404(Producto, codigo=producto_codigo)
        carrito, creado = obtener_carrito_usuario(request)
        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}
        )

        cantidad_final = cantidad

        if cantidad_final > producto.stock:
            return JsonResponse({
                "status": "error",
                "message": f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}"
            }, status=400)

        item.cantidad = cantidad_final
        item.save()

        return JsonResponse({
            "status": "ok",
            "message": f"'{producto.nombre}' agregado al carrito.",
            "total_items_carrito": carrito.items.count(), # Para actualizar un contador en la UI
            "cantidad_producto_en_carrito": cantidad_final # Para el display del producto
        })

    except Exception as e:

        import traceback
        traceback.print_exc() # Muestra el error completo en consola
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def ver_carrito(request):
    carrito, creado = obtener_carrito_usuario(request)

    return render(request, "carrito/VerCarrito.html", {"carrito": carrito})


@login_required
def actualizar_carrito(request):
    carrito, creado = obtener_carrito_usuario(request)

    if request.method == "POST":
        for item in carrito.items.select_related('producto'):
            # Construir el nombre del campo dinámicamente, igual que en el template
            nombre_campo = f"cantidad_{item.producto.codigo}"
            
            # Usar .get() para obtener el dato
            cantidad_str = request.POST.get(nombre_campo)
            if cantidad_str:
                try:
                    cantidad = int(cantidad_str)
                    if cantidad > 0:
                        # Opcional: validar que la cantidad no exceda el stock
                        if cantidad <= item.producto.stock:
                            item.cantidad = cantidad
                            item.save()
                    else:
                        # Si la cantidad es 0 o menos, eliminamos el ítem
                        item.delete()
                except (ValueError, TypeError):
                    # Ignorar si el valor no es un número válido
                    pass

    # El redirect debe ser a la vista que muestra el carrito
    return redirect("carrito:ver_carrito") 


@login_required
def eliminar_item_carrito(request, producto_codigo):
    carrito, creado = obtener_carrito_usuario(request)
    item = carrito.items.filter(producto__codigo=producto_codigo).first()
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
    orden_service.crear_orden(request.user, items)

    # Limpiar carrito
    carrito.items.all().delete()

    messages.success(request, "Orden generada correctamente.")
    return redirect("ordenes:listar")

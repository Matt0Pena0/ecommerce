from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
import json

from ordenes.views.reportes import exportar_orden_a_txt
from carrito.models import Carrito, ItemCarrito
from ordenes.models import Orden, ItemOrden
from productos.models import Producto


@login_required
def agregar_al_carrito_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        # Leemos el cuerpo de la petición, que esperamos sea JSON
        data = json.loads(request.body)
        producto_codigo = data.get('producto_codigo')
        cantidad = int(data.get('cantidad', 1))
        if not producto_codigo or cantidad <= 0:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

        producto = get_object_or_404(Producto, codigo=producto_codigo)
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}
        )

        cantidad_final = item.cantidad + cantidad if not creado else cantidad

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
            "total_items_carrito": carrito.items.count() # Para actualizar un contador en la UI
        })

    except Exception as e:

        import traceback
        traceback.print_exc()  # Muestra el error completo en consola
        return JsonResponse({"error": str(e)}, status=500)

# @login_required
# def agregar_al_carrito(request, producto_codigo):
#     producto = get_object_or_404(Producto, codigo=producto_codigo)

#     if request.method == "POST":
#         # 1. Construimos el nombre dinámico del campo, igual que en el template.
#         nombre_del_campo = f"cantidad_{producto.codigo}"
#         # 2. Obtenemos la cantidad de forma segura.
#         cantidad_str = request.POST.get(nombre_del_campo)
#         try:
#             cantidad = int(cantidad_str)
#             if cantidad <= 0:
#                 # Si la cantidad es inválida, no hacemos nada o mostramos un error.
#                 messages.error(request, "Cantidad inválida.")
#                 return redirect("productos:listar")

#         except (ValueError, TypeError):
#             # Si el valor no es un número, usamos 1 por defecto.
#             cantidad = 1
#             return redirect("productos:listar")


#         # 3. Obtenemos o creamos el carrito y el ítem
#         carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
#         item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()

#         if item:
#             item.cantidad += cantidad
#             item.save()
#             messages.success(request, f"Cantidad actualizada para '{producto.nombre}'.")
#         else:
#             ItemCarrito.objects.get_or_create(
#                 carrito=carrito,
#                 producto=producto,
#                 cantidad=cantidad,
#             )
#             messages.success(request, f"'{producto.nombre}' fue agregado al carrito.")

#     return redirect("productos:listar")


@login_required
def obtener_carrito_usuario(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return carrito


@login_required
def ver_carrito(request):
    carrito = obtener_carrito_usuario(request)
    return render(request, "carrito/VerCarrito.html", {"carrito": carrito})


@login_required
def actualizar_carrito(request):
    carrito = obtener_carrito_usuario(request)

    if request.method == "POST":
        for item in carrito.items.all():
            # Construimos el nombre del campo dinámicamente, igual que en el template
            nombre_campo = f"cantidad_{item.producto.codigo}"
            
            # Usamos .get() con un valor por defecto para evitar errores si no viene el dato
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
    carrito = obtener_carrito_usuario(request)
    item = carrito.items.filter(producto__codigo=producto_codigo).first()
    if item:
        item.delete()

    return redirect("carrito:ver_carrito")


@login_required
def finalizar_carrito(request):
    carrito = obtener_carrito_usuario(request)

    if not carrito.items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("carrito:ver_carrito")

    # Crear la orden
    orden = Orden.objects.create(solicitante=request.user)

    # Crear los items en la orden
    for item in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            producto=item.producto,
            cantidad=item.cantidad,
        )

    exportar_orden_a_txt(orden)

    # Limpiar carrito
    carrito.items.all().delete()

    messages.success(request, "Orden generada correctamente.")
    return redirect("ordenes:listar")

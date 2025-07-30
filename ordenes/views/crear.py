from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ordenes.services.exporters.txt_exporter import TxtExporter
from ordenes.views.reportes import exportar_orden_a_txt
from productos.models import Producto



@login_required
def crear_orden(request):
    productos = Producto.objects.all()
    if request.method == "POST":
        items = []
        for producto in productos:
            cantidad = int(request.POST.get(f"cantidad_{producto.codigo}", 0))
            if cantidad > 0:
                items.append((producto, cantidad))

        observaciones = request.POST.get("observaciones", "")

        if items:
            servicio = TxtExporter()
            nueva_orden = servicio.crear_orden(
                solicitante=request.user,
                items=items,
                observaciones=observaciones,
            )
            exportar_orden_a_txt(nueva_orden)
            return redirect("ordenes:listar")
        
    context = {"productos": productos}

    return render(request, "core/home.html", context)


# @login_required
# def finalizar_orden(request):
#     carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

#     if not carrito.items.exists():
#         return redirect("carrito:crear")

#     # Aquí podrías implementar la lógica para finalizar la orden
#     # Por ejemplo, crear una instancia de Orden y asociarla con el carrito

#     # Limpiar el carrito después de finalizar la orden
#     carrito.items.all().delete()

#     return redirect("carrito:crear")

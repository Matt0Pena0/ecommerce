from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# from ordenes.services.exporters.txt_exporter import TxtExporter
from ordenes.views.reportes import exportar_orden_a_txt
from ordenes.services.orden_service import OrdenService
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
            servicio = OrdenService()
            nueva_orden = servicio.crear_orden(
                solicitante=request.user,
                items=items,
                observaciones=observaciones,
            )
            exportar_orden_a_txt(nueva_orden)
            return redirect("ordenes:listar")
        
    context = {"productos": productos}

    return render(request, "ordenes/CrearOrden.html", context)
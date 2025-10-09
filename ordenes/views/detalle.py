from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from accounts.utils import RolRequeridoMixin, PermisosDatosMixin
from ordenes.models import Orden
from ordenes.services.exportar_orden_service import OrdenExportService
from ordenes.services.exporters.excel_exporter import ExcelExporter
from ordenes.services.exporters.txt_exporter import TxtExporter
from ordenes.services.serializers import OrdenSerializer


class OrdenDetailView(LoginRequiredMixin, RolRequeridoMixin, PermisosDatosMixin, DetailView):
    model = Orden
    template_name = "ordenes/DetalleOrden.html"
    context_object_name = "orden"
    rol_requerido = ["cliente", "admin"]

    def get_queryset(self):
        qs = super().get_queryset()

        # Optimización de consultas:
        # - select_related: trae al mismo tiempo datos del solicitante (usuario)
        # - prefetch_related: trae items y productos relacionados para evitar N+1
        qs = qs.select_related("solicitante").prefetch_related("items__producto")

        return qs

    def get_context_data(self, **kwargs):
        # Obtener el contexto de la vista
        context = super().get_context_data(**kwargs)

        orden_obj = context.get("orden")

        if orden_obj:
            data_serializada = OrdenSerializer.serialize(orden_obj)

        context['orden_data'] = data_serializada

        return context


# Vista para txt
class OrdenTxtView(View):
    def get(self, request, pk):
        orden = get_object_or_404(Orden.objects.select_related('solicitante'), pk=pk)

        # Crea una instancia del exportador.
        exporter_txt = TxtExporter()
        
        # Crea una instancia del servicio y le inyecta el exportador.
        service = OrdenExportService(exporter=exporter_txt)
        
        # Llama al método `generate` del servicio.
        return service.generate(
            orden=orden,
            filename=f"pedido_{pk}.txt",
            content_type="text/plain"
        )


# Vista para Excel
class OrdenExcelView(View):
    def get(self, request, pk):
        orden = get_object_or_404(Orden.objects.select_related('solicitante'), pk=pk)

        exporter_excel = ExcelExporter()

        service = OrdenExportService(exporter=exporter_excel)

        return service.generate(
            orden,
            filename=f"pedido_{pk}.xlsx",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


class OrdenPortapapelesView(View):
    """Vista que devuelve el contenido de la orden en texto plano, sin descarga."""
    def get(self, request, pk):
        orden = get_object_or_404(Orden.objects.select_related('solicitante'), pk=pk)
        
        # Serializamos los datos de la orden
        data_serializada = OrdenSerializer.serialize(orden)
        
        # Usar el mismo exportador para generar el texto
        # Serializamos los datos de la orden
        exporter = TxtExporter()
        data = exporter.export(data_serializada)
        
        # Devolvemos el texto como una respuesta HTTP.
        # No usamos la cabecera 'Content-Disposition' para evitar la descarga.
        return HttpResponse(data, content_type="text/plain")
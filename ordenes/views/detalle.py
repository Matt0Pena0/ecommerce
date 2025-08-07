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
from ordenes.services.exporters.serializers import OrdenSerializer


class OrdenDetailView(LoginRequiredMixin, RolRequeridoMixin, PermisosDatosMixin, DetailView):
    model = Orden
    template_name = "ordenes/DetalleOrden.html"
    context_object_name = "orden"
    rol_requerido = ["cliente", "admin"]

    # def get_object(self, queryset=None):
    #     queryset = self.get_filtered_queryset(self.get_queryset())
    #     return get_object_or_404(queryset, pk=self.kwargs['pk'])


# Vista para txt
class OrdenTxtView(View):
    def get(self, request, pk):
        orden = get_object_or_404(Orden, pk=pk)
        
        # Aquí es donde ocurre la magia de la inyección de dependencias:
        # 1. Creamos una instancia del exportador (la dependencia).
        exporter_txt = TxtExporter()
        
        # 2. Creamos una instancia del servicio y le "inyectamos" el exportador.
        service = OrdenExportService(exporter=exporter_txt)
        
        # 3. Llamamos al método `generate` del servicio, el cual se encargará del resto.
        return service.generate(
            orden=orden,
            filename=f"pedido_{pk}.txt",
            content_type="text/plain"
        )


# Vista para Excel
class OrdenExcelView(View):
    def get(self, request, pk):
        orden = get_object_or_404(Orden, pk=pk)

        exporter_excel = ExcelExporter()

        service = OrdenExportService(exporter=exporter_excel)

        return service.generate(
            orden,
            filename=f"pedido_{pk}.xlsx",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


class OrdenTxtCopyView(View):
    """Vista que devuelve el contenido de la orden en texto plano, sin descarga."""
    def get(self, request, pk):
        orden = get_object_or_404(Orden, pk=pk)
        
        # Serializamos los datos de la orden
        rows = OrdenSerializer.serialize(orden)
        
        # Usamos el mismo exportador para generar el texto
        exporter = TxtExporter()
        data = exporter.export(rows)
        
        # Devolvemos el texto como una respuesta HTTP.
        # No usamos la cabecera 'Content-Disposition' para evitar la descarga.
        return HttpResponse(data, content_type="text/plain")
from django.http import HttpResponse

from ordenes.services.exporters.serializers import OrdenSerializer


class OrdenExportService:
    def __init__(self, exporter):
        self.exporter = exporter

    def generate(self, orden, filename: str, content_type: str):
        rows = OrdenSerializer.serialize(orden)
        data = self.exporter.export(rows)
        response = HttpResponse(data, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

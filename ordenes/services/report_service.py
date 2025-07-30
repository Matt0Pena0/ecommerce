# from django.http import HttpResponse
# from ordenes.services.serializers import OrdenSerializer
# from ordenes.services.exporters import HTMLExporter, TxtExporter
# #ExcelExporter, PDFExporter

# class OrdenReportService:
#     def __init__(self, exporter):
#         self.exporter = exporter

#     def generate(self, orden, filename: str, content_type: str) -> TxtExporter:
#         rows = OrdenSerializer.serialize(orden)
#         data = self.exporter.export(rows)
#         response = TxtExporter(data, content_type=content_type)
#         response["Content-Disposition"] = f'attachment; filename="{filename}"'
#         return response

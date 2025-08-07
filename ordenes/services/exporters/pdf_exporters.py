# from weasyprint import HTML
# from .html_exporter import HtmlExporter


# class OrdenPDFView:
#     def __init__(self, html_exporter: HtmlExporter):
#         self.html_exporter = html_exporter

#     def export(self, rows: list[dict]) -> bytes:
#         # Genera HTML y luego lo convierte a PDF (por ejemplo con WeasyPrint)
#         html = self.html_exporter.export(rows).decode("utf-8")
#         pdf = HTML(string=html).write_pdf()
#         return pdf

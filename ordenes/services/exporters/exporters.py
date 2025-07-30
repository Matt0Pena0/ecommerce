from typing import Protocol


class IExporter(Protocol):
    def export(self, rows: list[dict]) -> bytes:
        ...


# class HTMLExporter:
#     def __init__(self, template_name: str):
#         self.template_name = template_name

#     def export(self, rows: list[dict]) -> bytes:
#         from django.template.loader import render_to_string
#         html = render_to_string(self.template_name, {"rows": rows})
#         return html.encode("utf-8")


# class ExcelExporter:
#     def export(self, rows: list[dict]) -> bytes:
#         import io
#         import pandas as pd

#         df = pd.DataFrame(rows)
#         buffer = io.BytesIO()
#         with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
#             df.to_excel(writer, index=False, sheet_name="Pedido")
#         return buffer.getvalue()


# class PDFExporter:
#     def __init__(self, html_exporter: HTMLExporter):
#         self.html_exporter = html_exporter

#     def export(self, rows: list[dict]) -> bytes:
#         # Genera HTML y luego lo convierte a PDF (por ejemplo con WeasyPrint)
#         html = self.html_exporter.export(rows).decode("utf-8")
#         from weasyprint import HTML
#         pdf = HTML(string=html).write_pdf()
#         return pdf

from ordenes.services.exporters_interface import IExporter
from typing import Any
from django.template.loader import render_to_string

class HtmlExporter(IExporter):
    def __init__(self, template_name: str):
        self.template_name = template_name

    def export(self, context: dict[str, Any]) -> bytes:
        """
        Renderiza un template de Django con un contexto dado y lo devuelve como bytes.
        """
        # render_to_string recibe el diccionario de contexto completo,
        html = render_to_string(self.template_name, context)
        return html.encode("utf-8")
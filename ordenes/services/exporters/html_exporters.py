from exporters.exporters import IExporter


class HTMLExporter(IExporter):
    def __init__(self, template_name: str):
        self.template_name = template_name

    def export(self, rows: list[dict]) -> bytes:
        from django.template.loader import render_to_string
        html = render_to_string(self.template_name, {"rows": rows})
        return html.encode("utf-8")
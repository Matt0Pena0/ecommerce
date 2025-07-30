from .exporters import IExporter


class TxtExporter(IExporter):
    def export(self, rows: list[dict]) -> bytes:
        lines = []
        for r in rows:
            line = f"{r['cantidad']} ({r['unidad']}) de {r['nombre']} - {r['marca']}"
            lines.append(line)
        return "\n".join(lines).encode("utf-8")

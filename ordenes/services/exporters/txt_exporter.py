from io import BytesIO

class TxtExporter:
    def export(self, rows: list[dict]) -> bytes:
        # Acomodamos los datos para que el TxtExporter funcione con el OrdenSerializer
        lines = []
        for r in rows:
            line = f"{r['cantidad']} ({r['unidad']}) de {r['nombre']} - {r['marca']}"
            lines.append(line)
        return "\n".join(lines).encode("utf-8")
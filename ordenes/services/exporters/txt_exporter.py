from io import BytesIO

class TxtExporter:
    def export(self, rows: list[dict]) -> bytes:
        # Acomodamos los datos para que el TxtExporter funcione con el OrdenSerializer
        lines = []
        for r in rows:
            # Siempre mostramos cantidad y nombre
            line = f"{r['cantidad']} x {r['nombre']} {r['marca']}"

            # Si unidad o descripcion tienen algo, añadimos el bloque
            if r['unidad'] or r['descripcion']:
                line += f" - {r['unidad']} {r['descripcion']}"

            lines.append(line)
        return "\n".join(lines).encode("utf-8")
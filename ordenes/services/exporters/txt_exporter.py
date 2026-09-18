from io import BytesIO

class TxtExporter:
    def export(self, data_serializada: list[dict]) -> bytes:
        # Se extre y organiza los datos, para procesar.
        items = data_serializada.get("items" , [])

        encabezado = f"Orden: {data_serializada["id"]} - {data_serializada["fecha_creacion"]} | {data_serializada["solicitante_username"]} |{'\n'}"

        items_list = []
        for item in items:
            # Agrega `cantidad x nombre marca` ya serializados.
            line = f"{item.get('cantidad')} x {item.get('nombre')}"

            # Si hay marca, se agrega.
            line += f" {item.get('marca')}" if item.get('marca') else ""

            # Si hay undida y/o descripcion, se agregan.
            line += f" | {item.get('unidad')}" if item.get('unidad') else ""
            # line += f" - {item.get('descripcion')}" if item.get('descripcion') else ""

            # Poblar la lista de items
            items_list.append(line)

        # Generar la orden final.
        txt_final = encabezado
        txt_final += ("\n".join(items_list))

        return txt_final.encode("utf-8")

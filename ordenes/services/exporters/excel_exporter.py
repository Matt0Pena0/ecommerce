from io import BytesIO
import pandas as pd

from ordenes.services.exporters_interface import IExporter


class ExcelExporter(IExporter):
    def export(self, rows: list[dict]):
        # Convertir la lista de diccionarios en un DataFrame de pandas
        df = pd.DataFrame(rows)
        
        # Guardar el DataFrame en memoria usando un buffer
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Orden')
            
        buffer.seek(0)
        return buffer.getvalue()
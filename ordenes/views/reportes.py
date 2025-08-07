# from django.shortcuts import get_object_or_404
# from django.conf import settings
# import os

# from django.views import View
# from ordenes.models import Orden
# from ordenes.services.exporters.txt_exporter import TxtExporter
# from ordenes.services.serializers import OrdenSerializer
# # from ordenes.services.exporters.html_exporters import HTMLExporter
# ExcelExporter, PDFExporter



# def exportar_orden_a_txt(orden: Orden):
#     """
#     Función auxiliar que toma una orden, prepara los datos
#     y los exporta a un archivo .txt en la carpeta 'media/ordenes/'.
#     """
#     exporter = TxtExporter()
    
#     # 1. Preparamos los datos en el formato que espera el exporter
#     rows = OrdenSerializer(orden)
#     # Asumo que el related_name en el modelo ItemOrden es 'items'
#     for item in orden.items.all():
#         rows.append({
#             "cantidad": item.cantidad,
#             "unidad": item.producto.unidad_medida,
#             "nombre": item.producto.nombre,
#             "marca": item.producto.marca,
#         })
    
#     # 2. Generamos el contenido del archivo en bytes
#     if not rows:
#         return # No hacer nada si no hay items
        
#     contenido_bytes = exporter.export(rows)

#     # 3. Definimos la ruta y guardamos el archivo
#     # Aseguramos que el directorio 'media/ordenes' exista
#     directorio_salida = os.path.join(settings.MEDIA_ROOT, 'ordenes')
#     os.makedirs(directorio_salida, exist_ok=True)
    
#     nombre_archivo = f"pediado_{orden.pk}.txt"
#     ruta_completa = os.path.join(directorio_salida, nombre_archivo)
    
#     # Usamos 'wb' porque el contenido está en bytes
#     with open(ruta_completa, 'wb') as f:
#         f.write(contenido_bytes)


# class OrdenTxtView(View):
#     def get(self, pk):
#         orden = get_object_or_404(Orden, pk=pk)
#         service = TxtExporter()
#         return service.generate(
#             orden,
#             filename=f"pedido_{pk}.txt",
#             content_type="text/plain"
#         )

# class OrdenHTMLView(View):
#     def get(self, request, pk):
#         orden = get_object_or_404(Orden, pk=pk)
#         service = OrdenReportService(HTMLExporter("ordenes/templates/orden_list.html"))
#         return service.generate(
#             orden,
#             filename=f"orden_{pk}.html",
#             content_type="text/html"
#         )


# class OrdenExcelView(View):
#     def get(self, request, pk):
#         orden = Orden.objects.get(pk=pk)
#         service = OrdenReportService(ExcelExporter())
#         return service.generate(
#             orden,
#             filename=f"orden_{pk}.xlsx",
#             content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

# class OrdenPDFView(View):
#     def get(self, request, pk):
#         orden = Orden.objects.get(pk=pk)
#         html_exporter = HTMLExporter("ordenes/templates/orden_pdf.html")
#         service       = OrdenReportService(PDFExporter(html_exporter))
#         return service.generate(
#             orden,
#             filename=f"orden_{pk}.pdf",
#             content_type="application/pdf"
#         )


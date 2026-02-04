from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Carrito, ItemCarrito
from productos.models import Producto
from ordenes.services.crear_orden_service import OrdenService
from .serializers import ActualizarCarritoSerializer, CarritoDetalleSerializer


class CarritoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_carrito(self, request):
        """Obtiene o crea el carrito del usuario"""
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        return carrito

    def _resumen_carrito(self, carrito):
        """Helper para devolver el estado actualizado al JS"""
        # Obtiene La lista de todos los items del carrito
        items = carrito.items.all().values('producto_id', 'cantidad')
        # Recorre cada item de la lista de items y los desempaqueta en items_dict
        items_dict = {item['producto_id']: item['cantidad'] for item in items}
        # Suma todos los item['cantidades'], es decir los valores de cada par en items_dict
        total_items = sum(items_dict.values())

        # Devuelve el total de items, y el diccionario de que contiene cada item {prod_id: cantidad}
        return {
            "total_items": total_items,
            "items_dict": items_dict
        }


    @action(detail=False, methods=['get'])
    def status(self, request):
        """GET /api/carrito/status/ (Devuelve el estado del carrito actualizado)"""
        carrito = self._get_carrito(request)

        return Response(self._resumen_carrito(carrito))

    @action(detail=False, methods=['post'])
    def agregar(self, request):
        """POST /api/carrito/agregar/ (Agrega o actualiza la cantidad del producto)"""
        # Instancia el serializer, el atributo request.data recibe los datos para serializar
        serializer = ActualizarCarritoSerializer(data=request.data)
        
        # Si el contenido recibido por el serializer no es valido, 
        # devuelve error y HTTP_400
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extrae y declara los valores extraidos del serializer
        # para cada clave, respectivamente
        producto_id = serializer.validated_data['producto_id']
        cantidad = serializer.validated_data['cantidad']

        carrito = self._get_carrito(request)
        producto = get_object_or_404(Producto, id=producto_id)

        # Busca el item del producto recibido dentro del Carrito
        item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()

        try:
            # Si el producto recibido tiene cantidad 0, se elimina del carrito
            if cantidad == 0:
                if item: item.delete()
                msg = "Producto removido."
            
            else:
                # Verifica que la cantidad no sea mayor al stock
                if cantidad > producto.stock:
                    return Response({"message": f"Solo hay {producto.stock} en stock"}, status=status.HTTP_400_BAD_REQUEST)
                # Si existe el item, actualiza la cantidad
                if item:
                    item.cantidad = cantidad
                    item.save()
                # Sino envia y agrega el nuevo item recibido al carrito
                else:
                    ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)

                msg = "Carrito actualizado."

            # Llama al handler para actualizar el estado del carrito
            resumen = self._resumen_carrito(carrito)

            return Response({"status": "ok", "message": msg, "nuevo_total_productos": resumen["total_items"]})

        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @action(detail=False, methods=['get'])
    def items_detalle(self, request):
        """GET /api/carrito/items_detalle/ (Obtiene el listado detallado de cada item)"""
        carrito = self._get_carrito(request)

        # Optimiza la query trayendo productos y sus relaciones en una sola consulta a la DB
        carrito_query = Carrito.objects.prefetch_related(
            'items__producto__marca',
            'items__producto__categoria',
            'items__producto__gondola',
            'items__producto__unidad_medida',
        ).get(id=carrito.id)

        # Instancia el serializer con la query ya optimizada
        serializer = CarritoDetalleSerializer(carrito_query)

        return Response(serializer.data)


    @action(detail=True, methods=['delete'])
    def eliminar(self, request, pk=None):
        """DELETE /api/carrito/{producto_id}/eliminar/ (Eliminación directa)"""
        carrito = self._get_carrito(request)

        # Busca el item para eliminar
        item = get_object_or_404(ItemCarrito, carrito=carrito, producto_id=pk)
        item.delete()
        
        # Actualiza el estado del carrito
        resumen = self._resumen_carrito(carrito)

        return Response({
            "status": "ok", 
            "message": "Producto eliminado.", 
            "nuevo_total_productos": resumen["total_items"]
        })


    @action(detail=False, methods=['post'])
    def finalizar(self, request):
        """POST /api/carrito/finalizar/ (Checkout)"""
        carrito = self._get_carrito(request)
        
        # Comprueba que el carrito no está vacío
        if not carrito.items.exists():
            return Response({"message": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Transacción atómica para asegurar que no se pierdan datos
            with transaction.atomic():

                # Crea la estructura que espera recibir el services 'items[(prod, qnty), (...)]'
                items_orden = [(item.producto, item.cantidad) for item in carrito.items.select_related('producto')]

                # Instancia el servicio que maneja la orden
                orden_service = OrdenService()

                # Se envia la orden con el metodo .crear_orden() del servicio OrdenService()
                orden = orden_service.crear_orden(solicitante=request.user, items=items_orden)
                
                # Luego limpia el carrito
                carrito.items.all().delete()

            return Response({
                "status": "ok",
                "message": f"Orden #{orden.id} generada correctamente.",
                "orden_id": orden.id,
                "redirect_url": "/ordenes/listar/"
            })

        except Exception as e:
            return Response({"status": "error", "message": f"Error: {str(e)}"}, status=500)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from productos import serializer

from .models import Carrito, ItemCarrito
from productos.models import Producto
from ordenes.services.crear_orden_service import OrdenService
from .serializers import ActualizarCarritoSerializer, CarritoDetalleSerializer

class CarritoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_carrito(self, request):
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        return carrito

    def _resumen_carrito(self, carrito):
        """Helper para devolver el estado actualizado al JS"""
        items = carrito.items.all().values('producto_id', 'cantidad')
        items_dict = {item['producto_id']: item['cantidad'] for item in items}
        total_items = sum(items_dict.values())
        return {
            "total_items": total_items,
            "items_dict": items_dict
        }

    @action(detail=False, methods=['get'])
    def status(self, request):
        """GET /api/carrito/status/"""
        carrito = self._get_carrito(request)
        return Response(self._resumen_carrito(carrito))

    @action(detail=False, methods=['post'])
    def agregar(self, request):
        """POST /api/carrito/agregar/ (Crea o actualiza cantidad)"""
        serializer = ActualizarCarritoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        producto_id = serializer.validated_data['producto_id']
        cantidad = serializer.validated_data['cantidad']
        
        carrito = self._get_carrito(request)
        producto = get_object_or_404(Producto, id=producto_id)
        item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()

        try:
                
            if cantidad == 0:
                if item: item.delete()
                msg = "Producto removido."
            else:
                if cantidad > producto.stock:
                    return Response({"message": f"Solo hay {producto.stock} en stock"}, status=status.HTTP_400_BAD_REQUEST)
                
                if item:
                    item.cantidad = cantidad
                    item.save()
                else:
                    ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)
                msg = "Carrito actualizado."

            resumen = self._resumen_carrito(carrito)
            return Response({"status": "ok", "message": msg, "nuevo_total_productos": resumen["total_items"]})

        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def items_detalle(self, request):
        carrito = self._get_carrito(request)
        
        # Optimizamos trayendo productos y marcas de un solo viaje a la DB
        carrito_query = Carrito.objects.prefetch_related(
            'items__producto__marca'
        ).get(id=carrito.id)
        
        serializer = CarritoDetalleSerializer(carrito_query)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def eliminar(self, request, pk=None):
        """DELETE /api/carrito/{producto_id}/eliminar/ (Eliminación directa)"""
        carrito = self._get_carrito(request)
        item = get_object_or_404(ItemCarrito, carrito=carrito, producto_id=pk)
        item.delete()
        
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
        
        if not carrito.items.exists():
            return Response({"message": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            # Transacción atómica para asegurar que no se pierdan datos

            with transaction.atomic():
                items_orden = [(item.producto, item.cantidad) for item in carrito.items.select_related('producto')]
                
                orden_service = OrdenService()
                orden = orden_service.crear_orden(solicitante=request.user, items=items_orden)
                
                # Limpiar carrito
                carrito.items.all().delete()

            return Response({
                "status": "ok",
                "message": f"Orden #{orden.id} generada correctamente.",
                "orden_id": orden.id,
                "redirect_url": "/ordenes/listar/"
            })

        except Exception as e:
            return Response({"status": "error", "message": f"Error: {str(e)}"}, status=500)
from rest_framework import serializers
from decimal import Decimal

from .models import ItemCarrito, Carrito
from productos.serializer import ProductoDetalleSerializer


class ActualizarCarritoSerializer(serializers.Serializer):
    """Datos necesaria del producto para actualizarlo en el carrito"""
    producto_id = serializers.IntegerField(required=True)
    cantidad = serializers.IntegerField(required=True, min_value=0)


class ItemCarritoSerializer(serializers.ModelSerializer):
    """Trae el objeto Producto completo, usando su serializer para tener el producto completo"""
    producto = ProductoDetalleSerializer(read_only=True) 
    subtotal = serializers.SerializerMethodField()

    # Producto ya viene con todos los fields propios declarados más arriba
    class Meta:
        model = ItemCarrito
        fields = ['producto', 'cantidad', 'subtotal']

    def get_subtotal(self, obj):
        return obj.producto.precio_unitario * obj.cantidad


class CarritoDetalleSerializer(serializers.ModelSerializer):
    """En forma de arbol, se hereda de ItemCarrrito lo que se heredo de Producto y sus subtotales"""
    items = ItemCarritoSerializer(many=True, read_only=True)
    total_unidades = serializers.SerializerMethodField()
    total_dinero = serializers.SerializerMethodField()

    # Además de cada item, con cada producto, agregamos el total de unidades y el total de dinero
    class Meta:
        model = Carrito
        fields = ['items', 'total_unidades', 'total_dinero']

    def get_total_unidades(self, obj):
        return sum(item.cantidad for item in obj.items.all())

    def get_total_dinero(self, obj):
        total = sum((item.producto.precio_unitario * item.cantidad) for item in obj.items.all())
        return Decimal(total).quantize(Decimal('0.01'))
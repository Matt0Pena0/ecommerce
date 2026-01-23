from rest_framework import serializers
from decimal import Decimal

from .models import ItemCarrito, Carrito
from productos.models import Producto


class ProductoCarritoSerializer(serializers.ModelSerializer):
    """Información mínima necesaria del producto para mostrar en la tabla"""
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')
    unidad_nombre = serializers.ReadOnlyField(source='unidad_medida.nombre')
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'img', 'marca_nombre', 'stock', 'precio_unitario', 'descripcion', 'unidad_nombre']


class ActualizarCarritoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField(required=True)
    cantidad = serializers.IntegerField(required=True, min_value=0)


class ItemCarritoSerializer(serializers.ModelSerializer):
    # Usamos el serializer del producto para tener el objeto completo: item.producto.nombre, etc.
    producto = ProductoCarritoSerializer(read_only=True) 
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrito
        fields = ['producto', 'cantidad', 'subtotal'] # producto contiene id, nombre, img, etc.

    def get_subtotal(self, obj):
        return obj.producto.precio_unitario * obj.cantidad


class CarritoDetalleSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    total_unidades = serializers.SerializerMethodField()
    total_dinero = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['items', 'total_unidades', 'total_dinero']

    def get_total_unidades(self, obj):
        # CORRECCIÓN: Solo sumamos las cantidades
        return sum(item.cantidad for item in obj.items.all())

    def get_total_dinero(self, obj):
        total = sum((item.producto.precio_unitario * item.cantidad) for item in obj.items.all())
        return Decimal(total).quantize(Decimal('0.01'))
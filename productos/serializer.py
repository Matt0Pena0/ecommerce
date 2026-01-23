from rest_framework import serializers
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    # Trae los nombres de las relaciones para pasarlos al frontend
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    codigo_str = serializers.ReadOnlyField(source='codigo.codigo')

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'marca_nombre', 'categoria_nombre', 
            'precio_unitario', 'stock', 'codigo_str', 'img'
        ]
from rest_framework import serializers
from .models import Producto, Codigo


class ProductoBaseSerializer(serializers.ModelSerializer):
    """Información esencial para listados rápidos (Catálogo)"""

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'img', 'stock', 'precio_unitario', 'descripcion', 'precio_unitario']


class ProductoDetalleSerializer(ProductoBaseSerializer):
    """Información completa para Carrito o Vista de Detalle"""
    # Registra los valores de las relaciones
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    gondola_nombre = serializers.ReadOnlyField(source='gondola.nombre')
    unidad_nombre = serializers.ReadOnlyField(source='unidad_medida.nombre')
    codigo_str = serializers.ReadOnlyField(source='codigo.codigo')

    codigo_input = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta(ProductoBaseSerializer.Meta):
        # Hereda los campos del padre y suma los específicos
        model = Producto
        fields = ProductoBaseSerializer.Meta.fields + [
            # IDs para escritura
            'marca_nombre', 'categoria_nombre', 'gondola_nombre', 'unidad_nombre', 'codigo_input',
            # Nombres para lectura
            'marca', 'categoria', 'gondola', 'unidad_medida', 'codigo_str'
        ]
        
    def create(self, validated_data):
        # Extrae el codigo string
        codigo_str = validated_data.pop('codigo_input', None)

        if codigo_str:
            # Si existe lo obtiene, sino lo crea.
            codigo_obj, _ = Codigo.objects.get_or_create(codigo=codigo_str)
            validated_data['codigo'] = codigo_obj
        else:
            validated_data['codigo'] = None

        return super().create(validated_data)

    def update(self, instance, validated_data):
        codigo_str = validated_data.pop('codigo_input', None)

        # Comprueba si el campo viene en la petición
        if codigo_str is not None:
                    if codigo_str == "":
                        instance.codigo = None
                    else:
                        # Si viene el codigo, lo busca o crea y lo asigna
                        codigo_obj, _ = Codigo.objects.get_or_create(codigo=codigo_str)
                        instance.codigo = codigo_obj
                
        return super().update(instance, validated_data)
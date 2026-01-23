from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Producto, Marca, Categoria, Gondola
from .serializer import ProductoSerializer


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    # Optimizamos la consulta antes de serializar
    queryset = Producto.objects.select_related(
        'marca', 'categoria', 'codigo', 'gondola', 'unidad_medida'
    ).all()
    serializer_class = ProductoSerializer

    # Activa el filtrado y orden
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # Configura los filtros
    filterset_fields = ['categoria', 'marca', 'gondola']

    # Configura la busqueda
    search_fields = ['nombre', 'codigo__codigo', 'marca__nombre']

    # Configura el orden
    ordering_fields = ['precio_unitario', 'stock', 'nombre', 'marca__nombre']
    ordering = ['nombre'] # Default

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def metadata(self, request):
        """
        Endpoint: GET /api/productos/metadata/
        Devuelve las listas para poblar los filtros del frontend.
        """
        return Response({
            "marcas": list(Marca.objects.values("id", "nombre").order_by('nombre')),
            "categoria": list(Categoria.objects.values("id", "nombre").order_by('nombre')),
            "gondolas": list(Gondola.objects.values("id", "nombre").order_by('nombre')),
            "ordenamiento": [
                {"key": "nombre", "label": "Nombre (A-Z)"},
                {"key": "-nombre", "label": "Nombre (Z-A)"},
                {"key": "precio_unitario", "label": "Precio (Menor a Mayor)"},
                {"key": "-precio_unitario", "label": "Precio (Mayor a Menor)"},
            ]
        })
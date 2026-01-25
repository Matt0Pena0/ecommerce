from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductoFilter
from .models import Producto, Marca, Categoria, Gondola, UnidadMedida
from .serializer import ProductoDetalleSerializer


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: Solo admins puede manejar CRUD.
    El resto de usuarios solo podrá leer
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class ProductoViewSet(viewsets.ModelViewSet):
    # Optimiza la consulta antes de serializar
    queryset = Producto.objects.select_related(
        'marca', 'categoria', 'codigo', 'gondola', 'unidad_medida'
    ).all()

    serializer_class = ProductoDetalleSerializer

    permission_classes = [IsAdminUserOrReadOnly]

    # Activa el filtrado y orden
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # Configura los filtros
    filterset_class = ProductoFilter

    # Configura la busqueda
    search_fields = ['nombre', 'marca__nombre', 'categoria__nombre']

    # Configura el orden
    ordering_fields = ['nombre', 'precio_unitario', 'stock', 'marca__nombre']
    ordering = ['nombre'] # por defecto

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def metadata(self, request):
        """
        Endpoint: GET /api/productos/metadata/
        Devuelve las listas para poblar los filtros del frontend.
        """
        return Response({
            "marcas": list(Marca.objects.values("id", "nombre").order_by('nombre')),
            "categorias": list(Categoria.objects.values("id", "nombre").order_by('nombre')),
            "gondolas": list(Gondola.objects.values("id", "nombre").order_by('nombre')),
            "unidades": list(UnidadMedida.objects.values("id", "nombre").order_by('nombre')),
            "ordenamiento": [
                {"key": "nombre", "label": "Nombre (A-Z)"},
                {"key": "-nombre", "label": "Nombre (Z-A)"},
                {"key": "precio_unitario", "label": "Precio (Menor a Mayor)"},
                {"key": "-precio_unitario", "label": "Precio (Mayor a Menor)"},
            ]
        })
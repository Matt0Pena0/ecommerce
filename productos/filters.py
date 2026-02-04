import django_filters

from .models import Producto


class ProductoFilter(django_filters.FilterSet):
    """Maneja los filtros de productos para la sidebar"""
    marca = django_filters.NumberFilter(field_name='marca__id')
    categoria = django_filters.NumberFilter(field_name='categoria__id')
    gondola = django_filters.NumberFilter(field_name='gondola__id')

    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    codigo = django_filters.CharFilter(field_name='codigo__codigo', lookup_expr='icontains')

    stock_status = django_filters.CharFilter(method='filter_stock')

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'marca', 'gondola', 'codigo']

    def filter_stock(self, queryset, name, value):
        if value == 'available':
            return queryset.filter(stock__gt=0)
        elif value == 'out':
            return queryset.filter(stock=0)
        return queryset

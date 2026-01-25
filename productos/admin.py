from django.contrib import admin
from django.utils.html import format_html
from productos.models import (
    Producto,
    UnidadMedida,
    Marca,
    Categoria,
    Gondola,
    Codigo,
)


@admin.register(Codigo)
class CodigoAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo")
    search_fields = ("codigo",)

@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)

@admin.register(Gondola)
class GondolaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


class StockFilter(admin.SimpleListFilter):
    title = 'Estado del Stock'
    
    parameter_name = 'rango_stock'

    def lookups(self, request, model_admin):
        """
        Define las opciones que aparecen en la barra lateral.
        Formato: (valor_interno, etiqueta_visible)
        """
        return (
            ('sin_stock', '❌ Sin Stock (0)'),
            ('bajo', '⚠️ Stock Bajo (1-10)'),
            ('normal', '✅ Stock Normal (> 10)'),
        )

    def queryset(self, request, queryset):
        """
        Aplica el filtro a la consulta según la opción seleccionada.
        """
        if self.value() == 'sin_stock':
            return queryset.filter(stock=0)
        
        if self.value() == 'bajo':
            return queryset.filter(stock__gt=0, stock__lte=10)
        
        if self.value() == 'normal':
            return queryset.filter(stock__gt=10)
        
        # Si no se selecciona nada, devuelve todos
        return queryset


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_select_related = (
        "marca", 
        "categoria", 
        "gondola", 
        "unidad_medida", 
        "codigo"
    )

    list_display = (
        "id",
        "nombre",
        "get_codigo_str",
        "marca",
        "gondola",
        "categoria",
        "unidad_medida",
        "precio_unitario",
        "stock",
        "ver_imagen",
    )

    list_filter = (
        "marca",
        "gondola",
        "categoria",
        StockFilter,
        "unidad_medida",
    )

    search_fields = (
        "id",
        "nombre",
        "codigo__codigo",
        "marca__nombre",
        "categoria__nombre",
        "gondola__nombre",
        "unidad_medida__nombre",
    )

    autocomplete_fields = ("marca", "categoria", "gondola", "unidad_medida", "codigo")


    # --- Métodos Custom para el Admin ---
    @admin.display(description="Cód")
    def get_codigo_str(self, obj):
        """Muestra el código en texto en vez del objeto Codigo"""
        return obj.codigo.codigo if obj.codigo else "-"

    @admin.display(description="Imagen")
    def ver_imagen(self, obj):
        """Renderiza una miniatura de la imagen"""
        if obj.img:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 4px;" />',
                obj.img.url
            )
        return "-"

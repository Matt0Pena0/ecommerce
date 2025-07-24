from django.contrib import admin
from productos.models import (
    Producto,
    UnidadMedida,
    Marca,
    Categoria,
    Gondola,
)


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


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "codigo",
        "marca",
        "categoria",
        "gondola",
        "unidad_medida",
        "precio_unitario",
        "stock",
    )
    list_filter = (
        "marca",
        "categoria",
        "gondola",
        "unidad_medida",
    )
    search_fields = (
        "nombre",
        "codigo__codigo",
        "marca__nombre",
        "categoria__nombre",
        "gondola__nombre",
        "unidad_medida__nombre",
    )
    autocomplete_fields = ("marca", "categoria", "gondola", "unidad_medida")

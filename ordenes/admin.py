from django.contrib import admin
from ordenes.models import Orden, EstadoOrden


@admin.register(EstadoOrden)
class EstadoOrdenAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ("id", "solicitante", "estado", "creado")
    list_filter = ("estado", "solicitante", "creado")
    search_fields = ("solicitante__username", "solicitante__email",)
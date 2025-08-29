from django.contrib import admin
from ordenes.models import Orden, EstadoOrden


@admin.register(EstadoOrden)
class EstadoOrdenAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ("id", "solicitante", "estado")
    list_filter = ("estado", "solicitante")
    search_fields = ("solicitante__username", "solicitante__email",)
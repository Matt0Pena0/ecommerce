from django.contrib import admin

from .models import UsuarioBase, RolesBase


@admin.register(UsuarioBase)
class UsuarioBaseAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "rol"]


@admin.register(RolesBase)
class RolesBaseAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
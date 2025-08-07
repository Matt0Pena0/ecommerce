from django.contrib import admin

from .models import UsuarioBase


@admin.register(UsuarioBase)
class UsuarioBaseAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "direccion"]


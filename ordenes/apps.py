from django.apps import AppConfig
from django.db import connection
from django.db.models.signals import post_migrate

class OrdenesConfig(AppConfig):
    name = "ordenes"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        pass
        # from .models import EstadoOrden

        # def crear_estados(sender, **kwargs):
        #     with connection.cursor() as cursor:
        #         tables = connection.introspection.table_names()
        #         if "ordenes_estadoorden" in tables:
        #             for id, _ in EstadoOrden.S:
        #                 EstadoOrden.objects.get_or_create(nombre=id)

        # post_migrate.connect(crear_estados, sender=self)


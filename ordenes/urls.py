from django.urls import path

from ordenes.views.crear import crear_orden
from ordenes.views.listar import OrdenListView


app_name = "ordenes"

urlpatterns = [
    path("crear/", crear_orden, name="crear"),
    path("listar/", OrdenListView.as_view(), name="listar"),
]
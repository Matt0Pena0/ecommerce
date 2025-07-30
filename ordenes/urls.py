from django.urls import path

from ordenes.views.listar import OrdenListView
from ordenes.views.crear import crear_orden


app_name = "ordenes"

urlpatterns = [
    path("crear/", crear_orden, name="crear"),
    path("listar/", OrdenListView.as_view(), name="listar"),
]
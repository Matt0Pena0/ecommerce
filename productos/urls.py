from django.urls import path

from productos.views.listar import ProductoListView
from productos.views.admin.crear import ProductosAdminCreateView
from productos.views.admin.actualizar import ProductosAdminUpdateView
from productos.views.admin.eliminar import ProductoDeleteAPIView, ProductosAdminDeleteView


app_name = "productos"

urlpatterns = [
    path("listar/", ProductoListView.as_view(), name="listar"),
    
    path("api-old/admin/eliminar/<int:pk>/", ProductoDeleteAPIView.as_view(), name="eliminar"),
    path("admin/crear", ProductosAdminCreateView.as_view(), name="crear"),
    path("admin/actualizar/<int:pk>", ProductosAdminUpdateView.as_view(), name="actualizar"),
    path("admin/eliminar/<int:pk>", ProductosAdminDeleteView.as_view(), name="eliminar"),
]
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from accounts.utils import RolRequeridoMixin
from productos.models import Producto


from django.http import JsonResponse


class ProductoDeleteAPIView(LoginRequiredMixin, RolRequeridoMixin, DeleteView):
    model = Producto
    rol_requerido = 'admin'

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'status': 'ok', 'message': 'Producto eliminado'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class ProductosAdminDeleteView(LoginRequiredMixin, RolRequeridoMixin, DeleteView):
    """
    Vista de eliminación de productos en el panel de administración.

    Requiere autenticación del usuario. Muestra una confirmación antes de eliminar
    definitivamente una instancia de Producto.

    Atributos:
        `model` (Producto): Modelo que se elimina.
        `template_name` (str): Ruta al template de confirmación.
        `success_url` (str): URL de redirección tras la eliminación exitosa.
    """
    rol_requerido = ["admin"]
    model = Producto
    template_name = "productos/admin/EliminarProducto.html"
    success_url = reverse_lazy("productos:listar")
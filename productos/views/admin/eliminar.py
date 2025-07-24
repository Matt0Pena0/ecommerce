from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from productos.models import Producto


class ProductosAdminDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "productos/admin/EliminarProducto.html"
    success_url = reverse_lazy("productos:listar")
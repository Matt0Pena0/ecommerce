from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.utils import RolRequeridoMixin, PermisosDatosMixin
from ordenes.models import Orden


class OrdenListView(LoginRequiredMixin, RolRequeridoMixin, PermisosDatosMixin, ListView):
    model = Orden
    template_name = "ordenes/ListarOrdenes.html"
    context_object_name = "ordenes"
    rol_requerido = ["cliente", "admin"]

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return self.get_filtered_queryset(qs)

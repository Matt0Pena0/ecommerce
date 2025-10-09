from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.utils import RolRequeridoMixin, PermisosDatosMixin
from ordenes.models import Orden


class OrdenListView(LoginRequiredMixin, RolRequeridoMixin, PermisosDatosMixin, ListView):
    model = Orden
    template_name = "ordenes/ListarOrdenes.html"
    context_object_name = "ordenes"
    rol_requerido = ["cliente", "admin"]

    # Paginación
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()

        # select_related: trae al mismo tiempo datos del solicitante
        qs = qs.select_related("solicitante")

        return qs
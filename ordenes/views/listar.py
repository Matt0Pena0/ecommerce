from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ordenes.models import Orden


class OrdenListView(LoginRequiredMixin, ListView):
    model = Orden
    template_name = "ordenes/ListarOrdenes.html"
    context_object_name = "ordenes"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Orden.objects.all().order_by("-creado")

        return Orden.objects.filter(solicitante=user).order_by("-creado")
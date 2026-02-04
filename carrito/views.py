from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CarritoListView(LoginRequiredMixin, TemplateView):
    """
    App Shell para el carrito. 
    La lógica de items y totales se maneja vía API/JS.
    """
    template_name = "ListarCarrito.html"
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ProductoListView(LoginRequiredMixin, TemplateView):
    """
    Vista con control de usuario, para listar Productos
    con filtros, buscador y orden dinámico.  

    - redirect_url: a dónde redirigir si no tiene permiso. "usuario:login"  
    - :template:`ListarProductos.html`  
    
    """
    redirect_url = "accounts:login"
    template_name = "ListarProductos.html"

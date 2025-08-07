from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from productos.models import Producto, Marca, Categoria, Gondola


class ProductoListView(LoginRequiredMixin, ListView):
    """
    Vista con control de usuario, para listar Productos
    con filtros, buscador y orden dinámico.  

    - redirect_url: a dónde redirigir si no tiene permiso. "usuario:login"  
    - :template:`productos/ListarProductos.html`  
    
    """
    redirect_url = "usuarios:login"
    model = Producto
    template_name = "productos/ListarProductos.html"
    context_object_name = "productos"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    ORDER_FIELDS = {
        "codigo":            "codigo__codigo",
        "-codigo":           "-codigo__codigo",
        "nombre":            "nombre",
        "-nombre":           "-nombre",
        "precio_asc":        "precio_unitario",
        "precio_desc":       "-precio_unitario",
        "stock_asc":         "stock",
        "stock_desc":        "-stock",
        "marca":             "marca__nombre",
        "-marca":            "-marca__nombre",
    }

    def get_queryset(self):
        qs = super().get_queryset().order_by("nombre")
        params = self.request.GET

        # Búsqueda por nombre o código
        q = params.get("q")
        codigo = params.get("codigo")
        if q:
            qs = qs.filter(nombre__icontains=q)
        if codigo:
            qs = qs.filter(codigo__codigo__icontains=codigo)

        # Filtros
        if params.get("marca"):
            qs = qs.filter(marca_id=params["marca"])
        if params.get("categoria"):
            qs = qs.filter(categoria_id=params["categoria"])
        if params.get("gondola"):
            qs = qs.filter(gondola_id=params["gondola"])

        # Filtro de stock
        stock = params.get("stock")
        if stock == "available":
            qs = qs.filter(stock__gt=0)
        elif stock == "out":
            qs = qs.filter(stock__lte=0)

        # — Aplicar ordering dinámico —
        order_key = params.get("order")
        order_by  = self.ORDER_FIELDS.get(order_key, "nombre")
        
        return qs.order_by(order_by)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Para poblar los dropdowns
        ctx["marcas"]     = Marca.objects.all()
        ctx["categorias"] = Categoria.objects.all()
        ctx["gondolas"]   = Gondola.objects.all()

        ctx["order_fields"] = [
            {"key": k, "label": lbl} for k, lbl in [
                ("codigo",      "Código ↑"),
                ("-codigo",      "Código ↓"),
                ("nombre",      "Nombre ↑"),
                ("-nombre",     "Nombre ↓"),
                ("precio_asc",  "Precio ↑"),
                ("precio_desc", "Precio ↓"),
                ("stock_asc",   "Stock ↑"),
                ("stock_desc",  "Stock ↓"),
                ("marca",       "Marca ↑"),
                ("-marca",      "Marca ↓"),
            ]
        ]
        # Guardamos la selección actual
        ctx["current_order"] = self.request.GET.get("order", "nombre")

        return ctx

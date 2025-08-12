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
        
        # Datos para poblar los dropdowns
        ctx["marcas"]     = Marca.objects.all()
        ctx["categorias"] = Categoria.objects.all()
        ctx["gondolas"]   = Gondola.objects.all()

        # Orden
        ctx["order_fields"] = [
            {"key": k, "label": lbl} for k, lbl in [
                ("codigo",      "Código ↑"),
                ("-codigo",     "Código ↓"),
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
        ctx["current_order"] = self.request.GET.get("order", "nombre")
        ctx["current_order_label"] = next(
            (o["label"] for o in ctx["order_fields"] if o["key"] == ctx["current_order"]),
            "Ordenar por..."
        )

        # Marca
        marca_id = self.request.GET.get("marca", "")
        ctx["current_marca"] = marca_id
        ctx["current_marca_label"] = next(
            (m.nombre for m in ctx["marcas"] if str(m.id) == marca_id),
            "--Marca--"
        )

        # Categoría
        categoria_id = self.request.GET.get("categoria", "")
        ctx["current_categoria"] = categoria_id
        ctx["current_categoria_label"] = next(
            (c.nombre for c in ctx["categorias"] if str(c.id) == categoria_id),
            "--Categoría--"
        )

        # Góndola
        gondola_id = self.request.GET.get("gondola", "")
        ctx["current_gondola"] = gondola_id
        ctx["current_gondola_label"] = next(
            (g.nombre for g in ctx["gondolas"] if str(g.id) == gondola_id),
            "--Góndola--"
        )

        # Stock
        stock_val = self.request.GET.get("stock", "")
        ctx["current_stock"] = stock_val
        ctx["current_stock_label"] = {
            "available": "Con stock",
            "out": "Sin stock"
        }.get(stock_val, "--Stock--")

        return ctx



    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     # Para poblar los dropdowns
    #     ctx["marcas"]     = Marca.objects.all()
    #     ctx["categorias"] = Categoria.objects.all()
    #     ctx["gondolas"]   = Gondola.objects.all()

    #     ctx["order_fields"] = [
    #         {"key": k, "label": lbl} for k, lbl in [
    #             ("codigo",      "Código ↑"),
    #             ("-codigo",      "Código ↓"),
    #             ("nombre",      "Nombre ↑"),
    #             ("-nombre",     "Nombre ↓"),
    #             ("precio_asc",  "Precio ↑"),
    #             ("precio_desc", "Precio ↓"),
    #             ("stock_asc",   "Stock ↑"),
    #             ("stock_desc",  "Stock ↓"),
    #             ("marca",       "Marca ↑"),
    #             ("-marca",      "Marca ↓"),
    #         ]
    #     ]
    #     # Guardamos la selección actual
    #     ctx["current_order"] = self.request.GET.get("order", "nombre")

    #     return ctx

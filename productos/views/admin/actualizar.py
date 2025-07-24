from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from productos.forms import ProductoForm
from productos.models import Producto, Codigo, Marca, Categoria, Gondola, UnidadMedida


class ProductosAdminUpdateView(LoginRequiredMixin, UpdateView):
    redirect_url = "usuarios:login"
    model = Producto
    form_class = ProductoForm
    template_name = "productos/admin/FormularioProducto.html"
    success_url = reverse_lazy("productos:listar")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        producto = form.save(commit=False)
        codigo_str = form.cleaned_data["codigo"]

        if codigo_str:
            codigo_obj, _ = Codigo.objects.get_or_create(codigo=codigo_str)
            producto.codigo = codigo_obj
        # si está en blanco, dejam el código actual intacto

        producto.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Los mismos que para la lista de productos
        ctx["codigos"]    = Codigo.objects.values_list("codigo", flat=True)
        ctx["marcas"]     = Marca.objects.values_list("nombre", flat=True)
        ctx["categorias"] = Categoria.objects.values_list("nombre", flat=True)
        ctx["gondolas"]   = Gondola.objects.values_list("nombre", flat=True)
        ctx["unidades"]   = UnidadMedida.objects.values_list("nombre", flat=True)
        return ctx
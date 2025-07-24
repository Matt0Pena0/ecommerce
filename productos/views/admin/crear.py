from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from productos.forms import ProductoForm
from productos.models import Codigo, Marca, Categoria, Gondola, UnidadMedida


class ProductosAdminCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductoForm
    template_name = "productos/admin/FormularioProducto.html"
    success_url = reverse_lazy("productos:listar")

    def form_valid(self, form):
        # 1) instanciar sin guardar
        producto = form.save(commit=False)

        # 2) obtener o crear el código
        codigo_str = form.cleaned_data["codigo"]
        
        if codigo_str:
            codigo_obj, _ = Codigo.objects.get_or_create(codigo=codigo_str)
        else:
            codigo_obj = Codigo.objects.create()

        producto.codigo = codigo_obj

        # 3) guardar el producto con su FK a Codigo
        producto.save()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["codigos"]    = Codigo.objects.values_list("codigo", flat=True)
        ctx["marcas"]     = Marca.objects.values_list("nombre", flat=True)
        ctx["categorias"] = Categoria.objects.values_list("nombre", flat=True)
        ctx["gondolas"]   = Gondola.objects.values_list("nombre", flat=True)
        ctx["unidades"]   = UnidadMedida.objects.values_list("nombre", flat=True)
        return ctx
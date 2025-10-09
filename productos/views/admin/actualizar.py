from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from accounts.utils import RolRequeridoMixin
from productos.forms import ProductoForm
from productos.models import Producto, Codigo, Marca, Categoria, Gondola, UnidadMedida


class ProductosAdminUpdateView(LoginRequiredMixin, RolRequeridoMixin, UpdateView):
    """
    Vista de actualización para productos en el panel de administración.

    Requiere autenticación del usuario. Permite editar los datos de un producto
    existente, incluyendo la asociación con un código único.

    Atributos:
        `model` (Producto): Modelo que se edita.
        `form_class` (ProductoForm): Formulario utilizado para la edición.
        `template_name` (str): Ruta al template HTML.
        `success_url` (str): URL de redirección tras guardar exitosamente.

    Métodos:
        _dispatch()_: Maneja la solicitud HTTP y aplica la verificación de login.
        _form_valid(form)_: Procesa el formulario válido, actualiza el código si es necesario.
        _get_context_data(**kwargs)_: Agrega datos auxiliares al contexto del template.
    """
    rol_requerido = ["admin"]
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

        # Si no se proporciona un nuevo código, se conserva el actual
        # si está en blanco, dejam el código actual intacto
        if codigo_str:
            codigo_obj, _ = Codigo.objects.get_or_create(codigo=codigo_str)
            producto.codigo = codigo_obj

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
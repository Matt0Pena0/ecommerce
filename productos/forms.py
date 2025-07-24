from django import forms
import unicodedata
import re

from productos.models import Producto, Codigo, Marca, Categoria, Gondola, UnidadMedida


class CreateOrGetModelChoiceField(forms.ModelChoiceField):
    """
    Un ModelChoiceField que, si el valor no coincide con ninguna instancia,
    la crea con get_or_create() usando el campo `nombre`.
    """

    def normalize(self, value: str) -> str:
        """
        Devuelve una versión normalizada del string:
        - minúsculas
        - sin tildes
        - sin puntuación básica
        - sin espacios redundantes
        """
        value = value.strip().lower()
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("utf-8")
        value = re.sub(r"[^\w\s]", "", value)  # elimina puntuación
        value = re.sub(r"\s+", " ", value)     # reduce espacios múltiples
        return value

    def to_python(self, value):
        if hasattr(value, "pk"):
            return value

        if not value:
            return None

        normalized_input = self.normalize(value)
        qs = self.queryset

        for obj in qs:
            if self.normalize(obj.nombre) == normalized_input:
                return obj

        # Si no coincide con ninguno, crear uno nuevo
        model = qs.model
        obj, _ = model.objects.get_or_create(nombre=value.strip())
        return obj

    def prepare_value(self, value):
        if isinstance(value, int) or isinstance(value, str):
            try:
                obj = self.queryset.model.objects.get(pk=value)
                return getattr(obj, "nombre", str(value))
            except self.queryset.model.DoesNotExist:
                return str(value)
        elif hasattr(value, "nombre"):
            return value.nombre
        return super().prepare_value(value)

class ProductoForm(forms.ModelForm):
    codigo = forms.CharField(
        max_length=20,
        required=False,
        label="Código",

        widget=forms.TextInput(attrs={
            "list": "codigos_list",
            "placeholder": "Código…",
            "id": "id_codigo"
        })
    )
    marca = CreateOrGetModelChoiceField(
        queryset=Marca.objects.all(),
        required=False,
        widget=forms.TextInput(attrs={
            "list": "marcas_list",
            "placeholder": "Escribe o elige marca",
            "nombre": "nombre_marca"
        })
    )
    categoria = CreateOrGetModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        widget=forms.TextInput(attrs={
            "list": "categorias_list",
            "placeholder": "Escribe o elige categoría",
            "nombre": "nombre_categoria"
        })
    )
    gondola = CreateOrGetModelChoiceField(
        queryset=Gondola.objects.all(),
        required=False,
        widget=forms.TextInput(attrs={
            "list": "gondolas_list",
            "placeholder": "Escribe o elige góndola",
            "nombre": "nombre_gondola"
        })
    )
    unidad_medida = CreateOrGetModelChoiceField(
        queryset=UnidadMedida.objects.all(),
        required=False,
        widget=forms.TextInput(attrs={
            "list": "unidades_list",
            "placeholder": "Escribe o elige unidad",
            "nombre": "nombre_unidad_medida"
        })
    )

    class Meta:
        model  = Producto
        exclude = ["codigo"]
        fields = [
            "nombre", "marca", "categoria", "gondola",
            "unidad_medida", "precio_unitario", "descripcion", "stock"
        ]

    def clean_codigo(self):
        val = self.cleaned_data.get("codigo", "").strip()
        if not val:
            return None
        qs = Codigo.objects.filter(codigo=val)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.codigo_id)
        if qs.exists():
            raise forms.ValidationError("Ese código ya está en uso.")
        return val


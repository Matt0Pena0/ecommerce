# productos/forms.py

from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'codigo', 'descripcion', 'precio_unitario', 'stock',
            'marca', 'categoria', 'gondola', 'unidad_medida',
        ]

        labels = {
            'nombre': 'Nombre del Producto',
            'precio_unitario': 'Precio Unitario',
            'unidad_medida': 'Unidad de Medida',
            # 'onSale': '¿Está en oferta?',
            # 'precio_oferta': 'Precio de Oferta',
        }

        # 3. Diccionario de WIDGETS para añadir atributos HTML (clases, placeholders, etc.)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', "placeholder": "Descripción"}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', "placeholder": "Precio Unitario"}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'precio_oferta': forms.NumberInput(attrs={'class': 'form-control'}),
            
            # Para los ForeignKey, el widget Select es el estándar
            'marca': forms.Select(attrs={'class': 'form-select', "placeholder": "Marca"}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'gondola': forms.Select(attrs={'class': 'form-select'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),

            # Para el BooleanField, usamos un Checkbox
            # 'onSale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



# from django import forms
# from django.core.exceptions import ValidationError

# import unicodedata
# import re

# from productos.models import Producto, Codigo, Marca, Categoria, Gondola, UnidadMedida


# class CreateOrGetModelChoiceField(forms.ModelChoiceField):
#     """
#     Campo personalizado que extiende ModelChoiceField.

#     Permite ingresar texto libre en lugar de seleccionar una opción existente.
#     Si el valor ingresado no coincide con ninguna instancia del queryset,
#     se crea una nueva utilizando el campo `nombre`.

#     Métodos:
#         normalize(value): Normaliza el texto para comparación (minúsculas, sin tildes, sin puntuación).
#         to_python(value): Devuelve la instancia correspondiente o crea una nueva si no existe.
#         prepare_value(value): Convierte el valor para mostrarlo correctamente en el formulario.
#     """
#     def normalize(self, value: str) -> str:
#         """
#         Devuelve una versión normalizada del string:
#         - minúsculas
#         - sin tildes
#         - sin puntuación básica
#         - sin espacios redundantes
#         """
#         value = value.strip().lower()
#         value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("utf-8")
#         value = re.sub(r"[^\w\s]", "", value)  # elimina puntuación
#         value = re.sub(r"\s+", " ", value)     # reduce espacios múltiples
#         return value

#     def to_python(self, value):
#         # Si el valor está vacío, no hacemos nada
#         if not value:
#             return None

#         # CASO 1: El valor es un número (probablemente un ID de un objeto existente)
#         # Intentamos buscarlo por clave primaria (pk)
#         if value.isdigit():
#             try:
#                 # El super().to_python() de ModelChoiceField ya hace esta búsqueda por pk
#                 return super().to_python(value)
#             except ValidationError:
#                 # Si el ID no existe, tratamos el número como texto para crear uno nuevo
#                 pass
        
#         # CASO 2: El valor es texto (queremos crear un objeto nuevo)
#         # Usamos get_or_create para buscarlo o crearlo.
#         # Asumimos que el modelo tiene un campo 'nombre' para buscar/crear.
#         obj, created = self.queryset.model.objects.get_or_create(id=value)
        
#         # Si se creó, lo imprimimos (útil para depurar)
#         return obj


# class ProductoForm(forms.ModelForm):
#     """
#     Formulario para crear o actualizar instancias de Producto.

#     Campos personalizados:
#         - `codigo`: Campo libre para ingresar un código único.
#         - `marca`, `categoria`, `gondola`, `unidad_medida`: Campos que permiten
#         seleccionar o crear nuevas instancias mediante texto libre.

#     Validaciones:
#         - `clean_codigo()`: Verifica que el código ingresado no esté duplicado
#         en otra instancia de Producto.

#     Meta:
#         `model` (Producto): Modelo asociado.
#         `fields` (list): Campos incluidos en el formulario.
#         `exclude` (list): Campos excluidos del formulario.
#     """

#     codigo = CreateOrGetModelChoiceField(
#         queryset=Codigo.objects.all(),
#         required=True,
#         label="Código",
#         widget=forms.TextInput(attrs={
#             "list": "codigos_list",
#             "id": "id_codigo",
#             "placeholder": "Código…",
#         })
#     )
#     marca = CreateOrGetModelChoiceField(
#         queryset=Marca.objects.all(),
#         required=True,
#         label="Marca",
#         widget=forms.TextInput(attrs={
#             "nombre": "nombre_marca",
#             "list": "marcas_list",
#             "placeholder": "Escribe o elige marca",
#         })
#     )
#     categoria = CreateOrGetModelChoiceField(
#         queryset=Categoria.objects.all(),
#         required=True,
#         label="Categoría",
#         widget=forms.TextInput(attrs={
#             "list": "categorias_list",
#             "placeholder": "Escribe o elige categoría",
#             "nombre": "nombre_categoria"
#         })
#     )
#     gondola = CreateOrGetModelChoiceField(
#         queryset=Gondola.objects.all(),
#         required=True,
#         label="Gondola",
#         widget=forms.TextInput(attrs={
#             "list": "gondolas_list",
#             "placeholder": "Escribe o elige góndola",
#             "nombre": "nombre_gondola"
#         })
#     )
#     unidad_medida = CreateOrGetModelChoiceField(
#         queryset=UnidadMedida.objects.all(),
#         required=True,
#         label="Unidad de Empaque",
#         widget=forms.TextInput(attrs={
#             "list": "unidades_list",
#             "placeholder": "Escribe o elige unidad",
#             "nombre": "nombre_unidad_medida"
#         })
#     )

#     class Meta:
#         model  = Producto
#         fields = [
#             "nombre", "codigo", "marca", "categoria", "gondola",
#             "unidad_medida", "precio_unitario", "descripcion", "stock"
#         ]

#     def clean_codigo(self):
#         val = self.cleaned_data.get("codigo", "")
#         if not val:
#             return None
#         qs = Codigo.objects.filter(codigo=val)
#         if self.instance.pk:
#             qs = qs.exclude(pk=self.instance.codigo_id)
#         if qs.exists():
#             raise forms.ValidationError("Ese código ya está en uso.")
#         return val

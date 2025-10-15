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
        }

        # Diccionario de WIDGETS para añadir atributos HTML (clases, placeholders, etc.)
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
            'gondola': forms.Select(attrs={'class': 'form-select',}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),

            # Para el BooleanField, usamos un Checkbox
            # 'onSale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

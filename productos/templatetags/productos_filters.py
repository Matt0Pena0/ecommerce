from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='product_add_attributes')
def product_add_attributes(field, attrs):
    """
    Añade clases CSS, otros atributos y la clase 'is-invalid' si hay errores.
    Uso: {{ field|add_attributes:"class:form-control|placeholder:." }}
    """
    # Solo aplicamos esto si el objeto tiene el método as_widget (es un campo de formulario)
    if hasattr(field, 'as_widget'):
        final_attrs = {}
        
        # 1. Parsear los atributos pasados (class, placeholder, etc.)
        for pair in attrs.split('|'):
            if ':' in pair:
                key, value = pair.split(':', 1)
                final_attrs[key] = value

        # 2. Copiar los atributos originales del widget que no se sobrescribieron
        for key, value in field.field.widget.attrs.items():
            if key not in final_attrs:
                final_attrs[key] = value

        # 3. MANEJO CLAVE DE ERRORES: Añadir 'is-invalid' si el campo tiene errores
        current_classes = final_attrs.get('class', '')
        
        # Aseguramos que 'form-control' esté presente
        if 'form-control' not in current_classes:
            current_classes += ' form-control'
            
        # Añadimos 'is-invalid' si el campo tiene errores
        # Esto es crucial para que el borde se ponga rojo.
        if field.errors:
            if 'is-invalid' not in current_classes:
                current_classes += ' is-invalid'
                
        final_attrs['class'] = current_classes.strip()

        # 4. Renderizar el campo con los atributos finales
        return field.as_widget(attrs=final_attrs)
        
    return field # Si no es un campo de widget, devuélvelo sin cambios

@register.filter
def get_label(options, selected_key):
    """Busca 'label' en una lista de diccionarios con clave 'key'."""
    for opt in options:
        if str(opt.get('key')) == str(selected_key):
            return opt.get('label')
    return ''

@register.filter
def get_nombre(queryset, selected_id):
    """Busca 'nombre' en un queryset o lista de objetos con id."""
    for obj in queryset:
        if str(obj.id) == str(selected_id):
            return getattr(obj, 'nombre', '')
    return ''

@register.filter
def get_stock_label(value):
    """Convierte el valor de stock a un texto amigable."""
    mapping = {
        'available': 'Con stock',
        'out': 'Sin stock',
        '': '--Stock--',
        None: '--Stock--'
    }
    return mapping.get(value, '--Stock--')

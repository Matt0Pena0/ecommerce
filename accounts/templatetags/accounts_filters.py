from django import template


register = template.Library()

@register.filter(name='add_attributes')
def add_attributes(field, attrs):
    """
    Añade clases CSS, otros atributos y la clase 'is-invalid' si hay errores.
    Uso: {{ field|add_attributes:"class:form-control|placeholder:." }}
    """
    if hasattr(field, 'as_widget'):
        final_attrs = {}

        # Parsear los atributos pasados (class, placeholder, etc.)
        for pair in attrs.split('|'):
            if ':' in pair:
                key, value = pair.split(':', 1)
                final_attrs[key] = value

        # Copiar los atributos originales del widget que no se sobrescribieron
        for key, value in field.field.widget.attrs.items():
            if key not in final_attrs:
                final_attrs[key] = value

        # Manejo de errores: Añadir 'is-invalid' y 'form-control' si es necesario
        current_classes = final_attrs.get('class', '')

        # Asegurar que 'form-control' esté presente
        if 'form-control' not in current_classes:
            current_classes += ' form-control'

        # Añadimos 'is-invalid' si el campo tiene errores
        if field.errors:
            if 'is-invalid' not in current_classes:
                current_classes += ' is-invalid'

        final_attrs['class'] = current_classes.strip()

        # Renderizar el campo con los atributos finales
        return field.as_widget(attrs=final_attrs)

    return field

from django import template


register = template.Library()

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

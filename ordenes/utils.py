from ordenes.models import Pedido

def format_orden(orden: Pedido) -> list[str]:
    """
    Devuelve una lista de strings, uno por cada ItemPedido de `orden`,
    con el formato:
        "{codigo} | {unidades} | {unidad_medida} | {nombre} {marca} {descripcion}"
    """
    lines = []
    for item in orden.items.all():
        prod = item.producto
        codigo        = str(prod.codigo)  # __str__ de Codigo
        unidades      = item.cantidad
        unidad_medida = prod.unidad_medida.nombre if prod.unidad_medida else ""
        nombre        = prod.nombre
        marca         = prod.marca.nombre if prod.marca else ""
        descripcion   = prod.descripcion or ""
        # Concatenamos sólo los fragmentos que tengan contenido
        parts = [codigo, unidades, unidad_medida, nombre]
        if marca:
            parts.append(marca)
        if descripcion:
            parts.append(descripcion)
        line = " | ".join(str(p) for p in parts)
        lines.append(line)
    return lines

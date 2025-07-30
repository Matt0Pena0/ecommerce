def formatear_producto(product, cantidad_pedida):
    """
    Retorna una cadena formateada según la plantilla:
    "{cantidad_pedida} {unidad} de {nombre} {marca} {descripcion}".
    
    La función omite campos vacíos para que la cadena final quede limpia.
    """
    # Se formatea el inicio con la cantidad y la unidad
    partes = [str(cantidad_pedida), product.get("unidad", "").strip(), "de", product.get("nombre", "").strip()]
    
    # Agregar marca solo si existe y no es vacía
    marca = product.get("marca", "").strip()
    if marca:
        partes.append(marca)
    
    # Agregar descripción solo si existe y no es vacía
    descripcion = product.get("descripcion", "").strip()
    if descripcion:
        partes.append(descripcion)
    
    # Se filtran partes vacías y se unen con un espacio
    return " ".join([parte for parte in partes if parte])

# Ejemplo de uso:
producto_ejemplo = {
    "nombre": "Pan lactal",
    "unidad": "unidad",
    "marca": "Bimbo",
    "descripcion": "de semillas"
}

cadena_producto = formatear_producto(producto_ejemplo, 1)
print(cadena_producto)
# Salida esperada: "1 unidad de Pan lactal Bimbo de semillas"

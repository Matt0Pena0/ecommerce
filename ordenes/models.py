from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from decimal import Decimal

from productos.models import Producto


class EstadoOrden(models.Model):
    # PENDIENTE  = "pendiente"
    # EN_REPARTO = "en_reparto"
    # COMPLETADO = "completado"

    ESTADOS = [
        ("pendiente",  "Pendiente"),
        ("en_reparto", "En reparto"),
        ("completado", "Completado"),
    ]

    nombre = models.CharField(
        max_length=30,
        unique=True,
        choices=ESTADOS,
        default="pendiente",
    )

    def __str__(self):
        return self.get_nombre_display()


User = get_user_model()

class Orden(models.Model):
    """
    Representa una orden de compra realizada por un usuario.

    Cada orden contiene múltiples ítems de :model: Producto  
    Tiene un estado asociado (pendiente, en_reparto, completado). (Aún no implementado)
    El total se calcula dinámicamente a partir de los ítems relacionados.

    :fields:  
        - solicitante (ForeignKey): Usuario que realizó la orden.  
        - creado (DateTimeField): Fecha de creación de la orden.  
        - estado (ForeignKey): Estado actual de la orden (comentado en este ejemplo).  

    :methods:  
        - total(): Calcula el total de la orden sumando los subtotales de cada ítem.  
        - __str__(): Representación legible de la orden.  
    """
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordenes")
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(EstadoOrden, max_length=20, default="pendiente")

    def total(self):
        """
        Calcula el total de la orden.  

        :return: Suma de los subtotales de todos los ítems.  
        :rtype: Decimal  
        """
        return sum(Decimal(item.subtotal()) for item in self.items.all())

    def __str__(self):
        return f"Orden #{self.id} ({self.estado}) – {self.solicitante.username}"


class ItemOrden(models.Model):
    """
    Representa un ítem dentro de una orden.

    Al momento de creación, los datos del producto se congelan para preservar el estado
    del producto en el momento de la compra, incluso si luego se modifican.

    :fields:  
        - orden (ForeignKey): Orden de compra a la que pertenece el ítem.  
        - producto (ForeignKey): Producto seleccionado.  
        - cantidad (PositiveIntegerField): Cantidad solicitada.  
        - nombre_producto, precio_unitario, unidad, marca, categoria, gondola, descripcion:  
        Campos congelados que reflejan el estado del producto al momento de la orden.  

    :methods:  
        - subtotal(): Calcula el subtotal del ítem.  
        - save(): Congela los datos del producto al crear el ítem.  
        - __str__(): Representación legible del ítem.  
    """
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    # Campos congelados
    nombre_producto = models.CharField(max_length=150, default="")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    unidad = models.CharField(max_length=50, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    gondola = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """
        Congela los datos del producto al momento de crear el ítem.

        Esto asegura que los cambios posteriores en el producto no afecten el historial de la orden.
        """
        if self._state.adding:
            p = self.producto
            self.nombre_producto = p.nombre
            self.precio_unitario = p.precio_unitario
            self.unidad = p.unidad_medida.nombre if p.unidad_medida else ""
            self.marca = p.marca.nombre if p.marca else ""
            self.categoria = p.categoria.nombre if p.categoria else ""
            self.gondola = p.gondola.nombre if p.gondola else ""
            self.descripcion = p.descripcion or ""
        super().save(*args, **kwargs)

    def subtotal(self):
        """
        Calcula el subtotal del ítem.

        :return: Precio unitario multiplicado por la cantidad.
        :rtype: Decimal
        """
        return Decimal(self.precio_unitario * self.cantidad)

    def __str__(self):
        return f"{self.cantidad} x {self.nombre_producto} en orden #{self.orden.id}"

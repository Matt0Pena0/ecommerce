from django.db import models
from django.contrib.auth import get_user_model

from productos.models import Producto


User = get_user_model()


class Carrito(models.Model):
    """
    Modelo que representa el carrito de compras de un usuario.

    Cada usuario tiene un único carrito asociado. El carrito contiene múltiples ítems
    y calcula el total dinámicamente.

    :fields:
        - `usuario` (OneToOneField): Relación uno a uno con el modelo de usuario.
        - `creado` (DateTimeField): Fecha de creación del carrito.

    :methods:
        - `total()`: Calcula el total del carrito sumando los subtotales de cada ítem.
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carrito")
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        """
        Calcula el total del carrito.

        :return: Suma de los subtotales de todos los ítems en el carrito.
        :rtype: float
        """
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Orden #{self.id} ({self.creado}) – {self.usuario.username}"


class ItemCarrito(models.Model):
    """
    Modelo que representa un ítem dentro del carrito.

    Cada ítem está asociado a un producto y a un carrito. La combinación de carrito y producto
    debe ser única para evitar duplicados.

    :fields:
        - `carrito` (ForeignKey): Relación con el modelo Carrito.
        - `producto` (ForeignKey): Relación con el modelo Producto.
        - `cantidad` (PositiveIntegerField): Cantidad del producto en el carrito.

    :meta:
        - `unique_together`: Garantiza que no haya duplicados de producto en un mismo carrito.

    :methods:
        - `subtotal()`: Calcula el subtotal del ítem (precio * cantidad).
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = ("carrito", "producto")

    def subtotal(self):
        """
        Calcula el subtotal del ítem.

        :return: Precio unitario del producto multiplicado por la cantidad.
        :rtype: float
        """
        return self.producto.precio_unitario * self.cantidad
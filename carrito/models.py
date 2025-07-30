from django.db import models
from django.contrib.auth import get_user_model

from productos.models import Producto


User = get_user_model()


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carrito")
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Orden #{self.id} ({self.creado}) – {self.usuario.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = ("carrito", "producto")

    def subtotal(self):
        return self.producto.precio_unitario * self.cantidad
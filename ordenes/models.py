from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from productos.models import Producto


# class EstadoOrden(models.Model):
#     # PENDIENTE  = "pendiente"
#     # EN_REPARTO = "en_reparto"
#     # COMPLETADO = "completado"

#     ESTADOS = [
#         ("pendiente",  "Pendiente"),
#         ("en_reparto", "En reparto"),
#         ("completado", "Completado"),
#     ]

#     nombre = models.CharField(
#         max_length=30,
#         unique=True,
#         choices=ESTADOS,
#         default="pendiente",
#     )

#     def __str__(self):
#         return self.get_nombre_display()
# ESTADOS = [
#     ("pendiente",  "Pendiente"),
#     ("en_reparto", "En reparto"),
#     ("completado", "Completado"),
# ]


User = get_user_model()

class Orden(models.Model):
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordenes")
    creado = models.DateTimeField(auto_now_add=True)
    # actualizado = models.DateTimeField(auto_now=True)
    # estado = models.ForeignKey("EstadoOrden", on_delete=models.PROTECT)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    # def save(self, *args, **kwargs):
    #     # Si es nuevo y no indicaron un estado, asignamos "pendiente"
    #     if self._state.adding and not self.estado_id:
    #         self.estado = EstadoOrden.objects.get(nombre=EstadoOrden.PENDIENTE)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden #{self.id} ({self.estado}) – {self.solicitante.username}"


class ItemOrden(models.Model):
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
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.nombre_producto} en orden #{self.orden.id}"

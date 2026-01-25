from django.db import models


class Codigo(models.Model):
    """
    Representa un código único asociado a un producto.

    Si no se define explícitamente, se asigna automáticamente el valor del `pk` como código.

    Sirve con el objetivo de asignar o migrar codigos de sistemas ya existentes
    """
    codigo = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        # Primera pasada: guarda para obtener self.pk
        super().save(*args, **kwargs)

        # Si es nuevo y aún no se definio un código, le asigna = pk
        if is_new and not self.codigo:
            # Usa el pk numérico como código, convertido a string
            self.codigo = str(self.pk)
            # Actualiza sólo este campo
            super().save(update_fields=["codigo"])

    def __str__(self):
        return self.codigo


class Marca(models.Model):
    """
    Marca comercial del producto.
    """
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    """
    Categoría a la que pertenece el producto.
    """
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre


class Gondola(models.Model):
    """
    Ubicación física o lógica del producto dentro del sistema de inventario.
    """
    nombre = models.CharField(max_length=50, unique=True, blank=True)
    
    def __str__(self):
        return self.nombre or "Sin góndola"


class UnidadMedida(models.Model):
    """
    Unidad de medida utilizada para el producto (ej. kg, litro, unidad).
    """
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Modelo principal que representa un producto en el sistema.

    Incluye información como nombre, marca, categoría, ubicación, unidad de medida,
    precio, descripción y stock disponible.
    """
    id = models.BigAutoField(primary_key=True)
    codigo = models.OneToOneField(Codigo, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    gondola = models.ForeignKey(Gondola, on_delete=models.SET_NULL, null=True, blank=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=20, decimal_places=2)
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    img = models.ImageField(upload_to='productos/', default='productos/producto.png', null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.nombre}"
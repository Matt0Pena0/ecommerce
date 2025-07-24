from django.db import models


class Codigo(models.Model):
    codigo = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        # Primera pasada: guardamos para obtener self.pk
        super().save(*args, **kwargs)

        # Si es nuevo y aún no definieron un código, lo asignamos = pk
        if is_new and not self.codigo:
            # Usamos el pk numérico como código, convertido a string
            self.codigo = str(self.pk)
            # Actualizamos sólo ese campo para no reinvocar recursivamente save()
            super().save(update_fields=["codigo"])

    def __str__(self):
        return self.codigo


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre


class Gondola(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=True)
    
    def __str__(self):
        return self.nombre or "Sin góndola"


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.OneToOneField(Codigo, on_delete=models.CASCADE, primary_key=True, blank=True)    
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    gondola = models.ForeignKey(Gondola, on_delete=models.SET_NULL, null=True, blank=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=20, decimal_places=2)
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
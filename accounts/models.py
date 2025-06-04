from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models


class RolesBase(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class UsuarioBase(AbstractUser):
    rol = models.ForeignKey(RolesBase, on_delete=models.SET_NULL, null=True, blank=True)
from django.db import models
from django.contrib.auth.models import AbstractUser


class UsuarioBase(AbstractUser):
    direccion = models.CharField(max_length=150, blank=True)

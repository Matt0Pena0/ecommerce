from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for nombre in ['admin', 'cliente']:
        Group.objects.get_or_create(name=nombre)


User = get_user_model()

@receiver(post_save, sender=User)
def asignar_cliente_por_defecto(sender, instance, created, **kwargs):
    if created:
        grupo_cliente, _ = Group.objects.get_or_create(name='cliente')
        instance.groups.add(grupo_cliente)

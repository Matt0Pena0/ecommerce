from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()

@transaction.atomic
def crear_usuario_service(**validated_data):
    """
    Crea un nuevo usuario asegurando reglas de negocio:
    - username y email únicos
    - posibilidad de disparar auditoría/signals
    """

    if User.objects.filter(username=validated_data["username"]).exists():
        raise ValueError("El username ya existe")

    if User.objects.filter(email=validated_data["email"]).exists():
        raise ValueError("El email ya está en uso")

    user = User.objects.create_user(
        username=validated_data["username"],
        first_name=validated_data["first_name"],
        last_name=validated_data["last_name"],
        email=validated_data["email"],
        direccion=validated_data["direccion"],
        password=validated_data["password1"],
    )

    return user

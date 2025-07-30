from django.urls import path

from carrito.views import agregar_al_carrito, finalizar_carrito, ver_carrito, eliminar_item_carrito, actualizar_carrito


app_name = "carrito"

urlpatterns = [
    path("ver_carrito/", ver_carrito, name="ver_carrito"),
    path("actualizar/", actualizar_carrito, name="actualizar"),
    path("agregar/<int:producto_codigo>", agregar_al_carrito, name="agregar_al_carrito"),
    path("eliminar/<int:producto_codigo>", eliminar_item_carrito, name="eliminar"),
    path("finalizar/", finalizar_carrito, name="finalizar"),
]
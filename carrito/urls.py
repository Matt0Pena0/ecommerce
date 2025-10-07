from django.urls import path

from carrito.views import ( finalizar_carrito, ver_carrito,
                            eliminar_item_carrito, 
                            agregar_item_carrito_api,
                            eliminar_item_carrito_api,
                            actualizar_carrito)


app_name = "carrito"

urlpatterns = [
    path("ver_carrito/", ver_carrito, name="ver_carrito"),
    path('api/agregar/', agregar_item_carrito_api, name='agregar_item_carrito_api'),
    path('api/eliminar/', eliminar_item_carrito_api, name='eliminar_item_carrito_api'),
    path("actualizar/", actualizar_carrito, name="actualizar"),
    path("eliminar/<int:producto_codigo>", eliminar_item_carrito, name="eliminar"),
    path("finalizar/", finalizar_carrito, name="finalizar"),
]

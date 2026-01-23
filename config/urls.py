from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from productos.api import ProductoViewSet
from carrito.api import CarritoViewSet


router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto-api')
router.register(r'carrito', CarritoViewSet, basename='carrito-api')

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include(router.urls)),

    path("accounts/", include("accounts.urls.urls_base", namespace="accounts")),
    path("productos/", include("productos.urls", namespace="productos")),
    path("carrito/", include("carrito.urls", namespace="carrito")),
    path("ordenes/", include("ordenes.urls", namespace="ordenes")),
    path("", include("core.urls", namespace="core")),

    path("admin/doc/", include('django.contrib.admindocs.urls')),
    path("grappelli/", include("grappelli.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

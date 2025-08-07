from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("productos/", include("productos.urls", namespace="productos")),
    path("ordenes/", include("ordenes.urls", namespace="ordenes")),
    path("carrito/", include("carrito.urls", namespace="carrito")),
    path("accounts/", include("accounts.urls.urls_base", namespace="accounts")),
    path("admin/doc/", include('django.contrib.admindocs.urls')),
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

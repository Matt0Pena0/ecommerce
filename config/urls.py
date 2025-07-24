from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("productos/", include("productos.urls", namespace="productos")),
    path("accounts/", include("accounts.urls.urls_base", namespace="accounts")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("grappelli/", include("grappelli.urls")),
    ]

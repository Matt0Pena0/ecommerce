from django.contrib import admin
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('grappelli/', include('grappelli.urls')),    
    ]
from .base import *


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    'debug_toolbar',
    'grappelli',
    'django_extensions',
] + INSTALLED_APPS 

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] 

INTERNAL_IPS = ['127.0.0.1']
# Detectar automáticamente IP del host desde contenedor Docker
import socket

try:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:ip.rfind('.')] + '.1' for ip in ips]
except:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
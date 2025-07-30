from decouple import config

from .base import *

ALLOWED_HOSTS = ["https://b95d1a609661.ngrok-free.app", '.ngrok-free.app',"localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = [
    "https://b95d1a609661.ngrok-free.app",
]
INSTALLED_APPS = [
    "debug_toolbar",
    "grappelli",
    "django_extensions",
] + INSTALLED_APPS

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]
# Detectar automáticamente IP del host desde contenedor Docker
import socket

try:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[: ip.rfind(".")] + ".1" for ip in ips]
except:
    pass

import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME":     os.getenv("DB_NAME"),          # Nombre de la base de datos
        "USER":     os.getenv("DB_USER"),          # Usuario creado para la base de datos
        "PASSWORD": os.getenv("DB_PASS"),          # Contraseña del usuario
        "HOST":     os.getenv("DB_HOST"),          # Dirección IP del host (localhost o la  IP de tu máquina)
        'PORT': '3306',                            # Puerto por defecto de MySQL
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_HOST = config("EMAIL_HOST")
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
# EMAIL_TO = config("EMAIL_TO")
# EMAIL_PORT = config("EMAIL_PORT")
# EMAIL_USE_TLS = config("EMAIL_USE_TLS")
# EMAIL_USE_SSL = config("EMAIL_USE_SSL")

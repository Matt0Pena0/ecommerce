from decouple import config

from .base import *

ALLOWED_HOSTS = ["https://da0a92a2e15b.ngrok-free.app", '.ngrok-free.app',"localhost", "127.0.0.1", "0.0.0.0"]

CSRF_TRUSTED_ORIGINS = [
    "https://da0a92a2e15b.ngrok-free.app",
]

INSTALLED_APPS = [
    "debug_toolbar",
    "django.contrib.admindocs",
] + INSTALLED_APPS

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
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
        "NAME":     config("DB_NAME"),          # Nombre de la base de datos
        "USER":     config("DB_USER"),          # Usuario creado para la base de datos
        "PASSWORD": config("DB_PASS"),          # Contraseña del usuario
        "HOST":     config("DB_HOST"),          # Dirección IP del host (localhost o la  IP de la máquina)
        'PORT': '3306',                         # Puerto por defecto de MySQL
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

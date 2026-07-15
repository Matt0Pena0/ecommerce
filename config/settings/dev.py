from decouple import config

from .base import *

ALLOWED_HOSTS = ["https://c1d2-2800-a4-1f04-4100-ba0d-b70-5e86-47b4.ngrok-free.app", '.ngrok-free.app',"localhost", "127.0.0.1", "0.0.0.0"]

CSRF_TRUSTED_ORIGINS = [
    "https://c1d2-2800-a4-1f04-4100-ba0d-b70-5e86-47b4.ngrok-free.app",
]
INSTALLED_APPS = [
    # "debug_toolbar",
    "django.contrib.admindocs",
] + INSTALLED_APPS

MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
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
        "NAME":     config("DB_NAME"),
        "USER":     config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST":     config("DB_HOST"),
        'PORT': '3306',
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

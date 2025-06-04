from .base import *


# INSTALLED_APPS += [

# ]

DEBUG = config('DEBUG', cast=bool)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME":     config("DB_NAME"),          # Nombre de la base de datos
        "USER":     config("DB_USER"),          # Usuario creado para la base de datos
        "PASSWORD": config("DB_PASS"),          # Contraseña del usuario
        "HOST":     config("DB_HOST"),          # Dirección IP del host (localhost o la  IP de tu máquina)
        'PORT': '3306',                      # Puerto por defecto de MySQL
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

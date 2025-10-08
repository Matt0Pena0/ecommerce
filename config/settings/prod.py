from decouple import config

from .base import *


DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = ['ecommerce.themattdev.com', 'www.ecommerce.themattdev.com', '200.45.208.202', '127.0.0.1']

# INSTALLED_APPS += []

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    'https://www.ecommerce.themattdev.com',
    'https://ecommerce.themattdev.com'
]

# EMAIL_HOST = config("EMAIL_HOST")
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
# EMAIL_TO = config("EMAIL_TO")
# EMAIL_PORT = config("EMAIL_PORT")
# EMAIL_USE_TLS = config("EMAIL_USE_TLS")
# EMAIL_USE_SSL = config("EMAIL_USE_SSL")

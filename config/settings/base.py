from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool, default=True)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps externas comunes
    "import_export",
    "core",
    "accounts",
    "productos",
    "ordenes",
    "carrito",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Modelo de usuario personalizado
AUTH_USER_MODEL = "accounts.UsuarioBase"

# Urls de sesión
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "accounts:login"

# Base de datos vacía, se define en cada entorno
DATABASES = {}

# Static files
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "node_modules/bootstrap-icons/font/",
]
STATIC_ROOT = str(BASE_DIR / "staticfiles")

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "mediafiles")

LANGUAGE_CODE = "es-UY"
TIME_ZONE = "America/Montevideo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

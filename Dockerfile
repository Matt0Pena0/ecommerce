# 1. Base
FROM python:3.12-slim

# Evitar archivos .pyc y buffered IO
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema para mysqlclient
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- Optimización del Caché ----
# Copiar solo los archivos de requeriments
COPY requirements/ app/requirements/

# Instalar los requeriments de producción
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copiar código de la aplicación
COPY . /app/

# Exponer puerto Django
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

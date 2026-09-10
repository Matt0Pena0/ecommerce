#!/bin/sh
# ==============================================================================
# Entrypoint de producción — Ecommerce
# ==============================================================================
# Espera a que la base de datos esté disponible, aplica migraciones,
# recopila archivos estáticos y arranca Gunicorn.
#
# La carga inicial de datos (data/backup.json) NO se ejecuta aquí; es un paso
# manual documentado en .infra/OPERATIONS.md:
#   docker compose exec web python manage.py loaddata data/backup.json
# ==============================================================================
set -e

: "${DB_HOST:=db}"
: "${DB_PORT:=3306}"
: "${GUNICORN_WORKERS:=3}"

echo "[entrypoint] Esperando a la base de datos en ${DB_HOST}:${DB_PORT}..."
# Espera activa hasta que MySQL acepte conexiones (máx ~60s)
i=0
until mysqladmin ping -h "${DB_HOST}" -P "${DB_PORT}" --silent >/dev/null 2>&1; do
    i=$((i + 1))
    if [ "$i" -ge 30 ]; then
        echo "[entrypoint] ERROR: la base de datos no respondió tras 60s." >&2
        exit 1
    fi
    sleep 2
done
echo "[entrypoint] Base de datos disponible."

echo "[entrypoint] Aplicando migraciones..."
python manage.py migrate --noinput

echo "[entrypoint] Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "[entrypoint] Arrancando Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS}" \
    --log-level info \
    --access-logfile - \
    --error-logfile -

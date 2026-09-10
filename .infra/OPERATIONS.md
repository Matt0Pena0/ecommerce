# Operaciones Comunes — Infraestructura Docker

> Comandos operativos de referencia para gestionar proyectos desplegados
> con esta arquitectura. Todos los comandos se ejecutan desde el directorio
> del proyecto: `/opt/ecommerce/`

---

## 1. Despliegue

### Deploy (vía GitHub Actions — recomendado)

El despliegue normal es automático con cada `push` a `main`. Para lanzarlo a mano:
`Actions → Deploy → Run workflow`. El VPS no construye imágenes.

### Deploy manual desde el VPS (excepcional)

Requiere estar autenticado en GHCR (`docker login ghcr.io`):

```bash
cd /opt/ecommerce
git pull origin main          # actualiza compose, nginx.conf, fixtures
docker compose pull web       # baja la imagen publicada
docker compose up -d
```

### Deploy sin rebuild (solo reinicio)

```bash
cd /opt/ecommerce
docker compose restart
```

---

## 2. Logs

### Ver logs de un servicio específico

```bash
docker compose logs -f nginx
docker compose logs -f backend --tail=100
docker compose logs -f db --since=1h
```

### Ver logs de todos los servicios

```bash
docker compose logs -f --tail=50
```

---

## 3. Backups

### Base de datos

```bash
# Exportar
docker compose exec db mysqldump -u $$MYSQL_USER -p$$MYSQL_PASSWORD $$MYSQL_DATABASE > backup_$(date +%F).sql

# Importar
docker compose exec -T db mysql -u $$MYSQL_USER -p$$MYSQL_PASSWORD $$MYSQL_DATABASE < backup_2025-01-15.sql
```

### Volúmenes completos

```bash
tar -czf /opt/backups/ecommerce_$(date +%F).tar.gz \
    /opt/ecommerce/data/
```

---

## 4. Gestión de Servicios

### Reiniciar un servicio

```bash
docker compose restart backend
docker compose restart nginx
```

### Actualizar un servicio a la última imagen

```bash
docker compose pull web && docker compose up -d web
```

### Volver a una versión anterior (rollback)

```bash
WEB_TAG=sha-a1b2c3d docker compose up -d web
```

### Detener todo el proyecto

```bash
docker compose down
```

### Detener y eliminar volúmenes (destructivo)

```bash
docker compose down -v   # PRECAUCIÓN: elimina datos persistentes
```

---

## 5. Acceso a Contenedores

### Shell interactivo

```bash
docker compose exec backend python manage.py shell
docker compose exec frontend sh
```

### Consola de base de datos

```bash
docker compose exec db mysql -u $$MYSQL_USER -p$$MYSQL_PASSWORD $$MYSQL_DATABASE
```

### Consola de cache

```bash
docker compose exec cache redis-cli -a $$REDIS_PASSWORD
```

---

## 6. Monitoreo

### Estado de servicios

```bash
docker compose ps
```

### Uso de recursos

```bash
docker stats --no-stream
```

### Verificar healthchecks

```bash
docker compose ps
# Ver estado detallado de healthcheck de un contenedor específico:
docker inspect ecommerce-nginx | grep -A 10 '"Health"'
```

---

## 7. Mantenimiento

### Actualizar imágenes base

```bash
docker compose pull
docker compose up -d
```

### Limpiar recursos no utilizados

```bash
# Imágenes huérfanas
docker image prune -f

# Volúmenes no referenciados
docker volume prune -f

# Limpieza completa (contenedores parados + imágenes sin usar)
docker system prune -f
```

---

## 8. Gateway Central

### Reiniciar el gateway

```bash
cd /opt/proxy
docker compose restart
```

### Ver logs del gateway

```bash
cd /opt/proxy
docker compose logs -f proxy --tail=50
```

### Verificar conectividad entre gateway y proyecto

```bash
docker network inspect proxy-network | grep ecommerce-nginx
```

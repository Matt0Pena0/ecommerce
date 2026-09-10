# Checklist de Migración — Proyecto Existente a Infraestructura Docker

> Guía paso a paso para migrar un proyecto existente (desplegado manualmente o con
> otra arquitectura) a la infraestructura estandarizada de este framework.

---

## Antes (Ejemplo Genérico)

```
Servidor (despliegue manual)
├── Configuración web manual (nginx/apache)   ← Config manual
├── /var/www/ecommerce/                  ← Archivos del proyecto
└── Certificados SSL (certbot o manual)
```

## Después (Dockerizado)

```
/opt/ecommerce/
├── docker-compose.yml          ← Orquestación (desde plantilla)
├── nginx/nginx.conf            ← Reverse proxy interno
├── backend/                    ← Código + Dockerfile
├── frontend/                   ← Código + Dockerfile
├── data/                       ← Volúmenes persistentes
└── .env.prod                   ← Variables de entorno
```

---

## Pasos de Migración

### 1. Crear Estructura

```bash
mkdir -p /opt/ecommerce/{nginx,data,backend,frontend}
```

### 2. Mover Código Fuente

```bash
cp -r /var/www/ecommerce/backend /opt/ecommerce/backend
cp -r /var/www/ecommerce/frontend /opt/ecommerce/frontend
```

### 3. Crear docker-compose.yml

Usar la plantilla `docker-compose.template.yml` de este directorio, adaptando:
- Imagen de base de datos según el motor del proyecto
- Servicios no necesarios (eliminar cache si no aplica, etc.)
- Puertos internos según el framework del backend

### 4. Adaptar Nginx

Convertir la configuración nativa a `nginx/nginx.conf` interno:
- Quitar directivas `listen 443` y `ssl_certificate` (SSL lo maneja el gateway)
- Cambiar `proxy_pass` a nombres de servicio Docker (`backend`, `frontend`)
- Quitar `server_name` específico (el gateway lo resuelve)

### 5. Crear .env.prod

Usar `env.template` como base y completar con las credenciales del proyecto.

### 6. Migrar Base de Datos

```bash
# Exportar datos del origen
mysqldump -u root -p$$MYSQL_ROOT_PASSWORD $$MYSQL_DATABASE > dump.sql

# Levantar contenedor de DB
docker compose up -d db

# Importar datos
mysql -u root -p$$MYSQL_ROOT_PASSWORD $$MYSQL_DATABASE < dump.sql
```

### 7. Levantar Servicios

```bash
cd /opt/ecommerce && docker compose up -d
```

### 8. Configurar Gateway

En el panel del Nginx Proxy Manager, crear un Proxy Host:

| Campo | Valor |
|-------|-------|
| Domain | `ecommerce.themattdev.com` |
| Forward Host | `ecommerce-nginx` |
| Forward Port | `80` |
| SSL | Certificado automático |

---

## Checklist de Validación

- [ ] Base de datos migrada a contenedor (datos importados y verificados)
- [ ] Variables de entorno en `.env.prod` (nunca en el repositorio)
- [ ] Volúmenes de datos en `./data/` (backups accesibles)
- [ ] Nginx interno escucha en puerto 80 (SSL lo maneja el gateway)
- [ ] `container_name` del nginx coincide con Forward Host en el gateway
- [ ] Contenedor nginx conectado a `proxy-network`
- [ ] Puertos de DB/Cache NO expuestos al host
- [ ] Acceso verificado via subdominio con HTTPS
- [ ] Healthchecks pasando para todos los servicios críticos
- [ ] Logs accesibles via `docker compose logs`
- [ ] Backup de datos funcional y documentado

# FEAT-007 — Integración de Infraestructura VPS + CI/CD

**Feature ID**: FEAT-007
**Componente**: DevOps / Infraestructura
**Estado**: SPEC_APPROVED
**Depende de**: FEAT-006 (Dockerización base)

---

## Objetivo

Adaptar la infraestructura del proyecto **Ecommerce** —hoy desplegado manualmente vía
`git clone` + Nginx del host en el VPS— a la arquitectura estandarizada definida en `.infra/`:

1. **Nginx interno por proyecto** conectado a la red compartida `proxy-network`, de modo que el
   gateway central (Nginx Proxy Manager) rutee por subdominio y gestione SSL.
2. **Cero puertos publicados al host** por los servicios internos (db, web). El único punto
   de contacto es el contenedor nginx interno a través de `proxy-network`.
3. **Arranque autónomo y reproducible**: el servicio web ejecuta `migrate` + `collectstatic`
   automáticamente antes de levantar Gunicorn.
4. **CI/CD con GitHub Actions**: pipeline de integración (checks + build) y despliegue continuo
   al VPS por SSH sobre la rama `main`.
5. **Corrección de bugs de infraestructura** detectados en la exploración (módulo WSGI incorrecto,
   `DJANGO_SETTINGS_MODULE` frágil).

### Fuera de alcance (Non-Goals)

- No se modifica lógica de negocio de las apps Django (`accounts/`, `productos/`, etc.).
- No se configura el gateway central en sí (Nginx Proxy Manager ya existe en el VPS; solo se
  documenta el Proxy Host a crear).
- No se introduce Redis/cache (queda como feature futura).

---

## Arquitectura Objetivo

```
Internet (443)
    │
    ▼
┌─────────────────────────────────────────┐
│  Nginx Proxy Manager (gateway central)  │  ← ya existe en el VPS
│  SSL Let's Encrypt + routing            │
│  Red: proxy-network                         │
└─────────────────────────────────────────┘
    │  Forward Host: ecommerce-nginx : 80
    ▼
┌─────────────────────────────────────────┐   /opt/ecommerce/
│  ecommerce-nginx  (proxy-network + internal)│
│  - / y /api/  → web:8000                │
│  - /static/   → volumen static          │
│  - /media/    → volumen media           │
└─────────────────────────────────────────┘
    │ internal
    ▼
┌──────────────────┐   ┌──────────────────┐
│ ecommerce-web    │   │ ecommerce-db      │
│ gunicorn :8000   │──▶│ mysql:8.0 :3306   │
│ (sin puerto host)│   │ (sin puerto host) │
└──────────────────┘   └──────────────────┘
```

---

## Contratos de Infraestructura

### Servicios Docker Compose (producción)

| Servicio | Imagen / Build | Redes | Puertos al host | Notas |
|----------|----------------|-------|-----------------|-------|
| `db` | `mysql:8.0` | `internal` | Ninguno | Volumen persistente en `./data/mysql`, healthcheck |
| `web` | Build local (Dockerfile) | `internal` | Ninguno | Gunicorn en `:8000`, entrypoint con migrate + collectstatic |
| `nginx` | `nginx:alpine` | `internal`, `proxy-network` | Ninguno (expose 80) | `container_name: ecommerce-nginx`, sirve static/media y proxy a web |

### Contrato de Ruteo del Gateway (a configurar en NPM)

| Campo | Valor |
|-------|-------|
| Domain | `ecommerce.themattdev.com` |
| Forward Host | `ecommerce-nginx` |
| Forward Port | `80` |
| SSL | Certificado automático (Let's Encrypt) |
| Websockets | No requerido |

### Contrato del Pipeline CI/CD (GitHub Actions)

| Workflow | Trigger | Jobs | Resultado |
|----------|---------|------|-----------|
| `ci.yml` | `push` / `pull_request` a `main` | `checks` (django check + migraciones + tests si existen), `build` (docker build sin push) | Bloquea merge si falla |
| `deploy.yml` | `push` a `main` (o `workflow_dispatch`) | `deploy` (SSH al VPS → `git pull` → `docker compose up --build -d` → `migrate`) | Despliegue en el VPS |

### Secrets de GitHub requeridos

| Secret | Descripción |
|--------|-------------|
| `VPS_HOST` | IP o host del VPS |
| `VPS_USER` | Usuario SSH de despliegue |
| `VPS_SSH_KEY` | Clave privada SSH (deploy key) |
| `VPS_PROJECT_PATH` | Ruta del proyecto en el VPS (`/opt/ecommerce`) |

> **Repositorio**: `github.com/Matt0Pena0/ecommerce` — rama de despliegue `main`.
> **Red del gateway**: `proxy-network` (externa, estándar de la infra del VPS).

---

## Modelo de Datos

No aplica. Esta feature no introduce cambios de esquema de base de datos.

---

## Criterios de Aceptación (DoD)

- [ ] `docker-compose.yml` de producción define `db`, `web` y `nginx`; ningún servicio publica puertos al host.
- [ ] El contenedor `nginx` (`container_name: ecommerce-nginx`) está conectado a `internal` y `proxy-network` (red externa).
- [ ] Existe `nginx/nginx.conf` interno que rutea `/` y `/api/` a `web:8000` y sirve `/static/` y `/media/` desde volúmenes.
- [ ] El `Dockerfile` de producción arranca con el módulo WSGI correcto (`config.wsgi:application`).
- [ ] El servicio `web` ejecuta `migrate` y `collectstatic --noinput` automáticamente antes de Gunicorn (entrypoint).
- [ ] `wsgi.py`, `asgi.py` y `manage.py` usan un `DJANGO_SETTINGS_MODULE` válido por defecto (`config.settings.prod` / `config.settings.dev` según entorno).
- [ ] Existe `.github/workflows/ci.yml` que corre `python manage.py check`, verifica migraciones y ejecuta tests, y hace `docker build`.
- [ ] Existe `.github/workflows/deploy.yml` que despliega al VPS por SSH usando los secrets definidos.
- [ ] Existe `.env.prod.example` con todas las variables de producción (sin secretos reales).
- [ ] `docker compose -f docker-compose.yml config` valida sin errores.
- [ ] `.dockerignore` excluye `.git`, `.venv`, `node_modules`, `.env*`, y artefactos de build.
- [ ] `project_manifest.md` (Sección 5 y 7) refleja la nueva arquitectura y marca FEAT-007 como `DONE`.

---

## Dependencias

| Dependencia | Estado | Fuente |
|-------------|--------|--------|
| Plantillas `.infra/` | Disponible | `.infra/docker-compose.template.yml`, `.infra/nginx/nginx.template.conf` |
| Gateway central (NPM) + red `proxy-network` | Asumido existente en VPS | Configuración previa del servidor |
| `requirements/prod.txt` con `gunicorn` | A verificar | `requirements/prod.txt` |
| Repositorio GitHub | Disponible | `github.com/MatttttaM/pedidos` |
| Acceso SSH al VPS para deploy | Requiere secrets | GitHub Actions Secrets |

---

## Constraints

- **Cero puertos al host** para `db` y `web`. Regla de oro de `.infra/SECURITY.md`.
- **SSL lo gestiona el gateway**, no el nginx interno (nginx interno escucha solo en `:80`).
- **No versionar secretos**: `.env.prod` vive solo en el VPS; el repo solo tiene `.env.prod.example`.
- **`proxy-network` es red externa**: se asume creada (`docker network create proxy-network`); el compose no la crea.
- **Compatibilidad de datos**: la migración del despliegue actual (git clone) al nuevo esquema
  (`./data/mysql`) debe preservar los datos existentes (documentar en el Action Plan).
- **Ruta de despliegue**: `/opt/ecommerce` en el VPS (estándar `.infra/`).

---

## Contexto Mínimo

Archivos que el agente asignado (@DevOps_Agent) DEBE leer antes de implementar:

- `.infra/docker-compose.template.yml`
- `.infra/nginx/nginx.template.conf`
- `.infra/README.md`
- `.infra/SECURITY.md`
- `.infra/OPERATIONS.md`
- `docker-compose.yml` (actual, a reemplazar)
- `Dockerfile` (a corregir)
- `config/settings/prod.py`
- `config/wsgi.py`, `manage.py`
- `requirements/prod.txt`
- `package.json`

---

## Decisiones Confirmadas (validadas con el usuario)

1. **Gateway central**: el VPS ya corre Nginx Proxy Manager. La red compartida es `proxy-network`
   (nombre estandarizado en todos los proyectos del VPS).
2. **Ruta de despliegue**: `/opt/ecommerce`. El VPS anterior (git clone + nginx del host) está
   apagado; se parte de un despliegue limpio.
3. **Estrategia de deploy**: SSH + `git pull` + `docker compose up --build -d` (estándar de la
   infra; sin registry de imágenes).
4. **Servido de estáticos**: **nginx interno + volumen compartido** con `web` (opción elegida).
   Razón: el proyecto usa `media/` (imágenes de productos vía `ImageField`), que WhiteNoise no
   cubre; como el nginx interno es obligatorio por la arquitectura `proxy-network`, servir
   `static/` y `media/` desde nginx es más performante y coherente que meterlos en Gunicorn.
5. **Base de datos**: MySQL en contenedor con volumen `./data/mysql`. Existe un respaldo en
   `data/backup.json` que se cargará posteriormente vía `manage.py loaddata` (paso documentado
   en OPERATIONS, no automático en el arranque).
6. **Repositorio**: `github.com/Matt0Pena0/ecommerce`.

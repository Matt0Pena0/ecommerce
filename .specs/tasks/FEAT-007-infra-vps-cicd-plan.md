# ACTION PLAN — FEAT-007: Integración de Infraestructura VPS + CI/CD

**Generado por**: @Orchestrator_Agent
**Fecha**: 2026-09-02
**Estado**: APROBADO (auditado por @Architect_Agent)
**Spec de referencia**: `.specs/features/FEAT-007-infra-vps-cicd.spec.md`

---

## Análisis de Dependencias

| Dependencia | Disponible | Fuente |
|-------------|-----------|--------|
| Plantillas `.infra/` | Sí | `.infra/` (ya en el repo, red renombrada a `proxy-network`) |
| Gateway NPM + red `proxy-network` | Sí (en VPS) | Configuración previa del servidor |
| `gunicorn` en `requirements/prod.txt` | A verificar en SUBTAREA 0 | `requirements/prod.txt` |
| Repo GitHub `Matt0Pena0/ecommerce` | Sí | Confirmado por usuario |
| Secrets SSH del VPS | Pendiente (config manual del usuario en GitHub) | GitHub Actions Secrets |

---

## Subtareas y Asignación

### SUBTAREA 0 — Verificar dependencias del backend

**Agente**: @DevOps_Agent
**Archivo**: `requirements/prod.txt` (solo lectura)

Confirmar que `gunicorn` y `mysqlclient` están en `requirements/prod.txt`. Si falta `gunicorn`,
reportarlo (no se agrega sin aprobación, pero es requisito del CMD de producción).

**DoD del paso**:
- [ ] Confirmado `gunicorn` presente (o reportado como faltante)
- [ ] Confirmado `mysqlclient` presente

---

### SUBTAREA 1 — Corregir `DJANGO_SETTINGS_MODULE` por defecto

**Agente**: @Backend_Agent (frontera: `config/`, `manage.py`)
**Archivos**: `config/wsgi.py`, `config/asgi.py`, `manage.py`

Cambiar el default `config.settings` (inexistente) por `config.settings.prod` en `wsgi.py`/`asgi.py`
y `config.settings.dev` en `manage.py`. El entorno real se sigue pudiendo sobreescribir vía env var.

**Acción Exacta**: `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")` en wsgi/asgi;
`config.settings.dev` en manage.py.

**DoD del paso**:
- [ ] `wsgi.py` y `asgi.py` apuntan a `config.settings.prod` por defecto
- [ ] `manage.py` apunta a `config.settings.dev` por defecto
- [ ] `python manage.py check` corre sin error de settings

---

### SUBTAREA 2 — Corregir y endurecer el `Dockerfile` de producción

**Agente**: @DevOps_Agent
**Archivo**: `Dockerfile`, `docker/entrypoint.sh` (nuevo)

Corregir el `CMD` (`themattdev.wsgi` → `config.wsgi:application`). Añadir un entrypoint que ejecute
`migrate --noinput` + `collectstatic --noinput` antes de arrancar Gunicorn. Crear usuario no-root.

**Acción Exacta**:
- Reemplazar `CMD` por un `ENTRYPOINT ["/app/docker/entrypoint.sh"]`.
- `entrypoint.sh`: espera a la DB, corre `migrate`, `collectstatic`, luego `exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3`.
- Añadir `USER 1000` tras copiar el código y ajustar permisos de `staticfiles`/`mediafiles`.

**DoD del paso**:
- [ ] `CMD`/`ENTRYPOINT` usa `config.wsgi:application`
- [ ] `entrypoint.sh` corre migrate + collectstatic y luego gunicorn
- [ ] Imagen corre como usuario no-root

---

### SUBTAREA 3 — Crear `nginx/nginx.conf` interno del proyecto

**Agente**: @DevOps_Agent
**Archivo**: `nginx/nginx.conf` (nuevo)

Basado en `.infra/nginx/nginx.template.conf`, adaptado a Django:
- `location /` y `location /api/` → `proxy_pass http://web:8000`
- `location /static/` → sirve desde volumen `static_volume`
- `location /media/` → sirve desde volumen `media_volume`
- Sin bloque WebSocket (no aplica). Escucha solo en `:80`. Sin SSL (lo gestiona NPM).

**DoD del paso**:
- [ ] `nginx.conf` rutea `/` y `/api/` a `web:8000`
- [ ] Sirve `/static/` y `/media/` desde volúmenes
- [ ] Escucha solo en puerto 80, sin directivas SSL

---

### SUBTAREA 4 — Reescribir `docker-compose.yml` de producción

**Agente**: @DevOps_Agent
**Archivo**: `docker-compose.yml`

Basado en `.infra/docker-compose.template.yml`:
- `db` (mysql:8.0): volumen `./data/mysql`, healthcheck, **sin puertos al host**.
- `web`: build local, `expose: 8000`, `env_file: .env.prod`, volúmenes `static_volume` y `media_volume` compartidos, depende de `db` healthy, **sin puertos al host**.
- `nginx` (nginx:alpine): `container_name: ecommerce-nginx`, monta `nginx/nginx.conf` + volúmenes static/media (RO), redes `internal` + `proxy-network`, `expose: 80`, **sin puertos al host**.
- Redes: `internal` (bridge) + `proxy-network` (external: true).
- Volúmenes nombrados: `static_volume`, `media_volume`.

**Dependencia de paso anterior**: SUBTAREA 2 y 3 (Dockerfile y nginx.conf).

**DoD del paso**:
- [ ] Tres servicios `db`, `web`, `nginx` sin puertos publicados al host
- [ ] `nginx` en `internal` + `proxy-network` con `container_name: ecommerce-nginx`
- [ ] Volúmenes `static_volume`/`media_volume` compartidos entre `web` y `nginx`
- [ ] `proxy-network` declarada como `external: true`
- [ ] `docker compose config` valida sin error

---

### SUBTAREA 5 — Crear `.env.prod.example` y actualizar ignores

**Agente**: @DevOps_Agent
**Archivos**: `.env.prod.example` (nuevo), `.dockerignore`, `.gitignore`

`.env.prod.example` basado en `.infra/env.template` adaptado a MySQL/Django (sin secretos reales).
`.dockerignore`: excluir `.git`, `.venv`, `node_modules`, `.env*`, `mediafiles/`, `staticfiles/`, caches.
Confirmar que `.gitignore` ya ignora `.env.prod` (ya cubierto por `*.env.prod`).

**DoD del paso**:
- [ ] `.env.prod.example` con todas las variables de producción, sin valores sensibles
- [ ] `.dockerignore` excluye artefactos y secretos
- [ ] `.env.prod` confirmado como ignorado por Git

---

### SUBTAREA 6 — Workflow CI (`.github/workflows/ci.yml`)

**Agente**: @DevOps_Agent
**Archivo**: `.github/workflows/ci.yml` (nuevo)

Trigger: `push` y `pull_request` a `main`. Jobs:
- `checks`: Python 3.12 + MySQL service, instala `requirements/dev.txt`, corre `manage.py check`,
  `makemigrations --check --dry-run`, y `manage.py test`.
- `build`: `docker build` de la imagen de producción (sin push), valida que la imagen compila.

**DoD del paso**:
- [ ] `ci.yml` corre `check`, verificación de migraciones y tests
- [ ] `ci.yml` hace `docker build` de la imagen de producción
- [ ] YAML válido

---

### SUBTAREA 7 — Workflow CD (`.github/workflows/deploy.yml`)

**Agente**: @DevOps_Agent
**Archivo**: `.github/workflows/deploy.yml` (nuevo)

Trigger: `push` a `main` + `workflow_dispatch`. Job `deploy`: usa SSH (secrets `VPS_HOST`, `VPS_USER`,
`VPS_SSH_KEY`, `VPS_PROJECT_PATH`) para: `cd /opt/ecommerce && git pull origin main && docker compose up --build -d && docker compose exec -T web python manage.py migrate --noinput`.

**Dependencia de paso anterior**: SUBTAREA 6 (idealmente CD solo tras CI verde).

**DoD del paso**:
- [ ] `deploy.yml` despliega por SSH usando secrets
- [ ] Ejecuta git pull + compose up --build + migrate
- [ ] YAML válido; documentados los secrets requeridos

---

### SUBTAREA 8 — Actualizar documentación operativa

**Agente**: @Docs_Agent / @DevOps_Agent
**Archivos**: `.infra/OPERATIONS.md` (referencia), `project_manifest.md`

Documentar el paso de carga inicial de datos (`manage.py loaddata data/backup.json`) y el alta del
Proxy Host en NPM. Actualizar `project_manifest.md` (Secciones 5 y 7).

**DoD del paso**:
- [ ] Documentado el `loaddata` de `data/backup.json`
- [ ] Documentado el Proxy Host de NPM (`ecommerce-nginx:80`, dominio, SSL)
- [ ] `project_manifest.md` refleja la nueva arquitectura y FEAT-007 = DONE

---

## Orden de Ejecución

```
SUBTAREA 0 (verificar deps)
   → SUBTAREA 1 (settings module)
   → SUBTAREA 2 (Dockerfile + entrypoint)
   → SUBTAREA 3 (nginx.conf)
   → SUBTAREA 4 (docker-compose.yml)   [depende de 2 y 3]
   → SUBTAREA 5 (.env.prod.example + ignores)
   → SUBTAREA 6 (CI)
   → SUBTAREA 7 (CD)                    [depende de 6]
   → SUBTAREA 8 (docs + manifiesto)
   → VERIFY (validaciones) → HANDOFF COMPLETION
```

---

## Criterios de Aceptación Globales (DoD)

- [ ] Ningún servicio interno (`db`, `web`) publica puertos al host.
- [ ] `nginx` interno (`ecommerce-nginx`) en `proxy-network`, sirve estáticos/media y proxya a `web`.
- [ ] `Dockerfile` corregido (`config.wsgi`) con entrypoint que corre migrate + collectstatic.
- [ ] `DJANGO_SETTINGS_MODULE` por defecto válido en wsgi/asgi/manage.
- [ ] `.github/workflows/ci.yml` y `deploy.yml` presentes y con YAML válido.
- [ ] `.env.prod.example` y `.dockerignore` creados; secretos no versionados.
- [ ] `docker compose -f docker-compose.yml config` valida sin errores.
- [ ] `project_manifest.md` actualizado y FEAT-007 marcada como DONE.

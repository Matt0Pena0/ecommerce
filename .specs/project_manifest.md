# Manifiesto del Proyecto — Ecommerce

> **Fuente única de verdad** del proyecto. Todos los agentes deben consultar este archivo
> antes de tomar decisiones de arquitectura, implementación o planificación.

---

## 1. Project Identity

* **Name:** Ecommerce
* **Core Purpose:** Sistema de e-commerce para gestión de productos, carrito de compras y órdenes con panel de administración avanzado.
* **Technology Stack:**
    * **Backend:** Django (Python 3.12)
    * **Frontend:** Django Templates + Bootstrap 5 + SCSS + JavaScript (ES Modules)
    * **Database:** MySQL 8.0
    * **Cache/Broker:** No configurado actualmente
    * **Infrastructure:** Docker Compose
    * **Gateway:** Nginx (externo, reverse proxy)
    * **Deployment:** Servidor con Gunicorn + Docker Compose, dominio `ecommerce.themattdev.com`

---

## 2. Architecture Blueprint

* **Topology:** Monolito Django con renderizado server-side (SSR). Las apps Django encapsulan la lógica de negocio. El frontend se sirve vía templates Django con Bootstrap 5 y JavaScript vanilla (ES modules) para interactividad.
* **Layers:**
    * **Presentación:** Django Templates + Bootstrap 5 + JS (ES Modules)
    * **API REST:** Django REST Framework (endpoints para productos y carrito)
    * **Lógica de Negocio:** Views + Services en cada app Django
    * **Datos:** Django ORM sobre MySQL 8.0
    * **Infraestructura:** Docker Compose (MySQL + Gunicorn)

### Diagrama de Alto Nivel

```
Cliente (Browser)
    │
    ▼
┌────────────────────────────────────────┐
│  Nginx (reverse proxy externo)         │
│  SSL termination                       │
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│  Gunicorn (WSGI)                       │
│  Puerto 8000                           │
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│  Django Application                    │
│  ┌──────────┐ ┌──────────┐ ┌────────┐│
│  │ accounts │ │productos │ │ordenes ││
│  └──────────┘ └──────────┘ └────────┘│
│  ┌──────────┐ ┌──────────┐           │
│  │ carrito  │ │  core    │           │
│  └──────────┘ └──────────┘           │
│                                        │
│  DRF API: /api/productos/, /api/carrito/│
│  Templates: SSR con Bootstrap 5        │
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│  MySQL 8.0                             │
│  Puerto 3306 (solo red interna)        │
└────────────────────────────────────────┘
```

---

## 3. Directory Standard

```
ecommerce/
├── .agents/                    ← System prompts de agentes SDD
├── .config/                    ← Configuración de agentes (agents.json)
├── .context/                   ← Sistema de handoffs entre agentes
├── .infra/                     ← Plantillas de infraestructura
├── .specs/                     ← Specs de features y planes de acción
├── accounts/                   ← App: autenticación y gestión de usuarios
│   ├── models.py               (UsuarioBase - AbstractUser + direccion)
│   ├── views.py                (Login, Logout, Register)
│   ├── forms.py
│   ├── services.py
│   ├── signals.py
│   ├── urls/                   (urls_base, password_change, password_reset)
│   ├── templatetags/
│   └── tests/
├── productos/                  ← App: catálogo de productos
│   ├── models.py               (Producto, Marca, Categoria, Gondola, UnidadMedida, Codigo)
│   ├── api.py                  (ProductoViewSet - DRF)
│   ├── serializers.py
│   ├── filters.py
│   └── view.py                 (ProductoListView - template-based)
├── carrito/                    ← App: carrito de compras
│   ├── models.py               (Carrito, ItemCarrito)
│   ├── api.py                  (CarritoViewSet - DRF)
│   ├── serializers.py
│   └── views.py                (CarritoListView - template-based)
├── ordenes/                    ← App: órdenes de compra
│   ├── models.py               (Orden, ItemOrden, EstadoOrden)
│   ├── views.py                (Listar, Detalle, Exportar)
│   └── urls.py
├── core/                       ← App: páginas generales (home, contacto)
│   ├── views.py
│   ├── context_processors.py
│   └── urls.py
├── config/                     ← Configuración Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/                  ← Templates Django (frontend)
│   ├── LayoutBase.html
│   ├── _includes/              (navbar, footer, toast, modals)
│   ├── accounts/               (login, register, password)
│   ├── ordenes/                (listar, detalle)
│   ├── core/                   (home)
│   ├── ListarProductos.html
│   ├── ListarCarrito.html
│   └── EliminarProducto.html
├── static/                     ← Assets estáticos (frontend)
│   ├── bootstrap/              (JS bundle local)
│   ├── css/
│   │   ├── base.css
│   │   ├── scss/styles.scss
│   │   └── dist/styles.css     (compilado via npm build)
│   ├── js/
│   │   ├── main.js
│   │   ├── carrito.js
│   │   ├── catalogo.js
│   │   └── modules/            (api.js, ui.js, utils.js, clipboard.js)
│   └── img/
├── mediafiles/                 ← Uploads (imágenes de productos)
├── data/                       ← Data fixtures (backup.json, data.json)
├── docker-compose.yml          ← Producción (MySQL + Gunicorn)
├── docker-compose.dev.yml      ← Desarrollo (MySQL + runserver)
├── Dockerfile                  ← Multi-stage: Node (SCSS) + Python
├── Dockerfile.dev              ← Dev con hot-reload
├── manage.py
├── package.json                ← npm build para SCSS
├── .env / .env.dev             ← Variables de entorno
└── project_manifest.md         ← Este archivo
```

---

## 4. Agent Roster & Scope

| Agente | Rol | Dominio (Scope) | Zonas Prohibidas |
|--------|-----|-----------------|------------------|
| @Orchestrator_Agent | PM Técnico y Director de Orquesta | `.specs/`, `.context/handoffs/`, `project_manifest.md` | Apps Django, `templates/`, `static/`, archivos Docker |
| @Architect_Agent | Arquitecto de Soluciones Senior | `.specs/`, `project_manifest.md` | Apps Django, `templates/`, `static/`, archivos Docker |
| @Backend_Agent | Ingeniero Python/Django | `accounts/`, `productos/`, `ordenes/`, `carrito/`, `core/`, `config/` | `templates/`, `static/`, archivos Docker |
| @Frontend_Agent | Ingeniero Django Templates + Bootstrap 5 | `templates/`, `static/` | Apps Django, archivos Docker |
| @DevOps_Agent | Ingeniero de Infraestructura | `.infra/`, `docker-compose.yml`, `docker-compose.dev.yml`, `Dockerfile`, `Dockerfile.dev` | Lógica de negocio en apps Django, `templates/`, `static/` |
| @Tester_Agent | SDET | `accounts/tests/`, `*/tests/`, `tests/` | Código de producción (solo reporta fallos) |
| @Docs_Agent | Documentación técnica | `project_manifest.md`, `docs/`, `README.md` | Código de producción |

---

## 5. State & Task Tracking

| Feature ID | Componente | Descripción | Estado |
|------------|-----------|-------------|--------|
| FEAT-001 | Backend + Frontend | Autenticación de usuarios (login, register, password reset) | DONE |
| FEAT-002 | Backend + Frontend | Catálogo de productos (CRUD, listado, filtros) | DONE |
| FEAT-003 | Backend + Frontend | Carrito de compras (agregar, quitar, listar) | DONE |
| FEAT-004 | Backend + Frontend | Órdenes de compra (crear, listar, detalle, exportar) | DONE |
| FEAT-005 | Backend | API REST productos y carrito (DRF ViewSets) | DONE |
| FEAT-006 | DevOps | Dockerización (producción + desarrollo) | DONE |
| FEAT-007 | DevOps | Integración infra VPS (nginx interno + proxy-network) + CI/CD GitHub Actions | DONE |
| FEAT-008 | DevOps | Despliegue vía GHCR (registry) en lugar de build en el VPS | DONE |

### Estados Válidos

- `PENDING` — Feature registrada, sin spec aprobado
- `SPEC_APPROVED` — Spec aprobado por @Architect_Agent
- `IN_PROGRESS` — Implementación en curso
- `TESTING` — En fase de validación por @Tester_Agent
- `DONE` — Completada y verificada
- `BLOCKED` — Impedimento activo

---

## 6. Development Standards

### Convenciones de Nomenclatura

**Python/Django (Backend):**
- Archivos: `snake_case.py`
- Clases (Models, Views, Forms): `PascalCase`
- Funciones y variables: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`
- URLs: `kebab-case` en paths, `snake_case` en names

**Templates (Frontend):**
- Templates: `PascalCase.html` (e.g., `ListarProductos.html`, `LayoutBase.html`)
- Parciales/includes: `_snake_case.html` con prefijo `_`
- Archivos CSS/SCSS: `kebab-case`
- Archivos JS: `camelCase` o `kebab-case`
- Funciones JS: `camelCase`

**Infraestructura:**
- Servicios Docker: `kebab-case`
- Variables de entorno: `UPPER_SNAKE_CASE`
- Nombres de contenedor: `{proyecto}-{servicio}` (e.g., `ecommerce-db`, `ecommerce-web`)

### Git Workflow

- Rama principal: `main`
- Feature branches: `feat/{FEAT_ID}-descripcion-corta`
- Fix branches: `fix/{descripcion-corta}`
- Commits: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `ci:`)

### Manejo de Errores

- Backend: Excepciones Django estándar + DRF exception handling para APIs
- Templates: Mensajes via Django Messages framework (toast notifications en frontend)
- API: Respuestas JSON estructuradas con códigos HTTP semánticos
- Logging: Configuración estándar Django (`django.utils.log`)

---

## 7. Infraestructura y Despliegue

### Configuración del Servidor

| Parámetro | Valor |
|-----------|-------|
| **Ruta base en servidor** | `/opt` |
| **Slug del proyecto** | `ecommerce` |
| **Dominio** | `ecommerce.themattdev.com` |
| **Gateway central** | Nginx Proxy Manager (red `proxy-network`) |
| **Repositorio** | `github.com/Matt0Pena0/ecommerce` |
| **Rama de despliegue** | `main` |
| **Acceso administrativo** | Tailscale (VPN). SSH y panel del gateway sin exposición pública. |

### Servicios (docker-compose.yml producción)

| Servicio | Contenedor | Imagen | Redes | Puerto al host |
|----------|-----------|--------|-------|----------------|
| Base de datos | `ecommerce-db` | `mysql:8.0` | `internal` | Ninguno |
| Backend | `ecommerce-web` | Build local (multi-stage: Node + Python) | `internal` | Ninguno (expose 8000) |
| Nginx interno | `ecommerce-nginx` | `nginx:alpine` | `internal`, `proxy-network` | Ninguno (expose 80) |

- **Cero puertos al host**: solo `ecommerce-nginx` es visible al gateway vía `proxy-network`.
- **Estáticos/media**: servidos por `ecommerce-nginx` desde los volúmenes `static_volume` y `media_volume` compartidos con `web`.
- **Arranque autónomo**: el entrypoint (`docker/entrypoint.sh`) corre `migrate` + `collectstatic` antes de Gunicorn.

### CI/CD (GitHub Actions)

| Workflow | Trigger | Propósito |
|----------|---------|-----------|
| `.github/workflows/ci.yml` | push/PR a `main` | `check`, verificación de migraciones, `pytest`, build de validación (sin push) |
| `.github/workflows/deploy.yml` | push a `main` / manual | `build-and-push` a GHCR → `deploy` por SSH (`pull` + `up -d`) |

### Estrategia de imágenes (FEAT-008)

| Parámetro | Valor |
|-----------|-------|
| Registry | `ghcr.io/matt0pena0/ecommerce/web` |
| Tags | `latest` (móvil), `sha-<short>` (inmutable) |
| Build | En el runner de GitHub Actions. **El VPS no compila.** |
| Deploy | Runner se une al tailnet (nodo efímero) → SSH a IP interna → `docker login ghcr.io` + `pull` + `up -d` |
| Rollback | `WEB_TAG=sha-<short> docker compose up -d web` |

### Plantillas y Guías

- `.infra/` — plantillas de infraestructura de referencia.
- `.infra/DEPLOYMENT.md` — guía de despliegue específica del proyecto (fixtures, Proxy Host, secrets).
- `.infra/OPERATIONS.md` — comandos operativos genéricos.

---

## 8. Protocolo de Ejecución de Funcionalidades

Toda nueva funcionalidad sigue el Ciclo SDD de 7 fases:

1. **Explore** — Analizar el requerimiento y el estado actual del proyecto
2. **Propose** — Presentar propuesta de solución al usuario
3. **Design** — @Architect_Agent diseña la solución técnica
4. **Spec** — Se redacta el `.spec.md` de la feature en `.specs/features/`
5. **Tasks** — @Orchestrator_Agent genera el Action Plan en `.specs/tasks/`
6. **Apply** — Agentes especialistas implementan según el plan aprobado
7. **Verify** — @Tester_Agent valida contra los criterios de aceptación del spec

> **Regla fundamental:** Ningún agente escribe código de producción sin un `.spec.md` aprobado.

# Infraestructura — Guía de Despliegue Multi-Proyecto

> Guía abstracta y plantillas reutilizables para desplegar cualquier proyecto
> construido con este framework en un servidor compartido usando contenedores
> por proyecto + gateway central.

---

## Visión General

Esta arquitectura permite hospedar múltiples proyectos en un mismo servidor,
cada uno completamente aislado, con un gateway central que gestiona el ruteo
por subdominio y la terminación SSL.

```
Internet
    │
    ▼
┌─────────────────────────────────────┐
│  Servidor — puertos 80/443 abiertos │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Gateway Central (Nginx Proxy Manager)│
│  SSL termination + routing          │
│  Red: proxy-network                 │
└─────────────────────────────────────┘
    │                         │
    ▼                         ▼
┌────────────────┐   ┌────────────────┐
│ proyecto-a     │   │ proyecto-b     │
│ nginx (p. 80)  │   │ nginx (p. 80)  │
└────────────────┘   └────────────────┘
    │                         │
    ▼                         ▼
┌────────────────┐   ┌────────────────┐
│ Red interna    │   │ Red interna    │    ← Aisladas entre sí
│ - backend      │   │ - backend      │
│ - frontend     │   │ - frontend     │
│ - db           │   │ - db           │
│ - cache        │   │ - cache        │
└────────────────┘   └────────────────┘
```

---

## Principios de Infraestructura

| # | Principio | Descripción |
|---|-----------|-------------|
| 1 | **Autonomía por proyecto** | Cada proyecto tiene su propio `docker-compose.yml`, red interna y datos aislados. |
| 2 | **Gateway centralizado** | Un único Nginx Proxy Manager rutea subdominios al nginx interno de cada proyecto. |
| 3 | **SSL centralizado** | La terminación TLS la gestiona el gateway con certificados automáticos. |
| 4 | **Cero puertos expuestos** | Ningún servicio interno (DB, cache, backend) publica puertos al host. |
| 5 | **Reproducibilidad** | Toda la infraestructura es declarativa y versionable (excepto secretos). |
| 6 | **Security by Design** | Imágenes mínimas, usuarios no-root, healthchecks, secretos vía `.env`. |

---

## Estructura en el Servidor

```
/opt/
├── proxy/                              ← Gateway central (Nginx Proxy Manager)
│   ├── docker-compose.yml              ← Desde .infra/proxy/docker-compose.template.yml
│   └── data/                           ← Certificados SSL, configuración
│
├── ecommerce/                   ← Proyecto desplegado
│   ├── docker-compose.yml              ← Desde .infra/docker-compose.template.yml
│   ├── nginx/nginx.conf                ← Desde .infra/nginx/nginx.template.conf
│   ├── backend/                        ← Código + Dockerfile
│   ├── frontend/                       ← Código + Dockerfile
│   ├── data/                           ← Volúmenes persistentes (DB, cache)
│   └── .env.prod                       ← Desde .infra/env.template (NO versionado)
│
└── otro-proyecto/             ← Proyecto N (completamente aislado)
    └── ...
```

---

## Contenido de este Directorio

| Archivo | Propósito |
|---------|-----------|
| `README.md` | Este archivo. Guía completa de infraestructura y despliegue. |
| `docker-compose.template.yml` | Orquestación para proyecto completo (DB + Cache + Backend + Frontend + Nginx). |
| `docker-compose.frontend-only.template.yml` | Variante para proyectos sin backend (solo frontend/estáticos). |
| `nginx/nginx.template.conf` | Reverse proxy interno del proyecto con headers de seguridad. |
| `proxy/docker-compose.template.yml` | Gateway central (Nginx Proxy Manager) con SSL automático. |
| `env.template` | Plantilla de variables de entorno para producción. |
| `MIGRATION_CHECKLIST.md` | Checklist para migrar un proyecto existente a esta arquitectura. |
| `SECURITY.md` | Consideraciones de seguridad para infraestructura multi-proyecto. |
| `OPERATIONS.md` | Comandos operativos comunes (deploy, logs, backup, restart). |

---

## Flujo de Despliegue

### Primera vez (configurar el servidor)

```bash
# 1. Crear la red compartida del gateway (una sola vez)
docker network create proxy-network

# 2. Configurar el gateway central
cp .infra/proxy/docker-compose.template.yml /opt/proxy/docker-compose.yml
# → Sustituir placeholders
cd /opt/proxy && docker compose up -d
```

### Desplegar un proyecto nuevo

```bash
# 1. Crear estructura del proyecto
mkdir -p /opt/ecommerce/{nginx,data,backend,frontend}

# 2. Copiar y adaptar plantillas
cp .infra/docker-compose.template.yml /opt/ecommerce/docker-compose.yml
cp .infra/nginx/nginx.template.conf /opt/ecommerce/nginx/nginx.conf
cp .infra/env.template /opt/ecommerce/.env.prod

# 3. Sustituir {{PLACEHOLDERS}} con valores reales del proyecto

# 4. Levantar servicios
cd /opt/ecommerce && docker compose up -d

# 5. Configurar ruteo en el gateway
#    Domain: ecommerce.themattdev.com
#    Forward Host: ecommerce-nginx
#    Forward Port: 80
#    SSL: Certificado automático
```

### Deploy de actualización

El deploy normal es automático vía GitHub Actions (`push` a `main`). El VPS **no construye
imágenes**: las descarga desde GHCR. Ver `.infra/DEPLOYMENT.md`.

Deploy manual desde el servidor (excepcional, requiere `docker login ghcr.io`):

```bash
cd /opt/ecommerce
git pull origin main          # compose, nginx.conf, fixtures
docker compose pull web       # imagen publicada por Actions
docker compose up -d
```

---

## Adaptaciones por Tipo de Proyecto

| Tipo de Proyecto | Plantilla Base | Servicios |
|-----------------|----------------|-----------|
| Full-stack (API + SPA) | `docker-compose.template.yml` | DB + Cache + Backend + Frontend + Nginx |
| Full-stack sin cache | `docker-compose.template.yml` (quitar servicio `cache`) | DB + Backend + Frontend + Nginx |
| Solo frontend / estáticos | `docker-compose.frontend-only.template.yml` | Frontend + Nginx |
| Solo API (sin frontend) | `docker-compose.template.yml` (quitar `frontend`, ajustar nginx) | DB + Cache + Backend + Nginx |

---

## Placeholders de Infraestructura

Valores concretos con los que está instanciada la infraestructura de **Ecommerce**.
Al adaptar las plantillas a otro proyecto, sustituir por los suyos.

| Parámetro | Valor en Ecommerce |
|-----------|--------------------|
| Slug del proyecto | `ecommerce` |
| Ruta base en el servidor | `/opt` (proyecto en `/opt/ecommerce`) |
| Gateway central | Nginx Proxy Manager (`jc21/nginx-proxy-manager:latest`) |
| **Red compartida del proxy** | **`proxy-network`** (estándar de la VPS) |
| Puerto del panel del gateway | `81` (solo alcanzable por VPN) |
| **Acceso administrativo (SSH)** | **Tailscale** — IP interna `100.x.y.z`, sin puertos públicos |
| Dominio | `ecommerce.themattdev.com` |
| Rama de despliegue | `main` |
| Imagen de base de datos | `mysql:8.0` (puerto interno `3306`) |
| Cache | No configurado |
| Puerto interno del backend | `8000` (Gunicorn) |
| Nginx interno | `nginx:alpine`, contenedor `ecommerce-nginx`, puerto `80` |
| UID del usuario en contenedores | `1000` |
| Firewall | `ufw` |
| **Registry de imágenes** | **`ghcr.io/matt0pena0/ecommerce/web`** |
| Tags de imagen | `latest` (móvil) y `sha-<short>` (inmutable, para rollback) |

> La red **debe** llamarse `proxy-network` en todos los proyectos de la VPS. El nombre
> anterior `proxy_net` está descontinuado.

---

## Resumen de Puertos

| Servicio | Puerto Host | Acceso |
|----------|-------------|--------|
| Gateway (HTTP) | 80 | Público |
| Gateway (HTTPS) | 443 | Público |
| Gateway (Admin) | 81 | Solo por VPN (`tailscale0`) |
| SSH | 22 | Solo por VPN (`tailscale0`), no público |
| Proyectos internos | Ninguno | Solo via proxy-network |
| DB/Cache | Ninguno | Solo red interna del proyecto |

**Regla de oro**: Si un servicio no necesita ser accesible desde internet, NO publica puertos al host.

---

## Documentación Complementaria

| Documento | Contenido |
|-----------|-----------|
| `OPERATIONS.md` | Deploy, logs, backup, restart, monitoreo |
| `MIGRATION_CHECKLIST.md` | Pasos para migrar un proyecto existente |
| `SECURITY.md` | Red, contenedores, credenciales, firewall |

---

## Relación con el Framework SDD

- El **@DevOps_Agent** es el responsable exclusivo de la infraestructura (`.infra/`).
- Toda modificación de infraestructura requiere un **`.spec.md` aprobado** (Ciclo SDD).
- Los valores específicos de proyecto se declaran en el **manifiesto** (`.specs/project_manifest_template.md`).
- Los placeholders siguen el formato `{{UPPER_SNAKE_CASE}}` estándar del framework.

---

## Cómo Usar

1. **Copia** las plantillas relevantes a la raíz de tu proyecto.
2. **Sustituye** los `{{PLACEHOLDER}}` con los valores de tu stack.
3. **Adapta** las plantillas según las necesidades específicas (quitar servicios no usados, agregar otros).
4. **Configura** el gateway central (una sola vez por servidor).
5. **Despliega** usando los comandos documentados en `OPERATIONS.md`.

> Consulta `MIGRATION_CHECKLIST.md` para migrar un proyecto existente a esta arquitectura.

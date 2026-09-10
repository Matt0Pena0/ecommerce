# FEAT-008 — Despliegue vía GHCR (registry) en lugar de build en el VPS

**Feature ID**: FEAT-008
**Componente**: DevOps / CI-CD
**Estado**: SPEC_APPROVED
**Depende de**: FEAT-007 (infra VPS + CI/CD)
**Supersede**: la decisión #3 de FEAT-007 (build local en el VPS)

---

## Objetivo

Migrar la estrategia de despliegue de **build en el VPS** a **imagen preconstruida en
GitHub Container Registry (GHCR)**. El servidor deja de compilar: solo hace `pull` de una
imagen ya validada y levanta los contenedores.

Además, consolidar el nombre de la red compartida del gateway como **`proxy-network`** en
toda la documentación e infraestructura (estándar de la VPS multi-proyecto).

### Motivación

| Problema con build en el VPS | Efecto |
|---|---|
| Build multi-stage (Node + `pip install` + compilación de `mysqlclient`) | Consume CPU/RAM del servidor de producción |
| Varios proyectos en la misma VPS construyendo | Builds simultáneos compiten por recursos |
| Fallo de build a mitad del deploy | Stack en estado inconsistente |
| Sin artefacto versionado | Rollback requiere rebuild desde un commit anterior |

Con GHCR el build ocurre en el runner de Actions, el VPS recibe un artefacto inmutable y
trazable, el deploy es rápido y el rollback es inmediato (cambiar de tag).

### Fuera de alcance

- El compose de **desarrollo** (`docker-compose.dev.yml`) sigue construyendo localmente
  con `Dockerfile.dev`. Esta feature solo afecta producción.
- No se cambia el `Dockerfile` de producción (se sigue usando, ahora en el runner).
- No se cambia nginx, entrypoint, ni el modelo de estáticos/media de FEAT-007.

---

## Arquitectura Objetivo

```
push a main
    │
    ▼
┌──────────────────────────────────────────────┐
│ GitHub Actions — runner                      │
│  1. checks (django check, migraciones, pytest)│
│  2. docker build (multi-stage)                │
│  3. push -> ghcr.io/matt0pena0/ecommerce/web  │
│       tags: latest, sha-<short>               │
└──────────────────────────────────────────────┘
    │ SSH
    ▼
┌──────────────────────────────────────────────┐
│ VPS /opt/ecommerce                            │
│  - git sync (compose, nginx.conf, fixtures)   │
│  - docker login ghcr.io                       │
│  - docker compose pull                        │
│  - docker compose up -d   (SIN --build)       │
└──────────────────────────────────────────────┘
```

---

## Contratos

### Imagen

| Campo | Valor |
|---|---|
| Registry | `ghcr.io` |
| Repositorio de imagen | `ghcr.io/matt0pena0/ecommerce/web` |
| Tag móvil | `latest` (apunta al último `main`) |
| Tag inmutable | `sha-<short_sha>` (trazabilidad y rollback) |
| Visibilidad | Privada por defecto (requiere auth para `pull`) |

> GHCR exige que la ruta de la imagen esté en **minúsculas**. El workflow normaliza
> `${{ github.repository }}` a minúsculas.

### Servicio `web` en `docker-compose.yml`

```yaml
web:
  image: ghcr.io/matt0pena0/ecommerce/web:${WEB_TAG:-latest}
  pull_policy: always
```

El default `:-latest` evita que la variable quede vacía si `WEB_TAG` no está definida
(el compose no depende de `.env` para esto).

### Workflows

| Workflow | Trigger | Jobs |
|---|---|---|
| `ci.yml` | `pull_request` a `main` | `checks` + `build` (build de validación, **sin** push) |
| `deploy.yml` | `push` a `main`, `workflow_dispatch` | `build-and-push` (a GHCR) → `deploy` (SSH: pull + up) |

El job `deploy` **depende** de `build-and-push`: si la imagen no se publica, no se despliega.

### Secrets y permisos

| Nombre | Tipo | Uso |
|---|---|---|
| `GITHUB_TOKEN` | automático | `push` a GHCR (requiere `permissions: packages: write`) |
| `GHCR_TOKEN` | secret (opcional, recomendado) | PAT con `read:packages` para que el VPS pueda hacer `pull` de forma autónoma |
| `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`, `VPS_DEPLOY_PATH` | secrets | Acceso SSH. `VPS_HOST` es la **IP de Tailscale** (`100.x.y.z`), no la pública. `VPS_DEPLOY_PATH` = `/opt/ecommerce`. |
| `TS_OAUTH_CLIENT_ID`, `TS_OAUTH_SECRET` | secrets | OAuth client de Tailscale (scope `auth_keys`) para unir el runner al tailnet |
| `ENV_PROD` | secret (opcional) | Contenido de `.env.prod` |

### Acceso a la red privada

El VPS no expone SSH a internet (firewall + VPN Tailscale con IP interna estable). El job
`deploy` une al runner al tailnet como **nodo efímero** con `tailscale/github-action@v3` y
tag `tag:ci` antes de conectarse. El nodo se descarta al finalizar el job.

Requiere en el panel de Tailscale: OAuth client con scope `auth_keys` (escritura), `tag:ci`
declarado en `tagOwners`, y una ACL que permita `tag:ci → VPS:22`.

Si `GHCR_TOKEN` no está definido, el workflow usa `GITHUB_TOKEN` para el `docker login`
en el VPS (válido solo durante la ejecución del job).

---

## Modelo de Datos

No aplica.

---

## Criterios de Aceptación (DoD)

- [ ] `docker-compose.yml` usa `image: ghcr.io/matt0pena0/ecommerce/web:${WEB_TAG:-latest}` y ya no tiene `build:` en `web`.
- [ ] `deploy.yml` tiene job `build-and-push` que publica en GHCR con tags `latest` y `sha-<short>`.
- [ ] `deploy.yml` hace `docker login ghcr.io`, `docker compose pull` y `docker compose up -d` (sin `--build`).
- [ ] `deploy.yml` declara `permissions: packages: write`.
- [ ] `deploy.yml` une el runner al tailnet vía `tailscale/github-action@v3` antes del SSH.
- [ ] Documentado que `VPS_HOST` es la IP de Tailscale y no la pública.
- [ ] `.infra/SECURITY.md` refleja que SSH y el panel del gateway van solo por VPN.
- [ ] `ci.yml` conserva el build de validación en PRs sin publicar imagen.
- [ ] La red del gateway se llama `proxy-network` en todo el repositorio (cero ocurrencias de `proxy_net`).
- [ ] Documentación actualizada sin referencias a `up --build` en producción: `.infra/DEPLOYMENT.md`, `.infra/OPERATIONS.md`, `.infra/README.md`, `.infra/docker-compose.template.yml`, `README.dev.md` (sección prod).
- [ ] `project_manifest.md` refleja la nueva estrategia (Sección 7) y registra FEAT-008.
- [ ] FEAT-007 queda marcada como parcialmente superseded (decisión #3).
- [ ] Procedimiento de rollback documentado (`WEB_TAG=sha-... docker compose up -d`).
- [ ] `docker compose config` valida sin errores.

---

## Dependencias

| Dependencia | Estado | Fuente |
|---|---|---|
| FEAT-007 implementada | DONE | `.specs/features/FEAT-007-*.spec.md` |
| Repo con GitHub Packages habilitado | Disponible | `github.com/Matt0Pena0/ecommerce` |
| Docker en el VPS con acceso a red saliente | Asumido | Infra existente |
| `Dockerfile` de producción funcional | DONE | FEAT-007 |

---

## Constraints

- **El VPS sigue necesitando el repositorio clonado**: `docker-compose.yml`, `nginx/nginx.conf`,
  `mediafiles/` semilla y `data/backup.json` viven en el repo. Solo desaparece el build.
- **Ruta de imagen en minúsculas** (requisito de GHCR).
- **`pull_policy: always`** para que `up -d` no reutilice una imagen local obsoleta.
- **Sin secretos en la imagen**: la configuración sigue inyectándose por `.env.prod` en runtime.
- **Red `proxy-network`** como único nombre válido; `proxy_net` queda prohibido.

---

## Contexto Mínimo

- `docker-compose.yml`
- `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`
- `Dockerfile`
- `.infra/DEPLOYMENT.md`, `.infra/OPERATIONS.md`, `.infra/README.md`
- `.infra/docker-compose.template.yml`
- `.specs/features/FEAT-007-infra-vps-cicd.spec.md` (decisión #3 superseded)

---

## Rollback

```bash
# En el VPS: volver a una imagen anterior por SHA
cd /opt/ecommerce
WEB_TAG=sha-a1b2c3d docker compose up -d web

# Para fijarlo de forma persistente, exportar WEB_TAG en el entorno del shell
# o añadirlo a .env.prod (Compose lo lee vía env_file para el contenedor, pero
# para la interpolación de `image:` debe estar en el entorno del shell).
```

> Nota: `WEB_TAG` se usa en interpolación de Compose, por lo que debe venir del shell
> (o de `./.env`), no de `env_file`. El default `latest` cubre el caso normal.

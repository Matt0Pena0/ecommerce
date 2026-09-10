# ACTION PLAN — FEAT-008: Despliegue vía GHCR

**Generado por**: @Orchestrator_Agent
**Fecha**: 2026-09-03
**Estado**: APROBADO (auditado por @Architect_Agent)
**Spec**: `.specs/features/FEAT-008-ghcr-registry-deploy.spec.md`

---

## Análisis de Dependencias

| Dependencia | Disponible | Fuente |
|-------------|-----------|--------|
| FEAT-007 implementada | Sí (DONE) | `.specs/features/FEAT-007-*.spec.md` |
| `Dockerfile` de producción | Sí | Raíz del proyecto |
| GitHub Packages en el repo | Sí | `github.com/Matt0Pena0/ecommerce` |
| Secret `GHCR_TOKEN` (opcional) | Pendiente (acción del usuario) | GitHub Actions Secrets |

---

## Subtareas y Asignación

### SUBTAREA 1 — `docker-compose.yml`: build → image

**Agente**: @DevOps_Agent · **Archivo**: `docker-compose.yml`

Sustituir el bloque `build:` del servicio `web` por `image:` apuntando a GHCR, con
`pull_policy: always` y tag parametrizable para rollback.

**DoD**:
- [x] `image: ghcr.io/matt0pena0/ecommerce/web:${WEB_TAG:-latest}`
- [x] `pull_policy: always`
- [x] Sin `build:` en `web`
- [x] Cabecera del archivo actualizada (setup sin `--build`)

---

### SUBTAREA 2 — `deploy.yml`: job de build+push a GHCR

**Agente**: @DevOps_Agent · **Archivo**: `.github/workflows/deploy.yml`

Job `build-and-push` con `permissions: packages: write`, login vía `GITHUB_TOKEN`,
normalización a minúsculas de la ruta de imagen, y tags `latest` + `sha-<short>`.

**DoD**:
- [x] `permissions: packages: write` declarado
- [x] Ruta de imagen normalizada a minúsculas
- [x] Tags `latest` y `sha-<short>`
- [x] Caché de GHA activada

---

### SUBTAREA 3 — `deploy.yml`: job de deploy con pull

**Agente**: @DevOps_Agent · **Archivo**: `.github/workflows/deploy.yml`

Job `deploy` dependiente de `build-and-push`: login en GHCR desde el VPS,
`docker compose pull web`, `docker compose up -d` (sin `--build`), `docker logout`.

**DoD**:
- [x] `needs: [build-and-push]` con guarda para `skip_build`
- [x] `docker login` con `GHCR_TOKEN` o fallback a `GITHUB_TOKEN`
- [x] `docker compose pull` + `up -d`, sin `--build`
- [x] `docker logout` al final

---

### SUBTAREA 4 — `ci.yml`: build de validación sin push

**Agente**: @DevOps_Agent · **Archivo**: `.github/workflows/ci.yml`

Mantener el build como validación en PRs; documentar que la publicación es de `deploy.yml`.

**DoD**:
- [x] `push: false` conservado
- [x] Comentario aclarando la separación de responsabilidades

---

### SUBTAREA 5 — Documentación e infraestructura de referencia

**Agente**: @DevOps_Agent / @Docs_Agent

Actualizar todo lo que asumía build en el VPS y consolidar `proxy-network`:
`.infra/DEPLOYMENT.md`, `.infra/OPERATIONS.md`, `.infra/README.md`,
`.infra/docker-compose.template.yml`, `.infra/docker-compose.frontend-only.template.yml`,
`README.dev.md`, `README.md`, `project_manifest.md`.

**DoD**:
- [x] Cero `up --build` referido a producción
- [x] Rollback documentado (`WEB_TAG=sha-...`)
- [x] Secret `GHCR_TOKEN` documentado
- [x] Plantillas de `.infra/` usan `image:` con `{{GH_OWNER}}/{{GH_REPO}}`
- [x] Tabla de valores de `.infra/README.md` reparada y con datos de GHCR
- [x] `proxy-network` como único nombre en el repositorio

---

### SUBTAREA 6 — Marcar FEAT-007 como parcialmente superseded

**Agente**: @Architect_Agent (Regla de Espejo)

No se reescribe la historia: se anota la decisión #3 y la fila de `deploy.yml` como
superseded, con puntero a FEAT-008.

**DoD**:
- [x] Nota de superseded en el spec de FEAT-007
- [x] Nota de superseded en el plan de FEAT-007

---

## Orden de Ejecución

```
1 (compose) → 2 (build-push) → 3 (deploy pull) → 4 (ci) → 5 (docs) → 6 (superseded) → VERIFY
```

---

## Criterios de Aceptación Globales (DoD)

- [x] El VPS no construye imágenes en ningún flujo de producción.
- [x] Imagen publicada en GHCR con tags móvil e inmutable.
- [x] `docker compose config` valida sin errores.
- [x] Workflows con YAML válido.
- [x] Cero ocurrencias de `proxy_net` en el repositorio.
- [x] Rollback documentado y sin rebuild.
- [ ] Verificación end-to-end del primer deploy real (requiere secrets configurados).

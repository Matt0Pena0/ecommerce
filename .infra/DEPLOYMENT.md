# Guía de Despliegue — Ecommerce

> Guía específica del proyecto **Ecommerce** sobre la arquitectura VPS multi-proyecto
> (gateway central Nginx Proxy Manager + red `proxy-network`).
> Para comandos operativos genéricos, ver `.infra/OPERATIONS.md`.

---

## Arquitectura de Despliegue

```
Internet (443)
   │
   ▼
Nginx Proxy Manager (proxy-network)  ── SSL Let's Encrypt
   │  Forward Host: ecommerce-nginx:80
   ▼
ecommerce-nginx (nginx:alpine)  ── sirve /static/ y /media/, proxya a web
   │ internal
   ▼
ecommerce-web (gunicorn :8000) ──▶ ecommerce-db (mysql:8.0)
```

Ningún servicio interno publica puertos al host. Solo `ecommerce-nginx` es visible al
gateway a través de la red externa `proxy-network`.

---

## Modelo de Despliegue: GitHub Actions + GHCR

El despliegue **no se hace a mano en el servidor** y **el VPS no construye imágenes**.
El build ocurre en el runner de Actions, se publica en GitHub Container Registry (GHCR)
y el servidor solo hace `pull`.

```
push a main
    │
    ├──▶ ci.yml            checks (django check, migraciones, pytest) + build de validación
    │
    └──▶ deploy.yml
           │
           ├── job build-and-push (runner)
           │     docker build  ──▶  ghcr.io/matt0pena0/ecommerce/web
           │                        tags: latest, sha-<short>
           │
           └── job deploy
                 ├── tailscale: runner se une al tailnet (nodo efímero, tag:ci)
                 ├── SSH a la IP interna del VPS (100.x.y.z) ← sin puertos públicos
                 ├── crea proxy-network si falta
                 ├── clona (1ª vez) o git reset --hard   ← compose, nginx.conf, fixtures
                 ├── valida/escribe .env.prod
                 ├── docker login ghcr.io
                 ├── docker compose pull web
                 ├── docker compose up -d      (SIN --build)
                 └── entrypoint: migrate + collectstatic
```

> El repositorio sigue clonándose en el VPS porque `docker-compose.yml`,
> `nginx/nginx.conf`, `mediafiles/` semilla y `data/backup.json` viven en git.
> Lo que desaparece es la compilación.

### Configuración previa (una sola vez)

**1. Secrets en GitHub** — `Settings → Secrets and variables → Actions`:

| Secret | Descripción |
|--------|-------------|
| `TS_OAUTH_CLIENT_ID` | OAuth client de Tailscale (scope `auth_keys` con escritura) |
| `TS_OAUTH_SECRET` | Secret del OAuth client de Tailscale |
| `VPS_HOST` | **IP de Tailscale del VPS** (`100.x.y.z`) o nombre MagicDNS. No la IP pública. |
| `VPS_USER` | Usuario SSH con permisos sobre Docker |
| `VPS_SSH_KEY` | Clave privada SSH |
| `VPS_DEPLOY_PATH` | Ruta de despliegue en el VPS: `/opt/ecommerce` |
| `VPS_SSH_PORT` | (opcional) puerto SSH, por defecto `22` |
| `ENV_PROD` | (opcional, recomendado) contenido completo de `.env.prod` |
| `GHCR_TOKEN` | (opcional, recomendado) PAT con `read:packages`, para que el VPS pueda hacer `pull` de forma autónoma (p. ej. en un redeploy manual). Si no se define, se usa `GITHUB_TOKEN`, válido solo durante la ejecución del workflow. |

> El workflow requiere `permissions: packages: write` para publicar en GHCR; ya está
> declarado en `deploy.yml`. Verifica también que el repositorio tenga GitHub Packages
> habilitado (`Settings → Actions → Workflow permissions`).

### Acceso a la red privada (Tailscale)

El VPS **no expone SSH a internet**: el acceso es por la VPN de Tailscale, con IP interna
estable (lo que además elimina el problema de las IPs dinámicas). El runner de GitHub no
está en el tailnet por defecto, así que el workflow lo une como **nodo efímero** antes de
hacer SSH:

```yaml
- name: Conectar a Tailscale
  uses: tailscale/github-action@v3
  with:
    oauth-client-id: ${{ secrets.TS_OAUTH_CLIENT_ID }}
    oauth-secret: ${{ secrets.TS_OAUTH_SECRET }}
    tags: tag:ci
```

Configuración necesaria en el panel de Tailscale (una sola vez):

1. **OAuth client** con scope `auth_keys` (escritura). Sus credenciales van a los secrets
   `TS_OAUTH_CLIENT_ID` y `TS_OAUTH_SECRET`.
2. **Tag `tag:ci`** declarado en `tagOwners` de las ACL.
3. **Regla ACL** que permita a `tag:ci` alcanzar el VPS por SSH:

```jsonc
{
  "tagOwners": { "tag:ci": ["autogroup:admin"] },
  "acls": [
    {
      "action": "accept",
      "src": ["tag:ci"],
      "dst": ["tag:vps:22"]   // o el hostname/IP concreta del servidor
    }
  ]
}
```

4. **`VPS_HOST` debe ser la IP de Tailscale** (`100.x.y.z`) o el nombre MagicDNS del
   servidor, **no** la IP pública.

El nodo del runner se desconecta automáticamente al finalizar el job, por lo que no quedan
dispositivos huérfanos en el tailnet.

> Si preferís no gestionar claves SSH, Tailscale SSH permite autenticar por ACL en lugar de
> `VPS_SSH_KEY`. Requiere `--ssh` en el cliente del VPS y una regla `ssh` en las ACL.

**2. Archivo de entorno** — es el único dato que no puede vivir en el repo. Dos opciones:

- **Opción A (recomendada)**: definir el secret `ENV_PROD` con el contenido completo del
  bloque B de `.env.example`. El workflow lo escribe en el servidor en cada deploy
  (con permisos `600`). Cero acceso manual al VPS.
- **Opción B**: crear `/opt/ecommerce/.env.prod` a mano una sola vez. El workflow lo
  detecta y falla con un mensaje claro si falta.

> Al generar la `SECRET_KEY` y los passwords, **no uses el carácter `$`**: Docker Compose
> lo interpreta como interpolación de variable y mutila el valor.

**3. Permisos sobre el directorio base** — el usuario SSH debe poder crear `/opt/ecommerce`:

```bash
sudo mkdir -p /opt/ecommerce && sudo chown "$USER" /opt/ecommerce
```

---

## Primer Despliegue

1. Configura los secrets (paso anterior).
2. Lanza el workflow **Deploy** desde `Actions → Deploy → Run workflow`, marcando
   la casilla **`load_fixtures`** para cargar `data/backup.json` en el arranque inicial.
3. Verifica el log del workflow: debe mostrar la imagen publicada en GHCR, el clone,
   el `docker compose pull`, y `web en ejecución`.

El entrypoint del contenedor `web` ejecuta automáticamente en cada arranque:
1. Espera a que MySQL esté disponible
2. `manage.py migrate --noinput`
3. `manage.py collectstatic --noinput`
4. Arranca Gunicorn (`config.wsgi:application`)

### Carga de datos

`load_fixtures` es **opt-in** y solo debe marcarse en el primer deploy: `loaddata`
sobrescribe registros por PK. Los deploys normales (push a `main`) no lo ejecutan.

> Ver la sección "Consideraciones del fixture" más abajo antes de cargarlo en producción.

### Superusuario

`data/backup.json` ya incluye usuarios (entre ellos un `admin`). **Rota sus contraseñas
inmediatamente después del primer deploy**, porque los hashes provienen de un entorno de
desarrollo:

```bash
# Desde Actions -> Deploy no es interactivo; hacerlo vía SSH puntual:
docker compose exec web python manage.py changepassword admin
```

Si prefieres partir sin esos usuarios, no marques `load_fixtures` y crea el superusuario:

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Consideraciones del fixture (`data/backup.json`)

El respaldo contiene, además de los datos de negocio (99 productos, marcas, órdenes):

| Contenido | Riesgo | Recomendación |
|-----------|--------|---------------|
| 3 usuarios (`admin`, `Cliente1`, `Cliente2`) con hashes de dev | Credenciales débiles en un dominio público | Rotar passwords tras cargar |
| `contenttypes.contenttype` y `auth.permission` (17 + 68 registros) | `migrate` ya los crea; los PKs del fixture pueden colisionar → `IntegrityError` | Filtrar del fixture si `loaddata` falla |
| `sessions.session` (5 registros) | Sesiones obsoletas, inválidas con la nueva `SECRET_KEY` | Filtrar; no aportan nada |
| `admin.logentry` (11 registros) | Historial de admin de otro entorno | Opcional, inofensivo |

Si `loaddata` falla por conflictos de contenttypes, regenera un fixture limpio solo con
datos de negocio:

```bash
docker compose exec web python manage.py dumpdata \
  productos ordenes carrito accounts \
  --natural-foreign --natural-primary \
  --exclude accounts.usuariobase \
  --indent 2 > data/backup_limpio.json
```

---

## Alta del Proxy Host en Nginx Proxy Manager

En el panel de NPM, crear un Proxy Host:

| Campo | Valor |
|-------|-------|
| Domain Names | `ecommerce.themattdev.com`, `www.ecommerce.themattdev.com` |
| Scheme | `http` |
| Forward Hostname / IP | `ecommerce-nginx` |
| Forward Port | `80` |
| Block Common Exploits | activado |
| Websockets Support | no requerido |
| SSL | Request a new Let's Encrypt certificate + Force SSL + HTTP/2 |

> El gateway y `ecommerce-nginx` deben compartir la red `proxy-network` para que NPM
> resuelva el Forward Hostname por nombre de contenedor.

---

## Workflows

| Workflow | Trigger | Qué hace |
|----------|---------|----------|
| `ci.yml` | push / PR a `main` | `manage.py check`, verificación de migraciones, `pytest`, build de validación (sin push) |
| `deploy.yml` | push a `main` o manual | `build-and-push` a GHCR → `deploy` (SSH: pull + `up -d`) |

### Entradas manuales de `deploy.yml`

Desde `Actions → Deploy → Run workflow`:

| Input | Uso |
|-------|-----|
| `load_fixtures` | Carga `data/backup.json`. **Solo primer deploy** (sobrescribe por PK). |
| `skip_build` | Redespliega la imagen `:latest` ya publicada, sin reconstruir. |

### Rollback

Las imágenes se etiquetan también con `sha-<short>`, lo que permite volver atrás sin rebuild:

```bash
cd /opt/ecommerce
WEB_TAG=sha-a1b2c3d docker compose up -d web
```

Para ver los tags disponibles: `Packages` del repositorio en GitHub, o
`docker image ls | grep ecommerce`.

> `WEB_TAG` se resuelve en la **interpolación** de Compose, por lo que debe venir del
> entorno del shell (o de `./.env`), no de `env_file`. Sin definirla, se usa `latest`.

---

## Verificación Post-Deploy

La verificación primaria es el **log del propio workflow**, que termina con `docker compose ps`.
Debe mostrar `ecommerce-db` (healthy), `ecommerce-web` y `ecommerce-nginx` en `Up`.

Comprobación externa (desde cualquier máquina):

```bash
curl -I https://ecommerce.themattdev.com
# Esperado: HTTP/2 200 (y NO un bucle de redirecciones 301)
```

Si necesitas inspección puntual vía SSH:

```bash
cd /opt/ecommerce
docker compose ps
docker compose logs -f web --tail=100
docker network inspect proxy-network | grep ecommerce-nginx
```

---

## Backup de Base de Datos

```bash
# Exportar
docker compose exec -T db mysqldump -u root -p"$DB_ROOT_PASSWORD" "$DB_NAME" > backup_$(date +%F).sql

# Restaurar
docker compose exec -T db mysql -u root -p"$DB_ROOT_PASSWORD" "$DB_NAME" < backup_2026-09-02.sql
```

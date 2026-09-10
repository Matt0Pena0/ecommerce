# Seguridad — Infraestructura Multi-Proyecto

> Consideraciones de seguridad para la arquitectura de despliegue.
> Este documento complementa la `.security-checklist.md` del framework SDD.

---

## 1. Aislamiento de Red

- Cada proyecto tiene su propia red `internal` aislada.
- Solo el nginx de cada proyecto se conecta a `proxy-network`.
- Ningún servicio interno (DB, Cache, Backend) es accesible entre proyectos.
- No publicar puertos de DB/Cache al host en producción.

### Diagrama de Red

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
│  /opt/proxy/           │
│  Nginx Proxy Manager                  │
│  (SSL termination + routing)        │
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
│ Red: internal  │   │ Red: internal  │    ← Redes aisladas
│ - backend      │   │ - backend      │
│ - frontend     │   │ - frontend     │
│ - db           │   │ - db           │
│ - cache        │   │ - cache        │
└────────────────┘   └────────────────┘
```

---

## 2. Contenedores

- Usar usuarios no-root dentro de contenedores (`USER 1000` en Dockerfile).
- Imágenes Alpine donde sea posible (superficie de ataque reducida).
- `restart: unless-stopped` para auto-recuperación.
- Healthchecks en todos los servicios críticos.
- No incluir herramientas de debug en imágenes de producción.
- Multi-stage builds para reducir tamaño de imagen y eliminar dependencias de build.

---

## 3. Credenciales y Secretos

- Un `.env.prod` por proyecto, **nunca versionado en Git**.
- Passwords únicos por proyecto (no reutilizar entre proyectos).
- Cache con autenticación habilitada en producción.
- Base de datos con usuario/password dedicado por proyecto.
- Secret keys generadas con mínimo 32 caracteres aleatorios.
- Rotación periódica de credenciales según política del equipo.

---

## 4. Firewall + Acceso por VPN (Tailscale)

El acceso administrativo (SSH) **no se expone a internet**: viaja por la VPN de Tailscale
con IP interna estable. Solo el tráfico web público llega al host.

```bash
ufw default deny incoming
ufw default allow outgoing

# Tráfico web público (gateway NPM)
ufw allow 80/tcp                    # HTTP
ufw allow 443/tcp                   # HTTPS

# SSH: NO abrir al mundo. Permitir solo por la interfaz de Tailscale.
# OJO: usar el PUERTO REAL de sshd, que NO necesariamente es el 22.
#   Averiguarlo con:  sudo sshd -T | grep '^port'
SSH_PORT="$(sudo sshd -T | awk '/^port /{print $2; exit}')"
ufw allow in on tailscale0 to any port "$SSH_PORT" proto tcp

# Tailscale necesita salida UDP para negociar la conexión directa
ufw allow out 41641/udp

# Panel de administración del gateway: tampoco al mundo.
# Alcanzarlo por la VPN en lugar de publicarlo.
ufw allow in on tailscale0 to any port 81 proto tcp

ufw enable
```

> ### Advertencia — riesgo de perder el acceso al servidor
>
> 1. **Confirmá el puerto real de sshd antes de escribir reglas.** Un `ufw allow ... port 22`
>    cuando sshd escucha en otro puerto te deja fuera al activar el firewall.
> 2. **Verificá que entrás por la IP `100.x.y.z` de Tailscale** antes de cerrar el acceso
>    público.
> 3. Dejá una sesión abierta y usá una red de seguridad mientras aplicás cambios:
>    `sudo shutdown -r +5` (y `sudo shutdown -c` si todo quedó bien).
>
> Nota: el puerto de NPM (81) queda accesible por la VPN. Si `ufw` está inactivo, ese panel
> está **expuesto a internet**; conviene resolverlo antes que después.

### Consecuencia para CI/CD

Como SSH solo es alcanzable desde el tailnet, el workflow de despliegue une al runner de
GitHub a la VPN como nodo efímero antes de conectarse. Ver la sección "Acceso a la red
privada (Tailscale)" en `.infra/DEPLOYMENT.md`.

### Panel del gateway

Con este esquema el panel de NPM (puerto 81) deja de ser público y se alcanza por la VPN,
lo que es preferible a restringirlo por IP de origen.

---

## 5. Actualizaciones

```bash
# Actualizar imágenes base periódicamente
docker compose pull && docker compose up -d

# Limpiar imágenes huérfanas
docker image prune -f

# Verificar vulnerabilidades en imágenes
docker scout cves ecommerce-backend:latest
```

---

## 6. Resumen de Puertos

| Servicio | Puerto Host | Acceso |
|----------|-------------|--------|
| Gateway (HTTP) | 80 | Público |
| Gateway (HTTPS) | 443 | Público |
| Gateway (Admin) | 81 | Solo por VPN (`tailscale0`) |
| SSH | 22 | Solo por VPN (`tailscale0`), no público |
| Proyectos internos | Ninguno | Solo via proxy-network |
| DB/Cache | Ninguno | Solo red interna |

**Regla de oro**: Si un servicio no necesita ser accesible desde internet, NO publica puertos al host.

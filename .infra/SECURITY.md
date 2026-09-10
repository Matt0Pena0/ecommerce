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

## 4. Firewall (Recomendado)

```bash
# Configuración básica — solo tráfico HTTP/S y SSH
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp                    # SSH
ufw allow 80/tcp                    # HTTP (gateway)
ufw allow 443/tcp                   # HTTPS (gateway)
ufw allow 81/tcp  # Panel admin (restringir por IP en producción)
ufw enable
```

> **Recomendación**: Restringir el acceso al panel de administración del gateway
> por IP de origen en producción.

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
| Gateway (Admin) | 81 | Restringir por IP |
| Proyectos internos | Ninguno | Solo via proxy-network |
| DB/Cache | Ninguno | Solo red interna |

**Regla de oro**: Si un servicio no necesita ser accesible desde internet, NO publica puertos al host.

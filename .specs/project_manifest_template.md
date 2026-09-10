# Manifiesto del Proyecto — {{PROJECT_NAME}}

> **Fuente única de verdad** del proyecto. Todos los agentes deben consultar este archivo
> antes de tomar decisiones de arquitectura, implementación o planificación.

---

## 1. Project Identity

* **Name:** {{PROJECT_NAME}}
* **Core Purpose:** {{PROJECT_PURPOSE}}
* **Technology Stack:**
    * **Backend:** {{BACKEND_FRAMEWORK}} ({{BACKEND_LANGUAGE}})
    * **Frontend:** {{FRONTEND_FRAMEWORK}}
    * **Database:** {{DATABASE}}
    * **Cache/Broker:** {{CACHE_BROKER}}
    * **Infrastructure:** {{CONTAINER_TOOL}}
    * **Gateway:** {{GATEWAY}} ({{PROXY_MANAGER}})
    * **Deployment:** Arquitectura multi-proyecto con gateway centralizado (ver `.infra/README.md`)

---

## 2. Architecture Blueprint

* **Topology:** {{TOPOLOGY_DESCRIPTION}}
* **Layers:** {{LAYER_DESCRIPTIONS}}

### Diagrama de Alto Nivel

```
{{ARCHITECTURE_DIAGRAM}}
```

---

## 3. Directory Standard

```
{{DIRECTORY_TREE}}
```

---

## 4. Agent Roster & Scope

| Agente | Rol | Dominio (Scope) | Zonas Prohibidas |
|--------|-----|-----------------|------------------|
| @Orchestrator_Agent | {{ORCHESTRATOR_ROLE}} | {{ORCHESTRATOR_SCOPE}} | {{ORCHESTRATOR_FORBIDDEN}} |
| @Architect_Agent | {{ARCHITECT_ROLE}} | {{ARCHITECT_SCOPE}} | {{ARCHITECT_FORBIDDEN}} |
| @Backend_Agent | {{BACKEND_ROLE}} | {{BACKEND_SCOPE}} | {{BACKEND_FORBIDDEN}} |
| @Frontend_Agent | {{FRONTEND_ROLE}} | {{FRONTEND_SCOPE}} | {{FRONTEND_FORBIDDEN}} |
| @DevOps_Agent | {{DEVOPS_ROLE}} | {{DEVOPS_SCOPE}} | {{DEVOPS_FORBIDDEN}} |
| @Tester_Agent | {{TESTER_ROLE}} | {{TESTER_SCOPE}} | {{TESTER_FORBIDDEN}} |
| @Docs_Agent | {{DOCS_ROLE}} | {{DOCS_SCOPE}} | {{DOCS_FORBIDDEN}} |

---

## 5. State & Task Tracking

| Feature ID | Componente | Descripción | Estado |
|------------|-----------|-------------|--------|
| {{FEAT_ID}} | {{COMPONENT}} | {{DESCRIPTION}} | PENDING |

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

{{NAMING_CONVENTIONS}}

### Git Workflow

{{GIT_WORKFLOW}}

### Manejo de Errores

{{ERROR_HANDLING_STANDARDS}}

---

## 7. Infraestructura y Despliegue

### Configuración del Servidor

| Parámetro | Valor |
|-----------|-------|
| **Ruta base en servidor** | `{{VPS_BASE_PATH}}` |
| **Slug del proyecto** | `{{PROJECT_SLUG}}` |
| **Dominio** | `{{DOMAIN}}` |
| **Gateway central** | {{PROXY_MANAGER}} (`{{PROXY_MANAGER_IMAGE}}`) |
| **Red del proxy** | `{{PROXY_NETWORK}}` (estándar: `proxy-network`) |
| **Registry de imágenes** | `{{IMAGE_REGISTRY}}` (ej. `ghcr.io/owner/repo/web`) |
| **Rama de despliegue** | `{{DEPLOY_BRANCH}}` |

### Servicios

| Servicio | Imagen | Puerto Interno |
|----------|--------|----------------|
| Base de datos | `{{DB_IMAGE}}` | `{{DB_PORT}}` |
| Cache | `{{CACHE_IMAGE}}` | — |
| Backend | Build local | `{{BACKEND_PORT}}` |
| Frontend | Build local | `{{FRONTEND_PORT}}` |
| Nginx interno | `nginx:alpine` | `80` |

### Plantillas de Referencia

Las plantillas de infraestructura viven en `.infra/` y se adaptan al instanciar el proyecto.
Consultar `.infra/README.md` para la guía completa de despliegue.

---

## 8. Protocolo de Ejecución de Funcionalidades

Toda nueva funcionalidad sigue el Ciclo SDD de 6 fases:

1. **Draft** — Se redacta el `.spec.md` de la feature en `.specs/features/`
2. **Plan** — @Orchestrator_Agent genera el Action Plan en `.specs/tasks/`
3. **Audit** — @Architect_Agent revisa y aprueba (o veta) el plan
4. **Dev** — Agentes especialistas implementan según el plan aprobado
5. **Test** — @Tester_Agent valida contra los criterios de aceptación del spec
6. **Done** — @Orchestrator_Agent actualiza este manifiesto (Sección 5)

> **Regla fundamental:** Ningún agente escribe código de producción sin un `.spec.md` aprobado.

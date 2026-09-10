# Protocolo de Handoffs — Ecommerce

## Propósito

El sistema de handoffs es el mecanismo formal de comunicación entre agentes IA dentro de la metodología SDD (Spec Driven Development). Cada handoff es un documento Markdown que transfiere contexto, tareas o reportes de estado entre agentes, garantizando trazabilidad completa de todas las acciones del proyecto.

**Principio fundamental:** Sin handoff = trabajo no registrado. El @Orchestrator_Agent no puede actualizar el manifiesto ni delegar la siguiente tarea si no recibe un handoff del agente ejecutor.

---

## Estructura de Archivos

```
.context/handoffs/
├── README.md              ← Este archivo (protocolo documentado)
├── _template.md           ← Plantilla base para crear nuevos handoffs
├── active/                ← Handoffs en proceso (agente trabajando)
│   └── .gitkeep
├── inbox/                 ← Handoffs pendientes de ser procesados por el receptor
│   └── .gitkeep
└── completed/             ← Handoffs finalizados (archivo histórico)
    └── .gitkeep
```

---

## Ciclo de Vida de un Handoff

Un handoff atraviesa las siguientes fases:

```
1. Creado       → El agente emisor genera el handoff usando _template.md
2. active/      → Se deposita en active/ mientras el emisor lo prepara
3. inbox/       → El @Orchestrator_Agent lo mueve al inbox/ del agente receptor
4. active/      → El receptor lo mueve a active/ al comenzar a procesarlo
5. completed/   → Al finalizar la acción, se archiva en completed/
```

### Flujos Especiales

- **BLOCKER**: Si el receptor encuentra un impedimento, emite un nuevo handoff de tipo BLOCKER hacia @Orchestrator_Agent. El handoff original permanece en `active/` hasta que se resuelva el bloqueo.
- **VETO**: El @Architect_Agent puede emitir un VETO que devuelve el handoff al @Orchestrator_Agent con justificación técnica. El plan debe ser revisado antes de re-delegar.
- **ACK**: El @Orchestrator_Agent confirma recepción de un COMPLETION o BLOCKER.

---

## Convenciones de Nomenclatura

### Formato del Nombre de Archivo

```
HANDOFF-{NNN}-{TIPO}-{EMISOR}-a-{RECEPTOR}.md
```

### Ejemplos

| Archivo | Descripción |
|---------|-------------|
| `HANDOFF-001-DELEGACION-orchestrator-a-backend.md` | Delegación de tarea al Backend |
| `HANDOFF-002-COMPLETION-backend-a-orchestrator.md` | Reporte de tarea completada |
| `HANDOFF-003-BLOCKER-frontend-a-orchestrator.md` | Impedimento reportado |
| `HANDOFF-004-VETO-architect-a-orchestrator.md` | Rechazo de plan con justificación |
| `HANDOFF-005-ACK-orchestrator-a-backend.md` | Confirmación de recepción |

### Reglas

- El `{NNN}` es un número secuencial global (no por agente).
- El `{TIPO}` corresponde a uno de los 5 tipos definidos abajo.
- Los nombres de agente usan formato kebab-case sin el sufijo `_Agent`.

---

## Campos Obligatorios

Todo handoff DEBE contener los siguientes campos en su cabecera:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| **ID** | String | Identificador único: `HANDOFF-{NNN}` |
| **De** | String | Agente emisor: `@{Rol}_Agent` |
| **Para** | String | Agente receptor: `@{Rol}_Agent` |
| **Fecha** | Date | Fecha de emisión (formato ISO: `YYYY-MM-DD`) |
| **Tipo** | Enum | Uno de: DELEGACION, COMPLETION, BLOCKER, VETO, ACK |
| **Feature** | String | Feature ID asociado (e.g., `FEAT-001`) |
| **Estado** | Enum | PENDING, IN_PROGRESS, DONE, BLOCKED, NEEDS_REVIEW |

### Secciones Obligatorias del Cuerpo

| Sección | Descripción |
|---------|-------------|
| **Misión / Mensaje** | Descripción clara de la tarea o mensaje |
| **Contexto Mínimo** | Archivos que el receptor DEBE leer antes de actuar |
| **Entregables Esperados** | Resultados concretos que se esperan del receptor |
| **Reporte de Vuelta** | Instrucciones para el handoff de respuesta |
| **Historial** | Registro cronológico de acciones sobre este handoff |

### Secciones Opcionales

| Sección | Descripción |
|---------|-------------|
| **Archivos Prohibidos** | Archivos fuera del dominio del receptor (no leer/modificar) |
| **Restricciones** | Limitaciones adicionales para la ejecución |

---

## Tipos de Handoff

| Tipo | Emisor | Receptor | Propósito |
|------|--------|----------|-----------|
| **DELEGACION** | @Orchestrator_Agent | Cualquier agente | Asignar una tarea específica con contexto y entregables |
| **COMPLETION** | Cualquier agente | @Orchestrator_Agent | Reportar tarea completada con resumen y archivos modificados |
| **BLOCKER** | Cualquier agente | @Orchestrator_Agent | Reportar impedimento que bloquea la ejecución |
| **VETO** | @Architect_Agent | @Orchestrator_Agent | Rechazar un plan o diseño con justificación técnica |
| **ACK** | @Orchestrator_Agent | Cualquier agente | Confirmar recepción de un handoff previo |

### Cuándo Usar Cada Tipo

- **DELEGACION**: El @Orchestrator_Agent ha generado un Action Plan y necesita asignar subtareas a agentes especializados.
- **COMPLETION**: Un agente terminó su trabajo y necesita que el @Orchestrator_Agent actualice el manifiesto y delegue la siguiente tarea.
- **BLOCKER**: Un agente no puede continuar por una dependencia faltante, error de configuración, o conflicto con otro dominio.
- **VETO**: El @Architect_Agent detecta que un plan viola el manifiesto, introduce deuda técnica inaceptable, o rompe contratos de API.
- **ACK**: El @Orchestrator_Agent confirma que recibió y procesó un COMPLETION o BLOCKER.

---

## Regla Crítica para Todos los Agentes

> **OBLIGACIÓN DE HANDOFF**: Al completar CUALQUIER acción (implementación, revisión,
> corrección, documentación), todo agente DEBE emitir un handoff de tipo COMPLETION
> dirigido a @Orchestrator_Agent. Sin este handoff, el trabajo no se registra en el
> manifiesto del proyecto y la siguiente tarea no puede ser delegada.

---

## Referencia

- Plantilla de handoff: `.context/handoffs/_template.md`
- Manifiesto del proyecto: `.specs/project_manifest_template.md`
- Configuración de agentes: `.config/agents.json`

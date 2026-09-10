# HANDOFF-{{ID}}

| Campo | Valor |
|-------|-------|
| **ID** | HANDOFF-{{ID}} |
| **De** | @{{SENDER}}_Agent |
| **Para** | @{{RECEIVER}}_Agent |
| **Fecha** | {{DATE}} |
| **Tipo** | {{TYPE}} |
| **Feature** | {{FEAT_ID}} |
| **Estado** | {{STATUS}} |

---

## Misión / Mensaje

{{MISSION_DESCRIPTION}}

---

## Contexto Mínimo

Archivos que el receptor DEBE leer antes de actuar:

- {{CONTEXT_FILE_1}}
- {{CONTEXT_FILE_2}}

---

## Archivos Prohibidos

NO leer ni modificar estos archivos (fuera de tu dominio):

- {{FORBIDDEN_FILE_1}}
- {{FORBIDDEN_FILE_2}}

---

## Entregables Esperados

- {{DELIVERABLE_1}}
- {{DELIVERABLE_2}}

---

## Restricciones

- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

---

## Reporte de Vuelta

Al completar, emitir HANDOFF de tipo COMPLETION a @Orchestrator_Agent con:

- **Resumen**: Qué se hizo exactamente
- **Archivos creados/modificados**: Lista completa
- **Estado resultante**: DONE | BLOCKED | NEEDS_REVIEW

---

## Historial

| Fecha | Agente | Acción |
|-------|--------|--------|
| {{DATE}} | @{{AGENT}}_Agent | {{ACTION}} |

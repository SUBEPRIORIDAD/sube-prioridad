# Decisiones de Arquitectura — SUBE Prioridad

## 1. Propósito del documento

Este documento registra las principales decisiones de arquitectura adoptadas para el desarrollo conceptual y técnico de SUBE Prioridad.

Su finalidad es explicar por qué el proyecto se estructura como una arquitectura modular, gradual, interoperable, prudente y respetuosa de la privacidad.

Las decisiones aquí descriptas no constituyen una especificación definitiva ni una obligación de implementación. Funcionan como criterios de diseño para orientar la evolución del MVP, la documentación técnica y eventuales pruebas piloto.

---

## 2. Decisión 1 — Atributo técnico de prioridad en lugar de diagnóstico médico

### Decisión

El core del sistema no debe procesar diagnósticos médicos, historia clínica ni información sanitaria identificable.

El modelo correcto es:

```text
persona habilitada -> atributo técnico de prioridad -> preferencia de asistencia

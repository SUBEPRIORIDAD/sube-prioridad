# Mapa Técnico de Módulos — SUBE Prioridad

## 1. Objetivo del documento

Este documento explica la función de cada módulo Python del repositorio SUBE Prioridad.

Su finalidad es que cualquier persona pueda entender la arquitectura técnica sin tener que leer todo el código fuente.

El proyecto está organizado en módulos separados para evitar mezclar:

- validación;
- preferencias;
- alertas;
- sincronización;
- antifraude;
- ventanas temporales;
- Bono Solidario;
- acumulación demo;
- flujo end-to-end;
- API.

La separación por módulos permite evolucionar el MVP gradualmente.

## 2. Regla general de arquitectura

Todos los módulos del repositorio mantienen estos límites:

- No integran SUBE real.
- No integran Red SUBE real.
- No consultan tarjetas reales.
- No consultan cuentas reales.
- No consultan validadores reales.
- No consultan molinetes reales.
- No aplican beneficios reales.
- No modifican saldo real.
- No aplican tarifa real.
- No escriben chips reales.
- No usan DNI.
- No usan diagnóstico.
- No usan CUD visible.
- No usan historia clínica.
- No usan certificado médico.
- No usan GPS exacto.
- No generan ranking.
- No generan sanciones.
- No imponen obligaciones nuevas a choferes o personal operativo.

## 3. Vista general del flujo

```text
Cuenta / Preferencias
        ↓
Atributo SUBE Prioridad demo
        ↓
Validación paga demo
        ↓
Alerta posterior a validación
        ↓
Sincronización solidaria
        ↓
Filtros antifraude
        ↓
Selección de canal
        ↓
Opción MVP de Bono Solidario
        ↓
Acumulación demo
        ↓
Próximo viaje elegible
        ↓
Orquestador end-to-end

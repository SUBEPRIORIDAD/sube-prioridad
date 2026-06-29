# SUBE Prioridad — Guardrails de Arquitectura

## 1. Naturaleza del MVP

Este repositorio representa un MVP técnico, conceptual y demostrativo del Programa SUBE Prioridad.

El código no debe interpretarse como una implementación definitiva, obligatoria ni cerrada del sistema. Su finalidad es ilustrar una arquitectura posible, modular y auditable, sujeta a evaluación técnica, jurídica, presupuestaria y operativa por parte de las autoridades competentes.

## 2. Principios que el código no debe vulnerar

Toda modificación del repositorio deberá respetar los siguientes principios:

- Accesibilidad universal.
- Autonomía personal del usuario.
- Protección de datos personales.
- Minimización de datos.
- Asistencia preventiva.
- No exposición pública de diagnósticos.
- No creación de privilegios.
- No sustitución de derechos ya reconocidos.
- No imposición de nuevas cargas operativas al chofer.
- No generación de sanciones automáticas a pasajeros.
- No alteración de la recaudación del sistema SUBE.
- Implementación progresiva, modular y reversible.

## 3. Datos prohibidos en el core del MVP

El core técnico no debe procesar ni almacenar:

- DNI.
- Nombre y apellido.
- Domicilio.
- Historia clínica.
- Diagnóstico médico específico.
- Certificados médicos en texto plano.
- Información sensible innecesaria.
- Identidad real de pasajeros colaboradores.

El MVP debe trabajar con tokens, hashes, atributos técnicos o identificadores pseudoanonimizados.

## 4. Modelo correcto de atributo prioritario

El sistema no debe clasificar personas por enfermedad, condición o diagnóstico.

El modelo correcto es:

```text
usuario habilitado -> atributo técnico de prioridad -> preferencia de asistencia
## 5. Interoperabilidad

Toda integración con organismos, registros o plataformas externas debe tratarse como simulada salvo que exista convenio, API real, documentación técnica y autorización formal.

Por eso, los módulos como `xroad_gateway.py` deben mantenerse como simuladores o adaptadores desacoplados.

No se debe afirmar conexión real con ANDIS, SISA, RENAPER, Mi Argentina, Nación Servicios S.A. u otros organismos si esa conexión no existe técnicamente.

## 6. Bono Solidario

El Bono Solidario debe entenderse como una hipótesis futura de reconocimiento ciudadano voluntario.

No debe implementarse como:

- multa;
- castigo;
- obligación;
- ranking público;
- sistema de vigilancia;
- mecanismo de presión social;
- beneficio por ocupar o liberar asientos prioritarios legales.

En el MVP, cualquier lógica de reconocimiento debe limitarse a eventos técnicos pseudoanonimizados y a situaciones voluntarias sobre asientos de uso general.

## 7. Separación entre documentación, simulación y producción

El repositorio debe distinguir claramente entre:

- documentación conceptual;
- simuladores;
- tests;
- API MVP;
- módulos futuros;
- integraciones reales aún no implementadas.

Todo archivo que simule una integración debe indicarlo expresamente en su nombre, docstring o comentario principal.

## 8. Regla de cambios seguros

Antes de incorporar nuevas funciones, cualquier cambio debe cumplir:

```bash
python -m py_compile main.py validator.py cache_manager.py circuit_breaker.py xroad_gateway.py
pytest -q
````

Ejemplo conceptual:

```json
{
  "atributo_prioridad_activo": true,
  "perfil_alertas_ux": 2,
  "fecha_caducidad": "2026-12-31T00:00:00Z"
}
````

## 5. Interoperabilidad

Toda integración con organismos, registros o plataformas externas debe tratarse como simulada salvo que exista convenio, API real, documentación técnica y autorización formal.

Por eso, los módulos como `xroad_gateway.py` deben mantenerse como simuladores o adaptadores desacoplados.

No se debe afirmar conexión real con ANDIS, SISA, RENAPER, Mi Argentina, Nación Servicios S.A. u otros organismos si esa conexión no existe técnicamente.

## 6. Bono Solidario

El Bono Solidario debe entenderse como una hipótesis futura de reconocimiento ciudadano voluntario.

No debe implementarse como:

* multa;
* castigo;
* obligación;
* ranking público;
* sistema de vigilancia;
* mecanismo de presión social;
* beneficio por ocupar o liberar asientos prioritarios legales.

En el MVP, cualquier lógica de reconocimiento debe limitarse a eventos técnicos pseudoanonimizados y a situaciones voluntarias sobre asientos de uso general.

## 7. Separación entre documentación, simulación y producción

El repositorio debe distinguir claramente entre:

* documentación conceptual;
* simuladores;
* tests;
* API MVP;
* módulos futuros;
* integraciones reales aún no implementadas.

Todo archivo que simule una integración debe indicarlo expresamente en su nombre, docstring o comentario principal.

## 8. Regla de cambios seguros

Antes de incorporar nuevas funciones, cualquier cambio debe cumplir:

```bash
python -m py_compile main.py validator.py cache_manager.py circuit_breaker.py xroad_gateway.py
pytest -q
```

Si el cambio rompe compilación o tests, no debe mergearse a `main`.

## 9. Criterio de mínima intervención

Cuando se corrija código existente, debe preferirse:

1. corregir sintaxis;
2. preservar nombres de módulos;
3. mantener la intención funcional original;
4. agregar tests;
5. evitar reescrituras innecesarias;
6. documentar toda simulación;
7. evitar afirmaciones técnicas no verificadas.

## 10. Declaración final

SUBE Prioridad debe evolucionar como una propuesta de innovación pública abierta, prudente, auditable y compatible con la infraestructura existente, sin comprometer datos sensibles ni imponer una solución técnica única.


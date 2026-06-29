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

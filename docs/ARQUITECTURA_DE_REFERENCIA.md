# Arquitectura de Referencia — SUBE Prioridad

## 1. Propósito del documento

Este documento describe la arquitectura de referencia del Programa SUBE Prioridad.

No constituye una especificación obligatoria, una implementación definitiva ni una solución tecnológica única.

Su objetivo es documentar una arquitectura conceptual, modular y escalable que pueda servir como referencia para el diseño, evaluación e implementación progresiva de soluciones de asistencia preventiva en sistemas de transporte público.

Todas las implementaciones deberán adecuarse a la normativa vigente, a la infraestructura disponible y a las decisiones de las autoridades competentes.

---

# 2. Visión

SUBE Prioridad propone una arquitectura abierta para facilitar la asistencia preventiva a personas que, por una necesidad acreditada, requieren viajar sentadas durante un trayecto.

La arquitectura prioriza:

- privacidad por diseño;
- accesibilidad universal;
- interoperabilidad;
- modularidad;
- neutralidad tecnológica;
- mínima intervención sobre la infraestructura existente;
- implementación gradual;
- escalabilidad.

La arquitectura no presupone una tecnología única, un proveedor específico ni una plataforma determinada.

---

# 3. Principios de diseño

La arquitectura se basa en los siguientes principios.

## Privacidad por diseño

El núcleo técnico no procesa información médica identificable.

Debe trabajar exclusivamente con atributos técnicos, tokens, hashes o identificadores pseudoanonimizados.

---

## Minimización de datos

Solo deben procesarse los datos estrictamente necesarios para verificar un atributo de prioridad.

No forman parte del core:

- DNI;
- nombre;
- apellido;
- domicilio;
- historia clínica;
- diagnóstico médico;
- certificados médicos en texto plano.

---

## Separación de responsabilidades

La arquitectura distingue claramente entre:

- acreditación de la necesidad de asistencia;
- validación técnica del atributo;
- operación del transporte;
- experiencia del usuario;
- analítica del sistema.

Cada componente puede evolucionar de forma independiente.

---

## Neutralidad tecnológica

La arquitectura no depende de:

- una marca de validadores;
- una tecnología NFC específica;
- una tarjeta determinada;
- una aplicación móvil concreta;
- un proveedor de identidad digital;
- un sistema operativo.

Las implementaciones podrán adaptarse a distintas infraestructuras.

---

## Reutilización de infraestructura

Siempre que resulte técnica y jurídicamente viable, deberán reutilizarse los componentes existentes del ecosistema de transporte.

La arquitectura procura minimizar modificaciones físicas y operativas.

---

## Escalabilidad

La arquitectura está diseñada para evolucionar mediante etapas sucesivas sin requerir rediseños completos del sistema.

---

# 4. Arquitectura conceptual

La arquitectura puede representarse mediante capas independientes.

```text
Usuarios

↓

Atributo técnico de prioridad

↓

Validación pseudoanonimizada

↓

Motor de reglas

↓

Experiencia de asistencia

↓

Infraestructura de transporte
```

Cada capa puede modificarse sin afectar necesariamente a las restantes.

---

# 5. Interoperabilidad

La arquitectura contempla la posibilidad de interoperar con organismos, registros o plataformas externas cuando exista:

- marco jurídico;
- autorización correspondiente;
- documentación técnica;
- interfaces compatibles.

En el MVP del repositorio, todas las integraciones se consideran simuladas.

La arquitectura no implica la existencia de conexiones reales con organismos públicos.

---

# 6. Implementación progresiva

La arquitectura fue concebida para permitir una evolución gradual.

Una posible secuencia de implementación podría comprender:

1. MVP conceptual.
2. Laboratorio técnico.
3. Prueba piloto.
4. Piloto ampliado.
5. Implementación regional.
6. Implementación nacional.
7. Adaptaciones internacionales.

Cada etapa deberá ser evaluada antes de avanzar hacia la siguiente.

---

# 7. Adaptabilidad

La arquitectura procura ser independiente del contexto normativo específico de un país.

Los principios técnicos pueden adaptarse a:

- distintos sistemas tarifarios;
- diferentes medios de validación;
- modelos de identidad digital;
- marcos regulatorios diversos;
- infraestructuras de transporte heterogéneas.

---

# 8. Gobernanza

La evolución de la arquitectura debe preservar:

- transparencia;
- auditabilidad;
- protección de datos;
- accesibilidad;
- reversibilidad;
- trazabilidad técnica;
- participación institucional.

---

# 9. Estado del repositorio

El presente repositorio implementa únicamente un MVP conceptual.

No representa una implementación productiva.

No modifica derechos vigentes.

No sustituye competencias de organismos públicos.

No establece integraciones reales con plataformas externas.

---

# 10. Declaración final

La Arquitectura de Referencia de SUBE Prioridad constituye una propuesta abierta de innovación pública orientada a facilitar la asistencia preventiva en el transporte, mediante una evolución gradual, modular y respetuosa de la privacidad, procurando su adaptación a diferentes contextos tecnológicos, institucionales y regulatorios.

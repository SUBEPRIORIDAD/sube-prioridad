# Roadmap de Implementación — SUBE Prioridad

## 1. Propósito del documento

Este documento describe una hoja de ruta conceptual para la evolución progresiva de SUBE Prioridad.

No constituye un cronograma obligatorio, una decisión estatal de implementación ni una especificación definitiva.

Su finalidad es ordenar posibles etapas de desarrollo, validación, prueba piloto, ampliación y adaptación institucional de la arquitectura del proyecto.

Toda implementación real deberá quedar sujeta a evaluación técnica, jurídica, presupuestaria, operativa y social por parte de las autoridades competentes.

---

## 2. Principio general de evolución progresiva

SUBE Prioridad fue concebido como una arquitectura gradual.

La propuesta no requiere que todas sus funcionalidades sean desarrolladas simultáneamente.

Por el contrario, permite comenzar con componentes simples, seguros y compatibles con infraestructura existente, para luego incorporar nuevas capacidades de manera progresiva, reversible y auditable.

La evolución del proyecto debe respetar los siguientes criterios:

- comenzar con alcance limitado;
- validar hipótesis operativas;
- medir resultados;
- proteger datos personales;
- evitar cargas indebidas al personal de transporte;
- preservar derechos vigentes;
- no alterar el régimen legal de asientos prioritarios;
- no afirmar integraciones reales sin autorización;
- permitir correcciones antes de escalar.

---

## 3. Fase 0 — Investigación, documentación y arquitectura

### Objetivo

Consolidar la base conceptual, institucional, jurídica, operativa y técnica del proyecto.

### Componentes

- Documentación del problema público.
- Fundamentos jurídicos, sociales, médicos y tecnológicos.
- Arquitectura de referencia.
- Guardrails de privacidad y gobernanza.
- Pliego técnico extendido.
- MVP demostrativo en repositorio público.

### Resultado esperado

Una propuesta suficientemente clara para ser evaluada por equipos técnicos, organismos públicos, universidades, operadores de transporte o áreas de innovación pública.

---

## 4. Fase 1 — MVP conceptual y técnico

### Objetivo

Demostrar la viabilidad básica de algunos componentes centrales del sistema sin procesar datos sensibles ni integrarse a sistemas reales.

### Componentes actuales del repositorio

- API demostrativa.
- Validación pseudoanonimizada por hash.
- Endpoint de salud.
- Principios de guardrails.
- Simulador de interoperabilidad.
- Motor antifraude inicial.
- Tests básicos.
- Integración continua.

### Alcance

Esta fase no representa producción.

No conecta con organismos reales.

No modifica el sistema SUBE.

No altera la operación del transporte.

No procesa DNI, nombre, diagnóstico ni historia clínica.

### Resultado esperado

Validar que el modelo técnico puede expresarse como una arquitectura modular, testeable y extensible.

---

## 5. Fase 2 — Laboratorio técnico controlado

### Objetivo

Probar el comportamiento del sistema en un entorno cerrado, sin impacto sobre usuarios reales ni servicios productivos.

### Actividades posibles

- Simulación de eventos de validación.
- Pruebas de latencia.
- Pruebas de perfiles de asistencia.
- Evaluación de UX.
- Pruebas de privacidad.
- Pruebas de seguridad lógica.
- Evaluación de interoperabilidad simulada.
- Validación de reglas antifraude.

### Resultado esperado

Identificar riesgos, ajustes técnicos y requerimientos mínimos antes de cualquier prueba en campo.

---

## 6. Fase 3 — Prueba piloto limitada

### Objetivo

Evaluar la arquitectura en condiciones reales acotadas.

### Alcance sugerido

- Una o pocas líneas de colectivo.
- Un operador o ámbito territorial limitado.
- Usuarios voluntarios previamente habilitados.
- Monitoreo institucional.
- Evaluación técnica y social.
- Métricas claras de resultado.

### Criterios de diseño

La prueba piloto debe:

- ser reversible;
- tener alcance temporal definido;
- no alterar derechos vigentes;
- no imponer nuevas cargas al chofer;
- no exponer diagnósticos;
- no utilizar datos personales innecesarios;
- contar con consentimiento y canales alternativos;
- ser evaluada antes de cualquier ampliación.

### Resultado esperado

Obtener evidencia inicial sobre funcionamiento, aceptación, riesgos, beneficios y ajustes necesarios.

---

## 7. Fase 4 — Piloto ampliado

### Objetivo

Extender la experiencia a más líneas, operadores o zonas, incorporando mejoras derivadas de la prueba inicial.

### Componentes posibles

- Mayor cantidad de usuarios.
- Mayor diversidad de recorridos.
- Ajuste de perfiles de asistencia.
- Monitoreo de indicadores.
- Evaluación de accesibilidad.
- Mejoras en experiencia de usuario.
- Revisión de reglas antifraude.
- Evaluación de interoperabilidad institucional.

### Resultado esperado

Validar si la arquitectura puede sostenerse en escenarios más diversos sin perder privacidad, simplicidad ni control operativo.

---

## 8. Fase 5 — Implementación regional

### Objetivo

Evaluar una implementación de escala intermedia, por ciudad, municipio, corredor, provincia o región metropolitana.

### Requisitos previos

Antes de esta etapa deberían existir:

- resultados positivos de pilotos anteriores;
- marco institucional claro;
- evaluación presupuestaria;
- documentación técnica;
- protocolos de protección de datos;
- mecanismos de auditoría;
- canales de reclamo;
- planes de capacitación;
- definición de autoridad responsable.

### Resultado esperado

Determinar si la arquitectura puede integrarse progresivamente en una política pública de mayor alcance.

---

## 9. Fase 6 — Implementación nacional

### Objetivo

Analizar la eventual expansión nacional de SUBE Prioridad, siempre que las etapas anteriores hayan demostrado factibilidad, utilidad pública y sustentabilidad.

### Condiciones necesarias

- decisión institucional expresa;
- marco normativo adecuado;
- interoperabilidad autorizada;
- gobernanza clara;
- infraestructura validada;
- protección de datos auditada;
- evaluación de impacto;
- sostenibilidad técnica y presupuestaria;
- compatibilidad con operadores y jurisdicciones.

### Resultado esperado

Transformar una arquitectura probada en una herramienta pública escalable, manteniendo sus principios de privacidad, accesibilidad, gradualidad y neutralidad tecnológica.

---

## 10. Fase 7 — Modelo adaptable a otras jurisdicciones

### Objetivo

Documentar los principios reutilizables de la arquitectura para que puedan servir como referencia en otros sistemas de transporte, regiones o países.

### Enfoque

No se propone exportar una implementación cerrada.

Se propone documentar un modelo adaptable basado en:

- asistencia preventiva;
- atributo técnico de prioridad;
- minimización de datos;
- interoperabilidad responsable;
- neutralidad tecnológica;
- validación progresiva;
- gobernanza pública;
- evaluación contextual.

### Resultado esperado

Permitir que otras jurisdicciones estudien, adapten o reinterpreten la arquitectura conforme a sus propias normas, infraestructuras y políticas públicas.

---

## 11. Indicadores de evaluación

Cada etapa debería contar con indicadores propios.

Algunos indicadores posibles:

- cantidad de usuarios voluntarios;
- nivel de aceptación;
- tiempos de respuesta del sistema;
- percepción de privacidad;
- reducción de conflictos;
- facilidad de uso;
- accesibilidad cognitiva;
- cantidad de eventos válidos;
- reportes de errores;
- reclamos recibidos;
- incidentes de privacidad;
- intentos de fraude detectados;
- satisfacción de usuarios prioritarios;
- opinión de operadores y personal técnico.

Estos indicadores deberán definirse de manera precisa antes de cada etapa.

---

## 12. Criterios de avance entre fases

Ninguna fase debería avanzar automáticamente a la siguiente.

El avance debe depender de:

- resultados técnicos;
- evaluación jurídica;
- aceptación social;
- protección de datos;
- sostenibilidad operativa;
- factibilidad presupuestaria;
- ausencia de impactos negativos relevantes;
- decisión de las autoridades competentes.

---

## 13. Criterios de pausa o reversión

La arquitectura debe permitir detener, pausar, modificar o revertir una implementación cuando existan riesgos o resultados no deseados.

Causales posibles:

- afectación de privacidad;
- complejidad operativa excesiva;
- rechazo social significativo;
- falta de accesibilidad;
- aumento de conflictos;
- fallas técnicas relevantes;
- ausencia de autorización institucional;
- costos no sostenibles;
- problemas de seguridad o fraude.

---

## 14. Relación con el Bono Solidario

El Bono Solidario no forma parte de la implementación inicial necesaria de SUBE Prioridad.

Debe entenderse como una posible evolución futura, voluntaria y sujeta a validaciones técnicas adicionales.

Su eventual desarrollo requeriría:

- funcionamiento estable del sistema base;
- reglas antifraude;
- evidencia verificable;
- evaluación de impacto;
- autorización institucional;
- límites claros respecto de asientos prioritarios legales;
- mecanismos que eviten presión social, sanciones o rankings públicos.

---

## 15. Declaración final

El roadmap de implementación de SUBE Prioridad debe entenderse como una guía conceptual de evolución gradual.

Su valor no reside en imponer una secuencia rígida, sino en demostrar que la arquitectura puede crecer de manera ordenada, prudente, reversible y auditable.

La finalidad última es permitir que una propuesta ciudadana de innovación pública pueda ser evaluada, probada, mejorada y eventualmente adaptada a distintas escalas, siempre con respeto por la privacidad, la accesibilidad, la dignidad de las personas y las competencias de las autoridades públicas.

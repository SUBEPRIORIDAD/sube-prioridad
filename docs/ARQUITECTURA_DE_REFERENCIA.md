# Arquitectura de Referencia — SUBE Prioridad

## 1. Propósito del documento

El presente documento describe la arquitectura conceptual de referencia de **SUBE Prioridad**.

Su finalidad es ordenar, desde una perspectiva técnica e institucional, cómo podría estructurarse una herramienta de asistencia preventiva en el transporte público basada en atributos técnicos de prioridad, privacidad por diseño, minimización de datos, interoperabilidad responsable, gradualidad y evaluación institucional.

Este documento no constituye una arquitectura productiva definitiva, una especificación obligatoria, una contratación tecnológica ni una integración real actualmente vigente.

Toda implementación real deberá ser evaluada, adaptada, autorizada y supervisada por las autoridades competentes.

---

## 2. Naturaleza de la arquitectura

SUBE Prioridad debe entenderse como una **arquitectura de referencia conceptual**.

Esto significa que propone principios, componentes, flujos y límites que podrían orientar una futura evaluación técnica o prueba piloto.

No debe entenderse como:

* implementación oficial vigente;
* sistema productivo;
* integración real con SUBE;
* integración real con organismos públicos;
* modificación actual de validadoras;
* solución tecnológica cerrada;
* proveedor obligatorio;
* diseño definitivo de infraestructura estatal.

La arquitectura es deliberadamente gradual, modular y adaptable.

---

## 3. Objetivo arquitectónico

El objetivo arquitectónico principal es permitir que una necesidad previamente acreditada pueda representarse operativamente como un atributo técnico de prioridad, sin exponer diagnósticos, historia clínica, certificados médicos ni datos sensibles en el núcleo operativo del sistema.

El modelo conceptual es:

```text
necesidad previamente acreditada
↓
atributo técnico de prioridad
↓
preferencia de asistencia
↓
validación operativa
↓
alerta genérica o asistencia preventiva
↓
evaluación institucional
```

---

## 4. Principios arquitectónicos

La arquitectura debe respetar los siguientes principios:

* privacidad por diseño;
* minimización de datos;
* no exposición de diagnósticos;
* separación entre acreditación y operación;
* neutralidad tecnológica;
* interoperabilidad responsable;
* modularidad;
* gradualidad;
* reversibilidad;
* auditabilidad;
* escalabilidad prudente;
* accesibilidad efectiva;
* no discriminación;
* no sustitución del régimen legal de asientos prioritarios;
* no imposición de nuevas cargas indebidas al chofer.

---

## 5. Separación entre acreditación y operación

La arquitectura distingue dos planos.

```text
Plano de acreditación:
organismos, profesionales, registros o procedimientos competentes
validan la necesidad de asistencia

Plano operativo:
el sistema técnico representa un atributo de prioridad
sin conocer ni exponer el diagnóstico o documentación respaldatoria
```

Esta separación es central para proteger la privacidad y evitar que el transporte público se transforme en un espacio de evaluación médica o documental.

---

## 6. Datos excluidos del núcleo operativo

El núcleo operativo no debe procesar:

* DNI;
* nombre;
* apellido;
* domicilio;
* diagnóstico médico;
* historia clínica;
* certificado médico en texto plano;
* datos de salud identificables;
* condición médica específica;
* documentación sanitaria;
* motivo sensible de la prioridad.

El sistema debe operar con atributos técnicos, tokens, hashes, identificadores pseudoanonimizados o señales genéricas.

---

## 7. Componentes conceptuales

Una arquitectura futura podría contemplar los siguientes componentes conceptuales:

```text
Módulo de acreditación institucional
↓
Módulo de emisión o habilitación de atributo técnico
↓
Módulo de validación operativa
↓
Módulo de preferencias de asistencia
↓
Módulo de alerta genérica o asistencia
↓
Módulo de registro mínimo
↓
Módulo de evaluación agregada
↓
Módulo de auditoría y gobernanza
```

Estos componentes son conceptuales y pueden implementarse de distintas maneras según la tecnología disponible, la jurisdicción y la autoridad competente.

---

## 8. Módulo de acreditación institucional

El módulo de acreditación institucional no pertenece al core técnico del MVP.

Su función conceptual sería determinar, conforme a reglas públicas y autoridad competente, si una persona se encuentra habilitada para solicitar asistencia preventiva.

Puede involucrar criterios médicos, funcionales, sanitarios, administrativos o sociales.

El sistema operativo no debe recibir ni almacenar la documentación que fundamenta esa acreditación.

---

## 9. Módulo de atributo técnico de prioridad

El atributo técnico de prioridad es la representación operativa de una habilitación previamente definida.

No debe revelar la causa de la prioridad.

Puede ser:

* temporal;
* permanente;
* revisable;
* asociado a una modalidad de asistencia;
* limitado a una prueba piloto;
* condicionado a un alcance territorial;
* revocable o actualizable.

El atributo no debe equivaler a un diagnóstico.

---

## 10. Módulo de preferencias de asistencia

El sistema puede contemplar preferencias de asistencia.

Un esquema conceptual posible es:

```text
0 = silenciosa
1 = discreta
2 = preventiva
3 = visible
```

Estas preferencias no representan categorías médicas.

Sólo indican modalidades operativas de experiencia de usuario.

La configuración final deberá ser definida por autoridad competente y evaluada en función de privacidad, accesibilidad y aceptación social.

---

## 11. Módulo de validación operativa

El módulo de validación operativa verifica si existe un atributo técnico activo.

En el MVP conceptual, esta validación se simula mediante tokens o identificadores demostrativos.

En una eventual prueba piloto real, la validación debería respetar:

* minimización de datos;
* seguridad;
* trazabilidad;
* finalidad determinada;
* control de acceso;
* conservación limitada;
* ausencia de diagnósticos;
* posibilidad de auditoría.

La validación no debe transformarse en evaluación médica.

---

## 12. Módulo de alerta o asistencia preventiva

El módulo de alerta o asistencia preventiva traduce la validación en una señal o experiencia concreta.

La alerta debe ser:

* genérica;
* no diagnóstica;
* no estigmatizante;
* proporcional;
* comprensible;
* configurable;
* evaluable;
* reversible.

Ejemplos conceptuales:

```text
Asistencia prioritaria solicitada
```

```text
Asiento de prioridad solicitado
```

```text
Se solicita colaboración para asistencia prioritaria
```

La alerta no debe indicar el motivo de la prioridad.

---

## 13. Canales posibles de asistencia

La arquitectura puede contemplar distintos canales, según evaluación técnica:

* señal visual;
* señal sonora breve;
* señal lumínica;
* mensaje en display;
* aviso discreto;
* registro técnico no público;
* indicador interno;
* integración con pictogramas;
* comunicación accesible;
* combinación de canales.

La elección del canal debe considerar privacidad, accesibilidad, ruido ambiente, comprensión, seguridad, costo e infraestructura existente.

---

## 14. Módulo de registro mínimo

El sistema puede registrar eventos mínimos para evaluación y seguridad.

Dichos registros deberían ser agregados o pseudoanonimizados.

Podrían incluir:

* cantidad de activaciones;
* línea o unidad;
* horario;
* modalidad de asistencia;
* errores técnicos;
* incidentes;
* reclamos;
* fallas;
* indicadores de uso.

No deberían incluir diagnósticos ni datos médicos identificables.

---

## 15. Módulo de evaluación agregada

La arquitectura debe permitir evaluación institucional.

La evaluación debería trabajar con datos agregados, no sensibles y orientados a medir:

* utilidad;
* privacidad;
* comprensión;
* aceptación social;
* carga operativa;
* incidentes;
* fallas técnicas;
* accesibilidad;
* convivencia;
* necesidad de ajustes;
* posibilidad de continuidad o cierre.

La evaluación es parte de la arquitectura, no un elemento externo.

---

## 16. Módulo de auditoría y gobernanza

Todo avance hacia una prueba piloto o implementación real debería contemplar mecanismos de auditoría y gobernanza.

Estos mecanismos pueden incluir:

* documentación de decisiones;
* responsables institucionales;
* control de accesos;
* registros de cambios;
* evaluación de privacidad;
* informes técnicos;
* criterios de suspensión;
* canales de reclamo;
* trazabilidad;
* revisión independiente;
* informe final.

La gobernanza permite evitar que la tecnología avance sin control institucional.

---

## 17. Interoperabilidad responsable

La interoperabilidad futura puede ser valiosa, pero debe ser especialmente prudente.

Toda interoperabilidad real deberá contar con:

* competencia institucional;
* marco jurídico;
* autorización;
* finalidad determinada;
* documentación técnica;
* seguridad de la información;
* minimización de datos;
* trazabilidad;
* auditoría;
* posibilidad de suspensión;
* evaluación de impacto.

En el estado actual del repositorio, toda integración externa debe interpretarse como simulada.

---

## 18. Modelo sin interoperabilidad real inicial

Para una primera prueba piloto, puede resultar más prudente evitar interoperabilidad real con organismos externos.

Un modelo inicial podría funcionar con:

```text
usuarios voluntarios
↓
atributos simulados o habilitados en entorno controlado
↓
validación demostrativa
↓
alerta genérica
↓
evaluación agregada
```

Este enfoque reduce riesgos jurídicos, técnicos y de privacidad.

---

## 19. Escalabilidad gradual

La arquitectura debe permitir escalabilidad gradual.

Un esquema posible es:

```text
MVP conceptual
↓
laboratorio técnico
↓
simulación controlada
↓
prueba piloto limitada
↓
piloto ampliado
↓
implementación territorial
↓
evaluación federal
↓
eventual implementación más amplia
```

Cada etapa debe tener criterios de avance, pausa, ajuste o cierre.

---

## 20. Reversibilidad

La reversibilidad es un principio arquitectónico.

Toda prueba o módulo debe poder desactivarse si se detectan:

* riesgos de privacidad;
* exposición de datos sensibles;
* fallas técnicas graves;
* rechazo social significativo;
* conflictos reiterados;
* carga indebida sobre choferes;
* falta de autorización;
* imposibilidad de auditoría;
* afectación de derechos.

La arquitectura debe prever la posibilidad de volver atrás.

---

## 21. Neutralidad tecnológica

SUBE Prioridad no debe quedar atado a una única tecnología, proveedor, tarjeta, aplicación, validadora, protocolo o plataforma.

La autoridad competente deberá definir la tecnología adecuada en función de:

* seguridad;
* costos;
* infraestructura existente;
* accesibilidad;
* interoperabilidad;
* mantenimiento;
* protección de datos;
* disponibilidad;
* escalabilidad;
* sostenibilidad.

El repositorio propone una referencia conceptual, no una contratación ni una solución propietaria.

---

## 22. Relación con el sistema SUBE

La denominación SUBE Prioridad refiere a una posible articulación futura con el ecosistema de transporte y boleto electrónico.

Sin embargo, el repositorio actual:

* no modifica el sistema SUBE;
* no se conecta con sistemas SUBE reales;
* no opera sobre validadoras reales;
* no acredita autorización institucional;
* no integra bases de datos públicas;
* no procesa tarjetas reales.

Cualquier relación futura con SUBE deberá ser evaluada por las autoridades competentes.

---

## 23. Relación con validadoras y hardware

La arquitectura no presupone una modificación inmediata de validadoras ni hardware embarcado.

En una etapa conceptual o piloto podrían evaluarse alternativas como:

* simuladores;
* dispositivos de laboratorio;
* interfaces demostrativas;
* displays externos;
* señales independientes;
* validadores no productivos;
* entornos controlados;
* pruebas sin conexión real.

Toda modificación de hardware real requeriría autorización, homologación y evaluación técnica.

---

## 24. Relación con pictogramas y accesibilidad cognitiva

La arquitectura puede articularse con pictogramas, señalética accesible, lenguaje claro y comunicación inclusiva.

Esta articulación puede permitir que la asistencia preventiva sea más comprensible para el entorno.

Modelo conceptual:

```text
pictogramas y señalética accesible
↓
comprensión del entorno
↓
atributo técnico de prioridad
↓
alerta genérica
↓
mejor convivencia
```

La accesibilidad tecnológica no debe desplazar a la accesibilidad cognitiva, sino complementarla.

---

## 25. Seguridad de la información

Una implementación real debería contemplar medidas de seguridad acordes al riesgo.

Entre ellas:

* cifrado;
* control de accesos;
* gestión de claves;
* segregación de entornos;
* auditoría;
* monitoreo;
* gestión de incidentes;
* revisión de código;
* pruebas de seguridad;
* respaldo y recuperación;
* eliminación segura;
* trazabilidad de cambios.

El MVP actual no debe interpretarse como infraestructura productiva segura.

---

## 26. Arquitectura del MVP actual

El MVP actual representa una demostración mínima.

Incluye, según el estado del repositorio:

* API demostrativa;
* endpoint raíz;
* endpoint de salud;
* endpoint de guardrails;
* endpoint de verificación conceptual;
* modelos de request y response;
* validación simulada por token;
* declaración explícita de ausencia de datos sensibles;
* declaración explícita de ausencia de integración real;
* tests básicos;
* Docker;
* documentación.

El MVP sirve para comunicar una arquitectura, no para operar usuarios reales.

---

## 27. Endpoints conceptuales del MVP

Los endpoints conceptuales son:

```text
GET  /
GET  /health
GET  /project/guardrails
POST /api/v1/prioridad/verificar
```

Estos endpoints permiten demostrar:

* estado del proyecto;
* salud del servicio;
* límites conceptuales;
* verificación simulada de atributo técnico.

No implican conexión real con organismos, SUBE, validadoras ni usuarios reales.

---

## 28. Modelo de entrada del MVP

El modelo de entrada debe evitar datos personales o médicos.

Un request conceptual puede incluir:

```text
token_prioridad
linea
unidad
```

El campo relevante es un token técnico o identificador pseudoanonimizado.

Los campos de línea y unidad sólo deben usarse para simulación o evaluación técnica, no para vigilancia individualizada.

---

## 29. Modelo de salida del MVP

La respuesta conceptual puede incluir:

```text
prioridad_activa
perfil_ux
fecha_caducidad
motivo
entorno
datos_sensibles_procesados
integracion_real_con_organismos
```

La respuesta debe declarar explícitamente que no se procesan datos sensibles y que no existe integración real con organismos.

Esto refuerza la transparencia del MVP.

---

## 30. Guardrails técnicos

Toda evolución del código debe respetar guardrails mínimos.

No incorporar al core:

* DNI;
* nombre;
* apellido;
* domicilio;
* diagnóstico médico;
* historia clínica;
* certificado médico en texto plano;
* datos de salud identificables.

No afirmar integración real si no existe.

No convertir el Bono Solidario en parte obligatoria del núcleo inicial.

No modificar la lógica de asientos prioritarios.

No imponer tareas médicas o decisorias al chofer.

---

## 31. Criterios para evolucionar la arquitectura

Antes de evolucionar el MVP, debería verificarse:

```text
[ ] Coherencia con privacidad por diseño.
[ ] Ausencia de datos sensibles en el core.
[ ] Integraciones simuladas correctamente identificadas.
[ ] Tests actualizados.
[ ] Documentación coherente.
[ ] Guardrails respetados.
[ ] No exposición de diagnósticos.
[ ] No afirmación de implementación productiva.
[ ] No afectación de derechos vigentes.
[ ] Evaluación institucional prevista.
```

---

## 32. Relación con otros documentos del repositorio

Este documento debe leerse junto con:

* `README.md`;
* `ARCHITECTURE_GUARDRAILS.md`;
* `docs/INDICE_DOCUMENTAL.md`;
* `docs/DECISIONES_DE_ARQUITECTURA.md`;
* `docs/ROADMAP_IMPLEMENTACION.md`;
* `docs/PRINCIPIOS_DE_GOBERNANZA.md`;
* `docs/PROTECCION_DATOS_PERSONALES.md`;
* `docs/FUNDAMENTOS_JURIDICOS.md`;
* `docs/FUNDAMENTOS_MEDICOS.md`;
* `docs/PROTOCOLO_OPERATIVO.md`;
* `docs/PRUEBA_PILOTO_MODELO.md`.

---

## 33. Declaración final

La arquitectura de referencia de SUBE Prioridad propone un camino prudente para articular tecnología, accesibilidad, privacidad y evaluación institucional.

Su núcleo no es diagnosticar personas ni imponer una implementación inmediata.

Su núcleo es representar una necesidad previamente acreditada mediante un atributo técnico de prioridad, sin exponer datos sensibles, permitiendo asistencia preventiva y evaluación gradual.

Toda evolución técnica deberá mantener coherencia con los principios de privacidad, minimización, interoperabilidad responsable, reversibilidad, auditabilidad, no discriminación y respeto de los derechos vigentes.

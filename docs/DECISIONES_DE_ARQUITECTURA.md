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
persona habilitada
↓
atributo técnico de prioridad
↓
preferencia de asistencia
```

### Fundamento

La necesidad de asistencia puede estar previamente acreditada por organismos, profesionales, registros o procedimientos competentes, pero el sistema operativo de transporte no necesita conocer la causa médica, funcional o administrativa que originó esa habilitación.

### Consecuencia

El sistema debe trabajar con atributos técnicos, tokens, hashes o identificadores pseudoanonimizados.

No deben incorporarse campos como:

- DNI;
- nombre;
- apellido;
- domicilio;
- diagnóstico médico;
- historia clínica;
- certificado médico en texto plano;
- datos de salud identificables.

---

## 3. Decisión 2 — Separación entre acreditación y operación

### Decisión

SUBE Prioridad separa el plano de acreditación del plano operativo.

```text
Plano de acreditación:
organismos, profesionales, registros o procedimientos competentes
validan la necesidad de asistencia

Plano operativo:
el sistema técnico representa un atributo de prioridad
sin conocer ni exponer el diagnóstico o documentación respaldatoria
```

### Fundamento

Esta separación protege la privacidad, reduce riesgos jurídicos y evita que el transporte público se transforme en una instancia médica, sanitaria o documental.

### Consecuencia

El personal de conducción, las validadoras, la API demostrativa y los módulos operativos no deben evaluar diagnósticos ni revisar certificados.

---

## 4. Decisión 3 — Privacidad por diseño

### Decisión

La privacidad debe formar parte del diseño desde el inicio.

No debe agregarse como una corrección posterior.

### Fundamento

SUBE Prioridad puede involucrar situaciones vinculadas con salud, discapacidad, edad, embarazo, movilidad reducida, rehabilitación u otras condiciones sensibles.

Por eso, el sistema debe minimizar el tratamiento de datos personales y evitar cualquier exposición innecesaria.

### Consecuencia

Toda evolución técnica debe responder esta pregunta:

```text
¿este dato es estrictamente necesario para activar asistencia preventiva?
```

Si la respuesta es no, el dato no debe ingresar al core operativo.

---

## 5. Decisión 4 — MVP conceptual y no productivo

### Decisión

El repositorio implementa un MVP conceptual, técnico y demostrativo.

No representa una implementación productiva.

### Fundamento

El objetivo del repositorio es demostrar una arquitectura posible, modular y auditable, no operar usuarios reales ni conectarse con infraestructura estatal.

### Consecuencia

El MVP no debe afirmar:

- integración real con SUBE;
- conexión real con organismos públicos;
- operación sobre validadoras reales;
- procesamiento de usuarios reales;
- modificación de infraestructura estatal;
- implementación oficial vigente.

---

## 6. Decisión 5 — Interoperabilidad simulada en el MVP

### Decisión

Toda interoperabilidad externa del MVP debe ser simulada salvo autorización institucional expresa, documentación técnica y convenio o marco jurídico aplicable.

### Fundamento

El proyecto puede contemplar interoperabilidad futura, pero afirmar integraciones inexistentes generaría riesgos técnicos, jurídicos e institucionales.

### Consecuencia

Módulos como `xroad_gateway.py` deben mantenerse como simuladores, adaptadores desacoplados o interfaces conceptuales.

No debe afirmarse conexión real con:

- ANDIS;
- SISA;
- RENAPER;
- Mi Argentina;
- Nación Servicios S.A.;
- CNRT;
- sistemas SUBE reales;
- validadoras reales.

---

## 7. Decisión 6 — Neutralidad tecnológica

### Decisión

La arquitectura no debe depender de una tecnología, proveedor, tarjeta, validadora, aplicación, sistema operativo o plataforma específica.

### Fundamento

SUBE Prioridad se concibe como arquitectura de referencia adaptable, no como solución propietaria cerrada.

### Consecuencia

La documentación y el código deben evitar formular la propuesta como dependiente de:

- una marca de hardware;
- una tarjeta específica;
- una app obligatoria;
- un protocolo único;
- un proveedor determinado;
- una implementación técnica cerrada.

La autoridad competente deberá definir, en cada caso, la tecnología adecuada.

---

## 8. Decisión 7 — Implementación gradual, reversible y auditable

### Decisión

Toda evolución debe poder implementarse por etapas, evaluarse y revertirse si aparecen riesgos.

### Fundamento

Una política pública tecnológica debe evitar despliegues irreversibles sin evidencia previa.

### Consecuencia

La evolución debe contemplar fases como:

```text
MVP conceptual
↓
laboratorio técnico
↓
prueba piloto limitada
↓
piloto ampliado
↓
implementación regional
↓
eventual implementación nacional
↓
adaptación a otras jurisdicciones
```

Ninguna fase debe avanzar automáticamente a la siguiente.

---

## 9. Decisión 8 — No sustitución del régimen legal de asientos prioritarios

### Decisión

SUBE Prioridad no sustituye, modifica, limita ni debilita el régimen legal vigente de asientos prioritarios.

### Fundamento

El proyecto busca fortalecer la accesibilidad efectiva, no reemplazar derechos ya reconocidos.

### Consecuencia

La herramienta debe presentarse como complementaria.

No debe crear una categoría superior de derecho ni reducir obligaciones existentes.

---

## 10. Decisión 9 — No imposición de nuevas cargas indebidas al chofer

### Decisión

El personal de conducción no debe ser convertido en evaluador médico, fiscalizador documental, administrador de datos sensibles ni árbitro principal de conflictos entre pasajeros.

### Fundamento

La conducción segura debe conservar prioridad operativa.

El sistema debe reducir conflictos, no trasladarlos al chofer.

### Consecuencia

El diseño no debe exigir que el chofer:

- pida diagnósticos;
- revise certificados;
- decida quién merece asistencia;
- administre datos sensibles;
- aplique sanciones;
- resuelva disputas por prioridad.

---

## 11. Decisión 10 — Alertas genéricas y no diagnósticas

### Decisión

Toda alerta o señal de asistencia debe ser genérica, no diagnóstica y no estigmatizante.

### Fundamento

La finalidad es solicitar colaboración sin revelar la causa de la prioridad.

### Consecuencia

Ejemplos conceptuales aceptables:

```text
Asistencia prioritaria solicitada
```

```text
Asiento de prioridad solicitado
```

```text
Se solicita colaboración para asistencia prioritaria
```

Ejemplos que deben evitarse:

```text
Paciente oncológico
```

```text
Persona trasplantada
```

```text
Persona con diagnóstico médico
```

```text
Discapacidad específica
```

---

## 12. Decisión 11 — Preferencias de asistencia controladas por el usuario

### Decisión

El sistema puede contemplar distintas preferencias de asistencia.

Un esquema conceptual posible es:

```text
0 = silenciosa
1 = discreta
2 = preventiva
3 = visible
```

### Fundamento

No todas las personas desean recibir asistencia de la misma forma.

La asistencia debe estar al servicio de la autonomía personal.

### Consecuencia

Las preferencias no deben representar diagnósticos ni categorías médicas.

Sólo deben indicar modalidades operativas de experiencia de usuario.

---

## 13. Decisión 12 — Registro mínimo y evaluación agregada

### Decisión

Los registros deben ser mínimos, proporcionales y orientados a evaluación.

### Fundamento

La medición es necesaria para evaluar utilidad, riesgos y continuidad, pero no debe convertirse en vigilancia individualizada.

### Consecuencia

Podrían registrarse de manera agregada o pseudoanonimizada:

- cantidad de activaciones;
- línea o unidad;
- horario;
- modalidad de asistencia;
- errores técnicos;
- incidentes;
- reclamos;
- indicadores de uso.

No deben registrarse diagnósticos ni datos médicos identificables.

---

## 14. Decisión 13 — Bono Solidario como evolución futura

### Decisión

El Bono Solidario no forma parte del núcleo inicial indispensable de SUBE Prioridad.

Debe considerarse una posible evolución futura.

### Fundamento

El objetivo inicial del proyecto es facilitar asistencia preventiva para personas con necesidad previamente acreditada de viajar sentadas.

El Bono Solidario requiere reglas propias de privacidad, voluntariedad, antifraude y no discriminación.

### Consecuencia

El Bono Solidario no debe implementarse como:

- multa;
- sanción;
- obligación;
- ranking público;
- mecanismo de presión social;
- sistema de vigilancia;
- beneficio por ocupar o liberar asientos prioritarios legales.

---

## 15. Decisión 14 — Arquitectura preparada para prueba piloto

### Decisión

La arquitectura debe estar pensada para una prueba piloto limitada, voluntaria, reversible y auditable.

### Fundamento

La primera meta institucional razonable no es una implementación nacional inmediata, sino una evaluación controlada.

### Consecuencia

Toda prueba piloto debería definir:

- autoridad responsable;
- alcance territorial;
- duración;
- población participante;
- participación voluntaria;
- datos excluidos del core;
- modalidad de asistencia;
- indicadores;
- canales de reclamo;
- criterios de suspensión;
- informe final.

---

## 16. Decisión 15 — Documentación como parte de la arquitectura

### Decisión

La documentación no es secundaria.

Forma parte de la arquitectura del proyecto.

### Fundamento

SUBE Prioridad combina software, política pública, privacidad, accesibilidad, operación de transporte, fundamentos jurídicos y evaluación institucional.

Sin documentación clara, la arquitectura puede ser malinterpretada.

### Consecuencia

El repositorio debe mantener documentación coherente sobre:

- alcance del MVP;
- arquitectura de referencia;
- roadmap;
- protección de datos;
- fundamentos jurídicos;
- fundamentos médicos;
- protocolo operativo;
- prueba piloto;
- gobernanza;
- guardrails técnicos.

---

## 17. Decisión 16 — Seguridad jurídica del repositorio público

### Decisión

El repositorio debe evitar afirmaciones que puedan interpretarse como implementación oficial, integración real o decisión estatal vigente.

### Fundamento

El proyecto se presenta como iniciativa ciudadana de innovación pública.

La decisión de implementación corresponde exclusivamente a las autoridades competentes.

### Consecuencia

Debe evitarse afirmar:

- “el sistema está integrado”;
- “Nación Servicios implementa”;
- “las validadoras procesan”;
- “ANDIS valida en producción”;
- “SISA verifica”;
- “Mi Argentina opera”;
- “SUBE ya incorpora el atributo”.

La formulación correcta es:

```text
podría evaluarse
podría analizarse
en una eventual prueba piloto
sujeto a autorización
en entorno simulado
como arquitectura conceptual
```

---

## 18. Decisión 17 — Escalabilidad sin automatismo

### Decisión

La arquitectura debe poder escalar, pero ninguna ampliación debe ser automática.

### Fundamento

El crecimiento debe basarse en evidencia, evaluación institucional, sostenibilidad y aceptación social.

### Consecuencia

El proyecto puede contemplar una evolución desde:

```text
una línea o corredor
↓
piloto ampliado
↓
municipio o región
↓
provincia o AMBA
↓
implementación nacional
↓
modelo adaptable a otras jurisdicciones
```

Pero cada etapa requiere evaluación previa.

---

## 19. Decisión 18 — Accesibilidad cognitiva y comunicación inclusiva

### Decisión

SUBE Prioridad puede articularse con pictogramas, señalética clara, lenguaje simple y comunicación inclusiva.

### Fundamento

La asistencia preventiva no depende únicamente de tecnología digital.

También requiere comprensión social, accesibilidad cognitiva y convivencia ciudadana.

### Consecuencia

La arquitectura debe permitir compatibilidad con:

- pictogramas;
- señalética accesible;
- mensajes simples;
- comunicación visual;
- materiales de capacitación;
- campañas de sensibilización.

---

## 20. Decisión 19 — Brecha digital y canales alternativos

### Decisión

El diseño no debe depender exclusivamente de teléfonos inteligentes, aplicaciones móviles o conectividad permanente.

### Fundamento

Una herramienta de accesibilidad no debe excluir a personas por falta de recursos tecnológicos, conectividad o alfabetización digital.

### Consecuencia

Toda implementación real debería evaluar canales alternativos, presenciales o asistidos, definidos por autoridad competente.

---

## 21. Decisión 20 — Tests y compilación como regla de cambio seguro

### Decisión

Toda evolución del código debe mantener compilación y tests automatizados.

### Fundamento

El MVP debe conservar una base técnica estable.

### Consecuencia

Antes de mergear cambios relevantes, debería verificarse:

```bash
python -m py_compile main.py validator.py cache_manager.py circuit_breaker.py xroad_gateway.py
pytest -q
```

Si el cambio rompe compilación o tests, no debe incorporarse a `main`.

---

## 22. Relación con otros documentos del repositorio

Este documento debe leerse junto con:

- `README.md`;
- `ARCHITECTURE_GUARDRAILS.md`;
- `docs/INDICE_DOCUMENTAL.md`;
- `docs/ARQUITECTURA_DE_REFERENCIA.md`;
- `docs/ROADMAP_IMPLEMENTACION.md`;
- `docs/PRINCIPIOS_DE_GOBERNANZA.md`;
- `docs/PROTECCION_DATOS_PERSONALES.md`;
- `docs/FUNDAMENTOS_JURIDICOS.md`;
- `docs/FUNDAMENTOS_MEDICOS.md`;
- `docs/PROTOCOLO_OPERATIVO.md`;
- `docs/PRUEBA_PILOTO_MODELO.md`.

---

## 23. Declaración final

Las decisiones de arquitectura de SUBE Prioridad buscan preservar la coherencia entre el MVP técnico, la documentación institucional y la visión de largo plazo del proyecto.

El sistema debe evolucionar como una arquitectura conceptual prudente, modular, reversible, auditable y respetuosa de la privacidad.

Su núcleo no consiste en diagnosticar personas ni imponer una implementación inmediata, sino en explorar si una necesidad previamente acreditada puede representarse mediante un atributo técnico de prioridad que facilite asistencia preventiva sin exposición de datos sensibles.

Toda evolución futura deberá respetar los principios de privacidad por diseño, minimización de datos, accesibilidad efectiva, neutralidad tecnológica, protección de derechos vigentes y evaluación institucional suficiente.

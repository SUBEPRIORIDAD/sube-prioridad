# Índice Documental — SUBE Prioridad

## 1. Propósito

Este índice organiza la documentación principal del repositorio SUBE Prioridad.

El proyecto se presenta como una propuesta ciudadana de innovación pública, acompañada por un MVP conceptual, documentación de arquitectura, fundamentos institucionales, estrategia legislativa y anexos técnicos.

La finalidad de este índice es facilitar la lectura por parte de:

* desarrolladores;
* legisladores;
* autoridades públicas;
* asesores técnicos;
* universidades;
* organizaciones de la sociedad civil;
* ciudadanos interesados;
* personas que acompañan la propuesta con firmas.

---

## 2. Estado general del repositorio

El repositorio representa actualmente un MVP conceptual, técnico y demostrativo.

No constituye una implementación productiva.

No acredita integración real con organismos públicos.

No modifica el sistema SUBE.

No altera el régimen vigente de asientos prioritarios.

No procesa diagnósticos médicos, historia clínica ni datos sensibles en el núcleo del MVP.

Toda eventual implementación real deberá quedar sujeta a evaluación técnica, jurídica, presupuestaria, operativa, social e institucional por parte de las autoridades competentes.

---

# Documentación principal

## README.md

Documento de entrada al repositorio.

Presenta:

* qué es SUBE Prioridad;
* qué no es;
* estado actual del MVP;
* principios de privacidad;
* arquitectura general;
* ejecución local;
* documentación complementaria.

Debe leerse primero.

---

## ARCHITECTURE_GUARDRAILS.md

Define los límites técnicos y conceptuales que toda evolución del proyecto debe respetar.

Incluye reglas sobre:

* privacidad por diseño;
* minimización de datos;
* datos prohibidos en el core;
* interoperabilidad simulada;
* Bono Solidario como evolución futura;
* separación entre documentación conceptual y producción;
* cambios seguros en el código.

Es el documento de control de coherencia técnica.

---

## docs/ARQUITECTURA_DE_REFERENCIA.md

Describe la arquitectura conceptual de SUBE Prioridad.

Explica cómo el proyecto puede entenderse como una arquitectura abierta, modular, escalable y tecnológicamente neutral.

Debe leerse para comprender la visión de largo plazo: desde un MVP conceptual hasta eventuales pruebas piloto, implementaciones regionales, nacionales o adaptaciones en otras jurisdicciones.

---

## docs/ROADMAP_IMPLEMENTACION.md

Ordena una posible evolución progresiva del proyecto.

Describe etapas como:

* investigación y documentación;
* MVP conceptual;
* laboratorio técnico;
* prueba piloto limitada;
* piloto ampliado;
* implementación regional;
* implementación nacional;
* modelo adaptable a otras jurisdicciones.

No constituye un cronograma obligatorio.

Funciona como guía conceptual para evaluar escalabilidad, reversibilidad y control institucional.

---

## docs/DECISIONES_DE_ARQUITECTURA.md

Registra las principales decisiones de diseño del proyecto.

Explica, entre otras cuestiones:

* por qué se usa un atributo técnico y no diagnósticos médicos;
* por qué el MVP no procesa datos sensibles;
* por qué las integraciones son simuladas;
* por qué la arquitectura debe ser neutral tecnológicamente;
* por qué el Bono Solidario queda desacoplado del core inicial;
* por qué la implementación debe ser gradual y reversible.

Este documento conecta el código con la filosofía de ingeniería del proyecto.

---

## docs/PRINCIPIOS_DE_GOBERNANZA.md

Define criterios institucionales para una eventual evolución del proyecto.

Incluye principios sobre:

* evaluación previa;
* competencia pública;
* transparencia;
* auditabilidad;
* protección de datos;
* separación de roles;
* accesibilidad;
* no discriminación;
* interoperabilidad responsable;
* gestión de riesgos;
* participación institucional.

Debe leerse antes de pensar cualquier prueba piloto o implementación real.

---

## docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md

Ordena la estrategia institucional y ciudadana para impulsar el análisis de SUBE Prioridad en Argentina.

Explica cómo presentar la propuesta ante:

* legisladores;
* autoridades administrativas;
* organismos técnicos;
* universidades;
* organizaciones sociales;
* ciudadanía.

También diferencia entre:

* expediente institucional;
* repositorio técnico;
* campaña ciudadana;
* firmas de apoyo.

Su eje central es solicitar evaluación responsable y eventual prueba piloto, no implementación nacional inmediata.

---

## docs/DOSSIER_INSTITUCIONAL_BREVE.md

Documento breve para presentación institucional.

Resume:

* problema público;
* objetivo de la propuesta;
* qué es SUBE Prioridad;
* qué no es;
* principios rectores;
* MVP actual;
* propuesta de prueba piloto;
* protección de datos;
* rol de la ciudadanía;
* solicitud institucional.

Es el documento recomendado para acompañar petitorios, reuniones, firmas ciudadanas o primeras conversaciones con legisladores y autoridades.

---

## docs/PLIEGO_TECNICO_EXTENDIDO.md

Documento técnico amplio que conserva la visión integral original del proyecto.

Debe interpretarse como una especificación conceptual, prospectiva y evolutiva.

No debe leerse como implementación productiva actualmente desplegada ni como integración real vigente.

Su contenido complementa al README y a la Arquitectura de Referencia.

---

# Documentación complementaria sugerida

A medida que el proyecto continúe ordenándose, podrán agregarse carpetas específicas dentro de `docs/`, por ejemplo:

```text
docs/
  fundamentos/
  institucional/
  juridico/
  medico/
  arquitectura/
  privacidad/
  interoperabilidad/
  bono-solidario/
  anexos/
  historico/
```

Estas carpetas permitirán separar documentos extensos, borradores, anexos técnicos y versiones históricas sin sobrecargar la documentación principal.

---

# Orden recomendado de lectura

Para una primera lectura institucional:

```text
1. README.md
2. docs/DOSSIER_INSTITUCIONAL_BREVE.md
3. docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md
4. docs/ROADMAP_IMPLEMENTACION.md
```

Para una lectura técnica:

```text
1. README.md
2. ARCHITECTURE_GUARDRAILS.md
3. docs/ARQUITECTURA_DE_REFERENCIA.md
4. docs/DECISIONES_DE_ARQUITECTURA.md
5. docs/PLIEGO_TECNICO_EXTENDIDO.md
```

Para una lectura jurídica e institucional:

```text
1. docs/DOSSIER_INSTITUCIONAL_BREVE.md
2. docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md
3. docs/PRINCIPIOS_DE_GOBERNANZA.md
4. docs/ROADMAP_IMPLEMENTACION.md
```

Para una lectura ciudadana:

```text
1. README.md
2. docs/DOSSIER_INSTITUCIONAL_BREVE.md
3. docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md
```

---

# Criterios de interpretación

Toda la documentación debe interpretarse conforme a los siguientes criterios:

* SUBE Prioridad es una propuesta ciudadana de innovación pública.
* El repositorio contiene un MVP conceptual y demostrativo.
* Las integraciones externas son simuladas salvo indicación expresa en contrario.
* Los documentos técnicos describen escenarios posibles, no obligaciones de implementación.
* Las autoridades competentes conservan la decisión sobre factibilidad, alcance, diseño e implementación.
* El sistema no debe procesar diagnósticos médicos ni historia clínica en el core.
* La propuesta no sustituye el régimen legal de asientos prioritarios.
* El Bono Solidario es una evolución futura, no parte del núcleo inicial.
* Toda implementación real debe ser gradual, reversible, auditable y respetuosa de la privacidad.

---

# Documentos pendientes recomendados

Para fortalecer aún más el repositorio, podrían desarrollarse luego los siguientes documentos:

```text
docs/PETITORIO_MODELO.md
docs/MODELO_PROYECTO_RESOLUCION.md
docs/FUNDAMENTOS_JURIDICOS.md
docs/FUNDAMENTOS_MEDICOS.md
docs/FUNDAMENTOS_OPERATIVOS.md
docs/PRUEBA_PILOTO_MODELO.md
docs/PROTECCION_DATOS_PERSONALES.md
docs/BONO_SOLIDARIO.md
docs/ANEXOS_ORIGINALES_REFERENCIA.md
```

Estos documentos deberán agregarse de manera gradual, evitando repeticiones y manteniendo coherencia con el README, los guardrails y la arquitectura de referencia.

---

# Declaración final

El Índice Documental tiene por finalidad preservar la coherencia del proyecto.

SUBE Prioridad no debe leerse únicamente como un repositorio de software ni únicamente como un expediente institucional.

Debe entenderse como una arquitectura pública en desarrollo, construida sobre documentación técnica, fundamentos jurídicos, principios de privacidad, participación ciudadana y una estrategia gradual orientada a permitir su evaluación responsable por parte de las autoridades competentes.

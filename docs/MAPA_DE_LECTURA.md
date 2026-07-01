# Mapa de lectura — SUBE Prioridad

## Guía para comprender la documentación del proyecto

---

# Propósito de este documento

SUBE Prioridad contiene documentación con distintos niveles de profundidad: presentación general, fundamentos institucionales, arquitectura técnica, privacidad, gobernanza, operación y estrategia de implementación.

Este documento permite identificar el recorrido recomendado según el perfil del lector y el objetivo de consulta.

No todos los lectores necesitan recorrer la totalidad del repositorio.

Cada documento cumple una función específica dentro de la arquitectura documental del proyecto.

---

# Lectura recomendada general

Para una primera aproximación al proyecto:

```text
INTRODUCCION_SUBE_PRIORIDAD.md

↓

RESUMEN_EJECUTIVO_SUBE_PRIORIDAD.md

↓

docs/INDICE_DOCUMENTAL.md
```

Este recorrido permite comprender:

* qué es SUBE Prioridad;
* qué problema busca abordar;
* cuáles son sus principios;
* qué límites tiene;
* cómo está organizada la documentación.

---

# Perfil: ciudadano/a o persona interesada

## Objetivo

Comprender la idea general sin necesidad de conocimientos técnicos.

Leer:

```text
INTRODUCCION_SUBE_PRIORIDAD.md
```

Permite conocer:

* origen de la propuesta;
* problema social abordado;
* funcionamiento conceptual;
* privacidad;
* límites del proyecto;
* visión general.

---

# Perfil: legislador/a, funcionario/a o asesor/a institucional

## Objetivo

Analizar SUBE Prioridad como una posible iniciativa de innovación pública.

Recorrido recomendado:

```text
INTRODUCCION_SUBE_PRIORIDAD.md

↓

docs/DOSSIER_INSTITUCIONAL_BREVE.md

↓

docs/FUNDAMENTOS_JURIDICOS.md

↓

docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md

↓

docs/PRUEBA_PILOTO_MODELO.md
```

Este recorrido permite analizar:

* finalidad pública;
* fundamentos jurídicos;
* marco institucional;
* participación ciudadana;
* implementación gradual.

---

# Perfil: especialista en accesibilidad, salud o enfoque funcional

## Objetivo

Comprender el fundamento humano y funcional del proyecto.

Recorrido recomendado:

```text
INTRODUCCION_SUBE_PRIORIDAD.md

↓

docs/FUNDAMENTOS_MEDICOS.md

↓

docs/PROTOCOLO_OPERATIVO.md

↓

docs/PRUEBA_PILOTO_MODELO.md
```

Permite analizar:

* necesidades de asistencia;
* situaciones visibles y no visibles;
* autonomía de las personas;
* experiencia de usuario;
* modelo de asistencia preventiva.

---

# Perfil: abogado/a o especialista jurídico

## Objetivo

Evaluar la compatibilidad normativa y los límites legales.

Recorrido recomendado:

```text
docs/FUNDAMENTOS_JURIDICOS.md

↓

docs/PROTECCION_DATOS_PERSONALES.md

↓

docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md

↓

docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
```

Permite revisar:

* derechos involucrados;
* accesibilidad;
* protección de datos;
* responsabilidad institucional;
* condiciones de adopción futura.

---

# Perfil: especialista en privacidad y protección de datos

## Objetivo

Analizar el modelo de minimización de información y separación de funciones.

Recorrido recomendado:

```text
docs/PROTECCION_DATOS_PERSONALES.md

↓

docs/ARQUITECTURA_DE_REFERENCIA.md

↓

docs/DECISIONES_DE_ARQUITECTURA.md

↓

ARCHITECTURE_GUARDRAILS.md
```

Aspectos principales:

* privacidad por diseño;
* minimización de datos;
* separación entre acreditación y operación;
* atributos técnicos;
* interoperabilidad responsable.

---

# Perfil: arquitecto/a de software o desarrollador/a

## Objetivo

Comprender el MVP técnico y la arquitectura demostrativa.

Recorrido recomendado:

```text
README.md

↓

docs/ARQUITECTURA_DE_REFERENCIA.md

↓

docs/DECISIONES_DE_ARQUITECTURA.md

↓

ARCHITECTURE_GUARDRAILS.md

↓

PLIEGO_TECNICO_EXTENDIDO.md
```

Incluye:

* arquitectura conceptual;
* componentes técnicos;
* límites del MVP;
* criterios de evolución;
* guardrails.

---

# Perfil: organismo, empresa o institución interesada en evaluar adopción

## Objetivo

Analizar condiciones necesarias antes de cualquier prueba piloto o implementación.

Recorrido recomendado:

```text
docs/RESUMEN_EJECUTIVO_SUBE_PRIORIDAD.md

↓

docs/PRUEBA_PILOTO_MODELO.md

↓

docs/PROTOCOLO_OPERATIVO.md

↓

docs/PRINCIPIOS_DE_GOBERNANZA.md

↓

docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md

↓

docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
```

Permite evaluar:

* gradualidad;
* gobernanza;
* responsabilidades;
* custodia;
* condiciones institucionales.

---

# Perfil: periodista, investigador/a o académico/a

## Objetivo

Comprender el proyecto y sus fundamentos.

Recorrido recomendado:

```text
INTRODUCCION_SUBE_PRIORIDAD.md

↓

docs/RESUMEN_EJECUTIVO_SUBE_PRIORIDAD.md

↓

docs/INDICE_DOCUMENTAL.md

↓

documentos específicos según interés
```

---

# Documentos principales del repositorio

## Presentación

```text
INTRODUCCION_SUBE_PRIORIDAD.md
```

Primera lectura general.

---

## Documento técnico principal

```text
README.md
```

Descripción completa del MVP conceptual y demostrativo.

---

## Organización documental

```text
docs/INDICE_DOCUMENTAL.md
```

Índice general de todos los documentos.

---

## Arquitectura

```text
docs/ARQUITECTURA_DE_REFERENCIA.md
```

Modelo conceptual de evolución tecnológica.

---

## Privacidad

```text
docs/PROTECCION_DATOS_PERSONALES.md
```

Principios de protección de datos y minimización.

---

## Fundamentos jurídicos

```text
docs/FUNDAMENTOS_JURIDICOS.md
```

Marco legal y conceptual.

---

## Fundamentos médicos

```text
docs/FUNDAMENTOS_MEDICOS.md
```

Fundamentos funcionales y sanitarios conceptuales.

---

## Operación

```text
docs/PROTOCOLO_OPERATIVO.md
```

Modelo operativo conceptual.

---

## Prueba piloto

```text
docs/PRUEBA_PILOTO_MODELO.md
```

Modelo de evaluación gradual.

---

## Gobernanza

```text
docs/PRINCIPIOS_DE_GOBERNANZA.md
```

Criterios de transparencia, control y responsabilidad.

---

## Custodia institucional

```text
docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md
```

Protección del carácter ciudadano y abierto del proyecto.

---

## Marca y uso público

```text
docs/POLITICA_DE_MARCA.md
```

Criterios de uso responsable de identidad y denominaciones.

---

# Regla general de interpretación

Toda la documentación del proyecto debe interpretarse bajo estos principios:

```text
MVP conceptual

no implementación oficial vigente

no integración real con SUBE

no procesamiento de datos médicos sensibles

no diagnóstico

no vigilancia

no sanciones

no reemplazo de derechos existentes

no nuevas cargas indebidas al personal

implementación solo mediante evaluación institucional
```

---

# Cierre

SUBE Prioridad combina documentación ciudadana, técnica, jurídica e institucional.

Este mapa busca que cada lector pueda acceder al nivel adecuado de información sin perder de vista el propósito general:

analizar si una herramienta tecnológica, diseñada con privacidad, accesibilidad y responsabilidad institucional, puede contribuir a una experiencia de transporte público más segura, digna y respetuosa.

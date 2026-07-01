# Índice Documental — SUBE Prioridad

## Guía general de documentación del proyecto ciudadano

---

## 1. Finalidad de este índice

Este documento organiza la documentación principal del repositorio SUBE Prioridad.

Su finalidad es permitir una lectura ordenada, gradual y comprensible del proyecto, diferenciando documentos introductorios, ejecutivos, técnicos, jurídicos, médicos, operativos, institucionales, de gobernanza, de protección de datos, de marca y de custodia pública.

SUBE Prioridad debe interpretarse como una iniciativa ciudadana abierta, conceptual, demostrativa y documentada, impulsada originalmente por Andrés Federico Di Fiore, orientada al análisis de accesibilidad efectiva, asistencia preventiva y convivencia dentro del transporte público.

El repositorio no representa una implementación oficial vigente, una integración productiva con SUBE, una conexión real con organismos públicos, una modificación actual de validadoras, una base de datos médica ni un sistema de sanciones.

---

## 2. Estado documental del proyecto

La versión actual del repositorio debe leerse como una **versión documental 1.0**.

Esto significa que el proyecto cuenta con:

```text
introducción general
resumen ejecutivo
mapa de lectura
README actualizado
índice documental
arquitectura de referencia
guardrails técnicos
fundamentos jurídicos
fundamentos médicos
protección de datos personales
protocolo operativo conceptual
modelo de prueba piloto
estrategia legislativa y ciudadana
decisiones de arquitectura
principios de gobernanza
neutralidad institucional
política de marca
modelo de condiciones para donación y custodia
pliego técnico extendido
código demostrativo
API de ejemplo
tests básicos
Docker
```

La documentación debe interpretarse como una base pública, abierta y auditable para análisis, discusión, mejora y eventual evaluación institucional.

No constituye una implementación oficial, una integración productiva ni una adopción vigente por parte de organismos públicos o privados.

---

## 3. Lectura recomendada inicial

Para una primera aproximación al proyecto, se recomienda leer en este orden:

```text
1. INTRODUCCION_SUBE_PRIORIDAD.md
2. docs/RESUMEN_EJECUTIVO.md
3. docs/MAPA_DE_LECTURA.md
4. README.md
5. docs/INDICE_DOCUMENTAL.md
```

Este recorrido permite comprender primero la idea general, luego la síntesis institucional, después las rutas de lectura por perfil, más tarde la visión completa del repositorio y finalmente la organización documental detallada.

---

## 4. Documentos de entrada

### 4.1. Introducción general

Archivo:

```text
INTRODUCCION_SUBE_PRIORIDAD.md
```

Función:

Presenta SUBE Prioridad en lenguaje general, ciudadano y accesible.

Debe ser la primera lectura para personas que se acercan al proyecto sin conocimiento técnico, jurídico o institucional previo.

Explica:

- qué es SUBE Prioridad;
- por qué surge;
- cuál es el problema que intenta abordar;
- cuál es la idea central;
- qué no es el proyecto;
- cómo se protege la privacidad;
- qué rol cumple la tecnología;
- por qué no se trata de una implementación oficial vigente;
- cómo continuar la lectura del repositorio.

---

### 4.2. Resumen Ejecutivo

Archivo:

```text
docs/RESUMEN_EJECUTIVO.md
```

Función:

Presenta una síntesis institucional del proyecto ciudadano.

Está pensado para autoridades, legisladores, asesores, universidades, organizaciones sociales, periodistas, operadores de transporte y personas interesadas en evaluar la iniciativa de manera rápida pero seria.

Resume:

- síntesis del proyecto;
- naturaleza actual;
- problema abordado;
- enfoque general;
- separación entre acreditación y operación;
- privacidad;
- principios fundamentales;
- límites no negociables;
- rol del chofer;
- prueba piloto;
- indicadores;
- valor público;
- neutralidad institucional;
- gobernanza multi-actor;
- política de marca;
- donación y custodia;
- Bono Solidario como evolución futura separada;
- riesgos y mitigaciones documentales;
- regla general de interpretación.

---

### 4.3. Mapa de Lectura

Archivo:

```text
docs/MAPA_DE_LECTURA.md
```

Función:

Orienta la lectura del repositorio según el perfil de cada lector.

Debe consultarse cuando una persona necesita saber qué documentos leer según su rol, interés o nivel de profundidad.

El Mapa de Lectura es el documento específico para recorridos diferenciados por perfil.

---

### 4.4. README principal

Archivo:

```text
README.md
```

Función:

Es el documento madre del repositorio.

Explica la visión general, el estado del proyecto, el objetivo, el MVP, los principios rectores, la privacidad, los fundamentos jurídicos y médicos, el protocolo operativo, el estado técnico, los endpoints, la documentación estratégica, la neutralidad institucional, la política de marca, las condiciones para donación y custodia, la licencia y la declaración final.

Debe leerse como referencia general del proyecto.

---

## 5. Documentos técnicos y de arquitectura

### 5.1. Guardrails de arquitectura

Archivo:

```text
ARCHITECTURE_GUARDRAILS.md
```

Función:

Define los límites técnicos mínimos que toda evolución del código debe respetar.

Debe leerse antes de modificar componentes técnicos del repositorio.

Incluye criterios sobre:

- no procesamiento de datos sensibles en el core;
- separación entre acreditación y operación;
- no exposición de diagnósticos;
- simulación de interoperabilidad;
- no integración real sin autorización;
- no carga operativa indebida al chofer;
- no vigilancia;
- no sanciones;
- validación demostrativa;
- auditabilidad;
- seguridad;
- reversibilidad.

---

### 5.2. Arquitectura de referencia

Archivo:

```text
docs/ARQUITECTURA_DE_REFERENCIA.md
```

Función:

Describe la arquitectura conceptual, institucional y técnica del proyecto.

Permite comprender cómo SUBE Prioridad podría evolucionar desde un MVP conceptual hacia una eventual prueba piloto o implementación gradual, siempre sujeta a evaluación institucional.

Desarrolla:

- componentes principales;
- actores;
- flujos;
- capas de arquitectura;
- separación entre acreditación y operación;
- privacidad por diseño;
- interoperabilidad responsable;
- módulos futuros;
- riesgos;
- criterios de evolución.

---

### 5.3. Decisiones de arquitectura

Archivo:

```text
docs/DECISIONES_DE_ARQUITECTURA.md
```

Función:

Registra decisiones conceptuales y técnicas adoptadas durante la construcción del proyecto.

Sirve como memoria institucional del diseño.

Permite explicar por qué el proyecto adopta determinadas reglas, entre ellas:

- no usar DNI en el core;
- no almacenar diagnósticos;
- no convertir al chofer en evaluador;
- no integrar sistemas reales en esta etapa;
- usar simulaciones;
- separar acreditación y operación;
- mantener el Bono Solidario fuera del núcleo inicial;
- preservar gradualidad y reversibilidad.

---

### 5.4. Roadmap de implementación

Archivo:

```text
docs/ROADMAP_IMPLEMENTACION.md
```

Función:

Ordena una posible evolución gradual del proyecto.

No establece una implementación obligatoria, sino una hoja de ruta conceptual para análisis institucional.

Puede incluir etapas como:

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
```

Toda evolución debe estar sujeta a evaluación técnica, jurídica, médica, operativa, presupuestaria, institucional y social.

---

### 5.5. Pliego técnico extendido

Archivo:

```text
docs/PLIEGO_TECNICO_EXTENDIDO.md
```

Función:

Conserva la visión técnica amplia e integral del Programa SUBE Prioridad.

Debe interpretarse como documentación conceptual, prospectiva y evolutiva.

No representa una implementación productiva ni una integración real vigente con SUBE, organismos públicos, validadoras, hardware embarcado o infraestructura estatal.

Sirve como documento de referencia técnica extendida para análisis futuro.

---

## 6. Documentos jurídicos, médicos y de protección de datos

### 6.1. Fundamentos jurídicos

Archivo:

```text
docs/FUNDAMENTOS_JURIDICOS.md
```

Función:

Desarrolla el marco jurídico conceptual del proyecto.

Incluye fundamentos vinculados con:

- dignidad;
- igualdad real;
- accesibilidad;
- no discriminación;
- derechos de personas con discapacidad;
- derechos de personas mayores;
- personas gestantes;
- movilidad reducida;
- protección de datos personales;
- razonabilidad;
- progresividad;
- transporte público;
- evaluación institucional;
- prueba piloto.

Debe leerse como base para discusión jurídica, legislativa, administrativa e institucional.

---

### 6.2. Fundamentos médicos

Archivo:

```text
docs/FUNDAMENTOS_MEDICOS.md
```

Función:

Explica los fundamentos médicos, sanitarios y funcionales conceptuales del proyecto.

Aclara que SUBE Prioridad:

- no diagnostica;
- no reemplaza certificados;
- no evalúa clínicamente;
- no sustituye autoridades sanitarias;
- no convierte al transporte en un ámbito de revisión médica;
- no exige revelar diagnósticos.

Su finalidad es reconocer que muchas personas pueden necesitar viajar sentadas o recibir asistencia preventiva por razones permanentes, temporales, visibles o no visibles.

---

### 6.3. Protección de datos personales

Archivo:

```text
docs/PROTECCION_DATOS_PERSONALES.md
```

Función:

Define lineamientos de privacidad, minimización de datos y protección de información personal.

Es uno de los documentos centrales del proyecto.

Desarrolla:

- privacidad por diseño;
- minimización de datos;
- separación entre acreditación y operación;
- no procesamiento de diagnósticos en el core;
- no uso de DNI, nombre, domicilio o historia clínica en el núcleo operativo;
- interoperabilidad responsable;
- prueba piloto;
- riesgos de exposición;
- medidas de mitigación;
- evaluación institucional previa.

La regla central es:

```text
el transporte no necesita conocer el diagnóstico
```

---

## 7. Documentos operativos y de prueba piloto

### 7.1. Protocolo operativo conceptual

Archivo:

```text
docs/PROTOCOLO_OPERATIVO.md
```

Función:

Ordena cómo podría funcionar una eventual experiencia de asistencia preventiva en transporte público.

Incluye:

- roles;
- acreditación previa;
- atributo técnico de prioridad;
- preferencias de asistencia;
- modalidades de alerta;
- rol del chofer;
- comunicación a bordo;
- registro de eventos;
- incidentes;
- canales de reclamo;
- criterios de suspensión;
- capacitación mínima;
- evaluación operativa;
- informe final.

No constituye una instrucción operativa vigente.

Debe interpretarse como una guía conceptual adaptable para pruebas piloto, laboratorios técnicos o evaluaciones institucionales.

---

### 7.2. Modelo de prueba piloto

Archivo:

```text
docs/PRUEBA_PILOTO_MODELO.md
```

Función:

Propone una estructura conceptual para una prueba piloto limitada, voluntaria, temporal, reversible y auditable.

Una eventual prueba piloto debería ser:

- voluntaria;
- limitada;
- temporal;
- reversible;
- auditable;
- respetuosa de la privacidad;
- sin diagnósticos en el core;
- sin datos sensibles innecesarios;
- sin sanciones;
- sin sobrecarga al chofer;
- con indicadores definidos;
- con evaluación previa y posterior;
- con informe final.

---

## 8. Documentos institucionales, legislativos y ciudadanos

### 8.1. Dossier institucional breve

Archivo:

```text
docs/DOSSIER_INSTITUCIONAL_BREVE.md
```

Función:

Documento de síntesis para presentar el proyecto ante autoridades, legisladores, asesores, universidades, organizaciones sociales, operadores de transporte o ciudadanía.

Debe funcionar como material de acompañamiento para reuniones, notas, presentaciones o conversaciones institucionales.

---

### 8.2. Petitorio modelo

Archivo:

```text
docs/PETITORIO_MODELO.md
```

Función:

Modelo orientativo de petitorio ciudadano.

Puede utilizarse como base para acompañar firmas, presentaciones o solicitudes de evaluación institucional.

No constituye un formulario oficial ni sustituye la adaptación jurídica o administrativa que corresponda.

---

### 8.3. Modelo de proyecto de resolución

Archivo:

```text
docs/MODELO_PROYECTO_RESOLUCION.md
```

Función:

Modelo orientativo para impulsar formalmente la evaluación institucional de SUBE Prioridad.

Debe adaptarse a la jurisdicción, órgano, competencia y procedimiento correspondiente.

---

### 8.4. Estrategia legislativa y participación ciudadana

Archivo:

```text
docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md
```

Función:

Desarrolla una estrategia amplia para promover el análisis legislativo, administrativo, social e institucional del proyecto.

Incluye posibles líneas de acción para:

- legisladores;
- autoridades administrativas;
- organizaciones sociales;
- universidades;
- ciudadanía;
- organismos técnicos;
- espacios de participación pública;
- presentación de propuestas;
- eventual prueba piloto.

Debe leerse como una guía estratégica, no como una instrucción obligatoria.

---

## 9. Documentos de gobernanza, neutralidad, marca y custodia

### 9.1. Principios de gobernanza

Archivo:

```text
docs/PRINCIPIOS_DE_GOBERNANZA.md
```

Función:

Define criterios para proteger la finalidad pública, la transparencia, la neutralidad institucional, la privacidad, la auditabilidad y la continuidad del proyecto.

Incluye principios sobre:

- gobernanza plural;
- participación multi-actor;
- trazabilidad;
- rendición de cuentas;
- revisión institucional;
- protección de datos;
- evaluación de riesgos;
- gradualidad;
- reversibilidad;
- control ciudadano razonable;
- no apropiación partidaria;
- no uso electoral.

---

### 9.2. Neutralidad institucional y custodia pública

Archivo:

```text
docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md
```

Función:

Preserva el carácter ciudadano, abierto, no partidario, auditable y social del proyecto.

Debe leerse antes de cualquier:

- donación;
- adopción institucional;
- convenio;
- fork relevante;
- presentación pública;
- prueba piloto;
- uso institucional;
- transferencia;
- custodia neutral;
- uso de la identidad del proyecto.

Establece que SUBE Prioridad no debe transformarse en una herramienta de propaganda, vigilancia, sanción, apropiación partidaria, uso electoral o explotación comercial incompatible con sus principios fundacionales.

---

### 9.3. Política de marca

Archivo:

```text
docs/POLITICA_DE_MARCA.md
```

Función:

Define criterios para el uso responsable del nombre, marca, identidad, logotipos, denominaciones y referencias públicas vinculadas con SUBE Prioridad.

Aclara que la apertura del código y de la documentación no implica autorización automática para usar la marca de manera irrestricta.

La identidad pública del proyecto debe utilizarse sólo de forma compatible con:

- asistencia preventiva;
- privacidad por diseño;
- neutralidad institucional;
- código abierto;
- auditabilidad;
- finalidad social;
- atribución de origen;
- no uso electoral;
- no confusión institucional.

---

### 9.4. Modelo de condiciones para donación y custodia

Archivo:

```text
docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
```

Función:

Propone un modelo conceptual de condiciones mínimas para una eventual donación, cesión, transferencia, convenio, adopción institucional, autorización de uso de marca o custodia neutral.

No constituye un contrato vigente ni una donación aceptada.

Debe revisarse jurídicamente antes de cualquier uso formal.

Ordena condiciones sobre:

- finalidad pública;
- neutralidad no partidaria;
- atribución de origen;
- uso de marca;
- código abierto;
- protección de datos;
- separación entre acreditación y operación;
- rol del chofer;
- no vigilancia;
- no sanción;
- prueba piloto limitada;
- gobernanza multi-actor;
- auditoría;
- trazabilidad pública;
- proveedores privados;
- forks;
- incumplimientos;
- revisión jurídica previa.

---

## 10. Documentos técnicos de ejecución y código

### 10.1. Código demostrativo

Archivos principales:

```text
main.py
validator.py
cache_manager.py
circuit_breaker.py
xroad_gateway.py
```

Función:

Contienen componentes demostrativos del MVP técnico.

El código no procesa usuarios reales, no se conecta con organismos públicos, no modifica validadoras reales y no opera sobre infraestructura SUBE.

Debe leerse como una demostración técnica mínima de arquitectura conceptual.

---

### 10.2. Tests

Archivos principales:

```text
test_main.py
test_antifraud.py
```

Función:

Incluyen pruebas básicas para verificar comportamiento técnico del MVP.

Los tests deben mantener coherencia con los guardrails del proyecto.

---

### 10.3. Dependencias, Docker e integración continua

Archivos principales:

```text
requirements.txt
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
```

Función:

Permiten instalar dependencias, ejecutar el proyecto localmente, correr pruebas, usar Docker y mantener integración continua básica.

---

## 11. Documentos que deben leerse antes de una prueba piloto

Antes de cualquier prueba piloto real deberían revisarse, como mínimo:

```text
README.md
docs/RESUMEN_EJECUTIVO.md
docs/FUNDAMENTOS_JURIDICOS.md
docs/FUNDAMENTOS_MEDICOS.md
docs/PROTECCION_DATOS_PERSONALES.md
docs/PROTOCOLO_OPERATIVO.md
docs/PRUEBA_PILOTO_MODELO.md
ARCHITECTURE_GUARDRAILS.md
docs/ARQUITECTURA_DE_REFERENCIA.md
docs/PRINCIPIOS_DE_GOBERNANZA.md
docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md
docs/POLITICA_DE_MARCA.md
docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
```

Ninguna prueba piloto debería avanzar sin evaluación jurídica, técnica, operativa, médica, institucional y de protección de datos personales.

La prueba piloto debe ser limitada, voluntaria, temporal, reversible, auditable y respetuosa de la privacidad.

---

## 12. Documentos que deben leerse antes de una donación, cesión o adopción institucional

Antes de cualquier donación, cesión, transferencia, convenio, adopción institucional, autorización de uso de marca o custodia neutral, deberían revisarse:

```text
docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md
docs/POLITICA_DE_MARCA.md
docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
docs/PRINCIPIOS_DE_GOBERNANZA.md
docs/PROTECCION_DATOS_PERSONALES.md
README.md
docs/RESUMEN_EJECUTIVO.md
```

Estos documentos buscan evitar:

- apropiación partidaria;
- uso electoral;
- borramiento del origen ciudadano;
- uso irrestricto de marca;
- cierre opaco del código;
- explotación comercial incompatible;
- implementación sin evaluación;
- vigilancia;
- sanciones;
- sobrecarga al chofer;
- pérdida de trazabilidad pública.

---

## 13. Documentos que deben leerse antes de modificar código

Antes de modificar código, endpoints, validadores, simuladores o servicios, deberían revisarse:

```text
ARCHITECTURE_GUARDRAILS.md
README.md
docs/ARQUITECTURA_DE_REFERENCIA.md
docs/DECISIONES_DE_ARQUITECTURA.md
docs/PROTECCION_DATOS_PERSONALES.md
docs/PRINCIPIOS_DE_GOBERNANZA.md
```

Toda modificación técnica debe respetar los guardrails fundacionales del proyecto.

El código no debe evolucionar hacia modelos que impliquen:

- tratamiento de datos sensibles reales;
- almacenamiento de diagnósticos;
- exposición de identidad personal;
- conexión real con organismos públicos sin autorización;
- modificación de validadoras reales;
- sanciones automáticas;
- vigilancia;
- sobrecarga del personal de conducción;
- alteración del sistema de cobro;
- sustitución de derechos vigentes.

---

## 14. Lectura por perfil

Para recorridos detallados según perfil de lector, debe consultarse:

```text
docs/MAPA_DE_LECTURA.md
```

Ese documento organiza lecturas sugeridas para:

- ciudadanía;
- autoridades públicas;
- legisladores y asesores;
- equipos técnicos;
- abogados;
- especialistas en protección de datos;
- profesionales de salud y accesibilidad;
- organizaciones sociales;
- operadores de transporte;
- universidades;
- prensa y comunicación;
- potenciales custodios institucionales.

Este índice no reemplaza el Mapa de Lectura.

El índice organiza los documentos disponibles.

El Mapa de Lectura orienta qué leer según el perfil, rol o necesidad de cada persona.

---

## 15. Orden sugerido para revisión institucional completa

Para una revisión institucional completa, se recomienda este orden:

```text
1. INTRODUCCION_SUBE_PRIORIDAD.md
2. docs/RESUMEN_EJECUTIVO.md
3. README.md
4. docs/INDICE_DOCUMENTAL.md
5. docs/MAPA_DE_LECTURA.md
6. docs/FUNDAMENTOS_JURIDICOS.md
7. docs/FUNDAMENTOS_MEDICOS.md
8. docs/PROTECCION_DATOS_PERSONALES.md
9. docs/PROTOCOLO_OPERATIVO.md
10. docs/PRUEBA_PILOTO_MODELO.md
11. ARCHITECTURE_GUARDRAILS.md
12. docs/ARQUITECTURA_DE_REFERENCIA.md
13. docs/DECISIONES_DE_ARQUITECTURA.md
14. docs/ROADMAP_IMPLEMENTACION.md
15. docs/PRINCIPIOS_DE_GOBERNANZA.md
16. docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md
17. docs/POLITICA_DE_MARCA.md
18. docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
19. docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md
20. docs/PLIEGO_TECNICO_EXTENDIDO.md
```

Este orden permite avanzar desde la comprensión general hacia la evaluación jurídica, médica, operativa, técnica, institucional y estratégica.

---

## 16. Advertencias documentales relevantes

SUBE Prioridad no debe ser presentado como:

- implementación oficial vigente;
- sistema SUBE modificado;
- solución ya adoptada por organismos públicos;
- sistema nacional activo;
- beneficio tarifario;
- subsidio;
- sistema de sanciones;
- sistema de vigilancia;
- base de datos médica;
- herramienta de diagnóstico;
- obligación para choferes;
- obligación para pasajeros;
- ranking público;
- mecanismo de denuncia social;
- plataforma cerrada;
- producto comercial incompatible con su finalidad social.

El uso de la denominación SUBE Prioridad no implica autorización oficial, adopción vigente ni vinculación institucional actual con el sistema SUBE o sus operadores.

---

## 17. Regla general de interpretación documental

Todo el repositorio debe interpretarse bajo estas reglas:

```text
MVP conceptual
versión documental 1.0
no implementación oficial vigente
no integración real con SUBE
no conexión real con organismos públicos
no procesamiento de datos sensibles reales
no diagnóstico médico en el core
no modificación actual de validadoras reales
no alteración del sistema de cobro
no beneficio tarifario
no subsidio
no sanciones
no vigilancia
no ranking público
no obligación nueva para pasajeros
no sobrecarga al chofer
no sustitución de derechos existentes
no apropiación partidaria
no uso electoral
no uso irrestricto de marca
no donación o transferencia sin condiciones fundacionales
implementación sólo mediante evaluación institucional competente
```

---

## 18. Atribución de origen

SUBE Prioridad es una iniciativa ciudadana impulsada originalmente por Andrés Federico Di Fiore.

La atribución de origen debe preservarse en toda presentación, fork, evaluación institucional, donación, convenio, adopción futura, comunicación pública o documentación derivada.

La apertura del repositorio no implica autorización para borrar el origen ciudadano del proyecto.

La eventual adopción institucional no debería transformar una iniciativa ciudadana abierta en una herramienta cerrada, partidaria, propagandística, comercialmente apropiada o incompatible con sus principios fundacionales.

---

## 19. Relación entre documentación y código

El código demostrativo debe interpretarse a la luz de la documentación estratégica.

En caso de duda, prevalecen los principios fundacionales:

```text
privacidad por diseño
minimización de datos
separación entre acreditación y operación
no exposición de diagnósticos
no vigilancia
no sanción
no sobrecarga al chofer
no sustitución de derechos vigentes
neutralidad institucional
trazabilidad pública
```

El código no debe evolucionar en sentido contrario a esos principios.

Las simulaciones, endpoints, validadores, servicios y módulos futuros deben conservar coherencia con la finalidad social, la protección de datos personales y la arquitectura conceptual del proyecto.

---

## 20. Cierre

Este índice documental organiza la versión documental 1.0 de SUBE Prioridad.

El proyecto debe leerse como una propuesta ciudadana abierta, prudente, documentada, auditable y orientada al interés público.

Su objetivo es aportar una base para analizar si una arquitectura tecnológica responsable puede contribuir a una experiencia de transporte público más segura, digna y respetuosa, facilitando asistencia preventiva sin exponer diagnósticos, sin alterar derechos existentes, sin imponer sanciones, sin sobrecargar al personal de conducción y sin transformar la tecnología en una herramienta de vigilancia o propaganda.

La lectura integral del repositorio debe preservar siempre el carácter ciudadano, abierto, no partidario, auditable y social del proyecto.

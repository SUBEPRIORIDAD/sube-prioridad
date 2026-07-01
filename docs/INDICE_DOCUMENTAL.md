# Índice Documental — SUBE Prioridad

## Propósito del índice

Este documento organiza la documentación principal del repositorio SUBE Prioridad.

Su finalidad es facilitar la lectura, navegación, evaluación institucional y comprensión pública del proyecto.

SUBE Prioridad debe interpretarse como una propuesta ciudadana de innovación pública, de código abierto, orientada a explorar una arquitectura de asistencia preventiva en transporte público.

El repositorio contiene un MVP conceptual, técnico y demostrativo. No constituye una implementación oficial vigente, una integración real con sistemas SUBE, organismos públicos, validadoras, hardware embarcado ni infraestructura estatal.

---

## Lectura recomendada

Para comprender el proyecto de manera ordenada, se recomienda leer los documentos en este orden:

1. `README.md`
2. `ARCHITECTURE_GUARDRAILS.md`
3. `docs/ARQUITECTURA_DE_REFERENCIA.md`
4. `docs/ROADMAP_IMPLEMENTACION.md`
5. `docs/DECISIONES_DE_ARQUITECTURA.md`
6. `docs/PRINCIPIOS_DE_GOBERNANZA.md`
7. `docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md`
8. `docs/POLITICA_DE_MARCA.md`
9. `docs/PROTECCION_DATOS_PERSONALES.md`
10. `docs/PROTOCOLO_OPERATIVO.md`
11. `docs/PRUEBA_PILOTO_MODELO.md`
12. `docs/FUNDAMENTOS_JURIDICOS.md`
13. `docs/FUNDAMENTOS_MEDICOS.md`
14. `docs/DOSSIER_INSTITUCIONAL_BREVE.md`
15. `docs/MODELO_PROYECTO_RESOLUCION.md`
16. `docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md`
17. `docs/PLIEGO_TECNICO_EXTENDIDO.md`

---

## README.md

Documento principal de entrada al repositorio.

Explica qué es SUBE Prioridad, cuál es su alcance actual, qué componentes contiene el MVP, qué límites tiene el proyecto y cómo debe interpretarse públicamente.

Debe leerse como la presentación general del proyecto.

Puntos centrales:

- MVP conceptual y demostrativo.
- Propuesta ciudadana de innovación pública.
- Privacidad por diseño.
- No procesamiento de datos sensibles.
- Integraciones externas simuladas.
- No implementación oficial vigente.
- No modificación actual del sistema SUBE.
- No imposición de nuevas cargas al chofer.
- No sustitución del régimen vigente de asientos prioritarios.
- Neutralidad institucional.
- No apropiación partidaria.
- Política de marca.
- Preservación de atribución de origen.

---

## ARCHITECTURE_GUARDRAILS.md

Define los límites técnicos y conceptuales que el código del repositorio no debe vulnerar.

Funciona como regla madre de arquitectura para preservar la coherencia del MVP.

Establece:

- naturaleza conceptual del MVP;
- datos prohibidos en el core;
- modelo correcto de atributo técnico de prioridad;
- interoperabilidad simulada;
- límites del Bono Solidario;
- separación entre documentación, simulación y producción;
- regla de cambios seguros;
- criterio de mínima intervención.

Debe consultarse antes de modificar código o documentación técnica.

---

## docs/ARQUITECTURA_DE_REFERENCIA.md

Describe la arquitectura conceptual de referencia de SUBE Prioridad.

No constituye una arquitectura productiva obligatoria, una especificación cerrada ni una integración real vigente.

Explica el modelo general del sistema:

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
evaluación institucional agregada
```

Incluye principios de diseño, separación entre acreditación y operación, módulos conceptuales, privacidad por arquitectura, interoperabilidad responsable, escalabilidad gradual y relación con el MVP actual.

Debe leerse como el documento técnico-institucional central de la versión 1.0.

---

## docs/ROADMAP_IMPLEMENTACION.md

Presenta una hoja de ruta conceptual para la evolución progresiva de SUBE Prioridad.

No constituye un cronograma obligatorio ni una decisión administrativa.

Ordena el crecimiento posible del proyecto en etapas:

```text
investigación y documentación
↓
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
modelo adaptable a otras jurisdicciones
```

Cada fase requiere evaluación previa, autorización institucional, análisis jurídico, protección de datos y revisión operativa.

Debe leerse como guía de evolución prudente, gradual, reversible y auditable.

---

## docs/DECISIONES_DE_ARQUITECTURA.md

Registra las principales decisiones de arquitectura adoptadas para el desarrollo conceptual y técnico de SUBE Prioridad.

Explica por qué el proyecto utiliza:

- atributo técnico de prioridad en lugar de diagnóstico médico;
- separación entre acreditación y operación;
- privacidad por diseño;
- interoperabilidad simulada en el MVP;
- neutralidad tecnológica;
- implementación gradual, reversible y auditable;
- alertas genéricas y no diagnósticas;
- preferencias de asistencia controladas por el usuario;
- registros mínimos y evaluación agregada;
- Bono Solidario como evolución futura;
- protección del rol del chofer;
- tests y compilación como regla de cambio seguro.

Debe leerse como criterio de diseño para orientar la evolución del MVP, la documentación técnica y eventuales pruebas piloto.

---

## docs/PRINCIPIOS_DE_GOBERNANZA.md

Establece criterios de gobernanza para orientar la evaluación, evolución e implementación progresiva de SUBE Prioridad.

Define principios de:

- competencia institucional;
- evaluación previa;
- gradualidad;
- reversibilidad;
- auditabilidad;
- transparencia;
- responsabilidad institucional;
- protección de datos;
- participación ciudadana;
- neutralidad tecnológica;
- gestión de incidentes;
- gobernanza documental;
- gobernanza del código;
- gobernanza federal;
- adaptación internacional.

Debe leerse como guía conceptual para eventuales pruebas piloto o implementaciones de mayor escala.

No constituye una norma jurídica ni una estructura institucional obligatoria.

---

## docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md

Establece criterios para preservar el carácter ciudadano, abierto, social, no partidario y auditable de SUBE Prioridad.

Su finalidad es prevenir usos incompatibles con la voluntad original de Andrés Federico Di Fiore, tales como apropiación partidaria, uso electoral, cierre opaco del código, explotación comercial incompatible, eliminación de atribución, uso indebido de la marca o implementación sin respeto de los guardrails fundacionales.

Define principios sobre:

- neutralidad no partidaria;
- atribución de origen;
- código abierto y transparencia;
- evaluación de copyleft;
- licencia documental;
- política de marca;
- donación con cargo o transferencia condicionada;
- comité de gobernanza multi-actor;
- política de Estado transversal;
- trazabilidad pública;
- forks y adaptaciones;
- prohibición de confusión institucional;
- prohibición de uso electoral;
- rol del fundador;
- entidad de custodia neutral.

Debe leerse antes de cualquier donación, convenio, adopción institucional, prueba piloto, fork relevante o presentación pública del proyecto.

---

## docs/POLITICA_DE_MARCA.md

Establece criterios para el uso responsable del nombre, identidad, denominación, logotipos, isotipos, pictogramas, materiales visuales y referencias públicas vinculadas con SUBE Prioridad.

Su finalidad es preservar el carácter ciudadano, abierto, social, no partidario, auditable y orientado al interés público del proyecto impulsado originalmente por Andrés Federico Di Fiore.

Aclara que la apertura del código o de la documentación no implica autorización automática para utilizar la marca o identidad visual de forma irrestricta.

Define criterios sobre:

- uso responsable de la denominación SUBE Prioridad;
- atribución de origen;
- usos permitidos sin autorización especial;
- usos que requieren autorización o revisión previa;
- usos prohibidos;
- uso por organismos públicos;
- uso por legisladores, partidos o bloques políticos;
- uso por proveedores privados;
- uso por universidades y organizaciones sociales;
- forks y proyectos derivados;
- prohibición de confusión institucional;
- identidad visual;
- registro marcario;
- política de autorización;
- revocación o cese de uso;
- relación entre código abierto y marca;
- relación con donación o adopción institucional.

Debe leerse antes de cualquier uso institucional, público, comercial, partidario, legislativo, comunicacional o derivado de la identidad SUBE Prioridad.

---

## docs/PROTECCION_DATOS_PERSONALES.md

Desarrolla el enfoque de protección de datos personales aplicable a SUBE Prioridad.

Su eje es que el core operativo no debe procesar diagnósticos médicos, historia clínica, DNI, nombre, domicilio ni certificados médicos en texto plano.

Establece principios de:

- privacidad por diseño;
- minimización de datos;
- finalidad determinada;
- pseudoanonimización;
- separación entre acreditación y operación;
- seguridad de la información;
- registros mínimos;
- evaluación agregada;
- no exposición pública de condiciones sensibles.

Debe leerse como documento central para evaluar la viabilidad jurídica y ética del proyecto.

---

## docs/PROTOCOLO_OPERATIVO.md

Describe un protocolo operativo conceptual para una eventual prueba piloto o implementación controlada.

Ordena roles, etapas y límites prácticos del sistema.

Incluye criterios sobre:

- usuarios voluntarios;
- acreditación previa fuera del core;
- activación del atributo técnico;
- preferencias de asistencia;
- alertas genéricas;
- rol limitado del chofer;
- colaboración voluntaria de pasajeros;
- gestión de incidentes;
- canales de reclamo;
- evaluación agregada;
- criterios de suspensión o revisión.

Debe leerse como una guía operativa prudente, no como una orden de implementación.

---

## docs/PRUEBA_PILOTO_MODELO.md

Propone un modelo conceptual de prueba piloto limitada, voluntaria, reversible y auditable.

La prueba piloto debe servir para evaluar si un atributo técnico de prioridad puede facilitar asistencia preventiva sin revelar datos sensibles ni alterar el régimen vigente de transporte.

Incluye criterios sobre:

- alcance territorial;
- duración;
- autoridad responsable;
- selección voluntaria de participantes;
- datos excluidos del core;
- modalidad de asistencia;
- indicadores;
- incidentes;
- reclamos;
- evaluación final;
- criterios de continuidad, ajuste o cierre.

Debe leerse como el documento base para presentar una primera experiencia controlada.

---

## docs/FUNDAMENTOS_JURIDICOS.md

Reúne fundamentos jurídicos para analizar la compatibilidad de SUBE Prioridad con derechos, garantías y marcos normativos aplicables.

Su enfoque principal es presentar el proyecto como herramienta complementaria de accesibilidad efectiva, no como sustitución de derechos existentes.

Aborda, entre otros ejes:

- igualdad real;
- accesibilidad;
- ajustes razonables;
- dignidad;
- autonomía personal;
- protección de datos;
- no discriminación;
- derecho al transporte;
- derechos de personas con discapacidad;
- límites del rol del chofer;
- voluntariedad;
- proporcionalidad;
- gradualidad;
- evaluación institucional.

Debe leerse como fundamento argumental para evaluación legislativa, administrativa o institucional.

---

## docs/FUNDAMENTOS_MEDICOS.md

Desarrolla fundamentos médicos, funcionales y preventivos vinculados con la necesidad de viajar sentado en determinadas situaciones.

No debe leerse como guía clínica, protocolo médico ni criterio automático de admisión.

Su finalidad es explicar que existen condiciones visibles y no visibles que pueden hacer razonable una asistencia preventiva en el transporte público.

Debe preservar el principio central del proyecto:

```text
el sistema operativo no necesita conocer el diagnóstico
```

Lo relevante para el MVP no es la enfermedad específica, sino la existencia de una necesidad previamente acreditada de asistencia durante el viaje.

---

## docs/DOSSIER_INSTITUCIONAL_BREVE.md

Documento ejecutivo de presentación institucional.

Resume el proyecto en lenguaje claro para autoridades, legisladores, municipios, organismos públicos, universidades, organizaciones sociales, operadores de transporte y ciudadanía.

Debe servir como primera lectura institucional cuando no sea posible revisar toda la documentación técnica.

Explica:

- qué es SUBE Prioridad;
- qué problema busca abordar;
- cómo funciona conceptualmente;
- qué datos no procesa;
- qué límites respeta;
- por qué puede evaluarse mediante prueba piloto;
- cuál es su valor público.

---

## docs/MODELO_PROYECTO_RESOLUCION.md

Modelo conceptual de proyecto de resolución o acto administrativo para promover la evaluación institucional de SUBE Prioridad.

No constituye una norma vigente ni una presentación oficial por sí misma.

Su finalidad es ofrecer una base de redacción para que una autoridad competente pueda, si lo considera adecuado, impulsar:

- una mesa técnica;
- un estudio de factibilidad;
- una prueba piloto;
- una evaluación de privacidad;
- una convocatoria a actores relevantes;
- un informe de viabilidad.

Debe adaptarse siempre a la jurisdicción, competencia y procedimiento aplicable.

---

## docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md

Desarrolla una estrategia para presentar SUBE Prioridad ante legisladores, autoridades administrativas, organismos públicos, universidades, organizaciones sociales, cámaras, municipios y ciudadanía.

Su objetivo no es solicitar una implementación inmediata, obligatoria o nacional, sino promover evaluación, diálogo institucional, prueba piloto y participación pública.

Incluye criterios sobre:

- narrativa pública;
- actores destinatarios;
- etapas de incidencia;
- participación ciudadana;
- comunicación institucional;
- riesgos discursivos;
- lenguaje prudente;
- articulación con organizaciones;
- escalabilidad política.

Debe leerse como guía de posicionamiento público e institucional del proyecto.

---

## docs/PLIEGO_TECNICO_EXTENDIDO.md

Conserva el pliego técnico extendido y la visión integral original del Programa SUBE Prioridad.

Debe interpretarse como documentación conceptual, prospectiva y evolutiva.

No representa una implementación productiva, una integración real vigente con SUBE, organismos públicos, validadoras, hardware embarcado ni infraestructura estatal.

Su lectura debe realizarse junto con:

- `README.md`;
- `ARCHITECTURE_GUARDRAILS.md`;
- `docs/ARQUITECTURA_DE_REFERENCIA.md`;
- `docs/ROADMAP_IMPLEMENTACION.md`;
- `docs/DECISIONES_DE_ARQUITECTURA.md`;
- `docs/PRINCIPIOS_DE_GOBERNANZA.md`;
- `docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md`;
- `docs/POLITICA_DE_MARCA.md`;
- `docs/PROTECCION_DATOS_PERSONALES.md`.

Este documento conserva la visión técnica original, pero debe quedar subordinado a los límites actuales del MVP y a la nota de alcance incluida al inicio del propio archivo.

---

## Documentos técnicos de código

Además de la documentación institucional, el repositorio contiene archivos de código y configuración que integran el MVP conceptual.

Entre ellos:

- `main.py`;
- `validator.py`;
- `cache_manager.py`;
- `circuit_breaker.py`;
- `xroad_gateway.py`;
- `test_main.py`;
- `test_antifraud.py`;
- `requirements.txt`;
- `.github/workflows/ci.yml`;
- `docker-compose.yml`;
- `Dockerfile`, si corresponde.

Estos archivos deben interpretarse como implementación demostrativa y simulada.

No deben incorporar datos reales ni integraciones productivas sin autorización, documentación técnica, marco jurídico y evaluación institucional suficiente.

---

## Regla de interpretación general

Todo el repositorio debe interpretarse bajo las siguientes reglas:

```text
MVP conceptual
no implementación oficial vigente
no integración real con SUBE
no conexión real con organismos públicos
no procesamiento de datos sensibles
no diagnóstico médico en el core
no modificación actual de validadoras reales
no alteración del cobro del transporte
no sanciones automáticas
no nuevas cargas indebidas al chofer
no sustitución de derechos vigentes
no apropiación partidaria
no uso electoral
no cierre opaco del código
no uso irrestricto de marca
no explotación comercial incompatible con el interés público
```

---

## Núcleo funcional del MVP

La versión 1.0 documenta y demuestra este núcleo conceptual:

```text
persona con necesidad previamente acreditada
↓
atributo técnico de prioridad
↓
preferencia de asistencia
↓
validación demostrativa
↓
alerta genérica, discreta o visible
↓
colaboración voluntaria o asistencia preventiva
↓
evaluación agregada
```

El sistema no debe revelar la causa médica, funcional o personal de la prioridad.

---

## Criterios para prueba piloto

Una eventual prueba piloto debería ser:

- limitada;
- voluntaria;
- reversible;
- auditable;
- institucionalmente autorizada;
- territorialmente acotada;
- técnicamente controlada;
- respetuosa de la privacidad;
- sin diagnósticos en el core;
- sin obligación de colaboración;
- sin sanciones;
- sin sobrecarga al chofer;
- con indicadores agregados;
- con canales de reclamo;
- con informe final.

La primera meta no es una implementación nacional inmediata, sino evaluar si el modelo de asistencia preventiva resulta útil, aceptable, seguro y respetuoso de derechos.

---

## Bono Solidario

El Bono Solidario debe considerarse una evolución futura.

No forma parte del núcleo indispensable del MVP inicial.

Su eventual análisis requiere reglas específicas de:

- voluntariedad;
- privacidad;
- antifraude;
- no discriminación;
- no vigilancia;
- no presión social;
- no afectación del régimen legal de asientos prioritarios;
- evaluación institucional previa.

No debe implementarse como multa, sanción, ranking público ni mecanismo de control entre pasajeros.

---

## Neutralidad institucional y custodia pública

SUBE Prioridad debe preservar su carácter de iniciativa ciudadana abierta, no partidaria, auditable y orientada al interés público.

Su eventual evaluación, donación, adopción institucional, prueba piloto, fork o presentación pública no debe implicar apropiación partidaria, uso electoral, cierre opaco del código, eliminación de la atribución de origen ni explotación comercial incompatible con sus principios fundacionales.

El documento específico sobre esta materia es:

`docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md`

Debe leerse antes de cualquier transferencia, convenio, donación con cargo, política de marca, uso institucional de la identidad SUBE Prioridad o adopción por terceros.

---

## Política de marca

La apertura del código y de la documentación no implica autorización automática para utilizar la marca, nombre, logotipos, identidad visual o denominaciones vinculadas con SUBE Prioridad de manera irrestricta.

La marca debe utilizarse únicamente de manera compatible con la finalidad original del proyecto: asistencia preventiva, privacidad por diseño, neutralidad institucional, código abierto, auditabilidad, finalidad social y atribución de origen.

El documento específico sobre esta materia es:

`docs/POLITICA_DE_MARCA.md`

Debe leerse antes de cualquier uso institucional, público, comercial, partidario, legislativo, comunicacional o derivado de la identidad SUBE Prioridad.

---

## Declaración de cierre documental v1.0

La versión documental 1.0 de SUBE Prioridad consolida el repositorio como una propuesta ciudadana de innovación pública, de código abierto, orientada a evaluar una arquitectura de asistencia preventiva en el transporte público argentino.

Su propósito es aportar una base técnica, jurídica, médica, operativa, institucional y documental para que las autoridades competentes, organizaciones sociales, universidades, operadores y ciudadanía puedan analizar la viabilidad de una prueba piloto limitada, voluntaria, reversible y auditable.

SUBE Prioridad no pretende imponer una solución cerrada ni afirmar una implementación vigente.

Propone explorar si una necesidad previamente acreditada puede representarse mediante un atributo técnico de prioridad, mínimo y no sensible, que facilite asistencia preventiva sin exponer diagnósticos, sin alterar el sistema de cobro, sin sustituir derechos existentes y sin trasladar cargas indebidas al personal de conducción.

La apertura del proyecto no habilita su apropiación partidaria, su uso electoral, el uso irrestricto de su marca, el borramiento de su origen ciudadano ni su transformación en una herramienta de vigilancia, sanción, negocio cerrado o propaganda institucional incompatible con sus principios fundacionales.

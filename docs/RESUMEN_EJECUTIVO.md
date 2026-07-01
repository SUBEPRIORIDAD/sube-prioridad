# Resumen Ejecutivo — SUBE Prioridad

## Documento institucional de presentación, análisis y evaluación del proyecto ciudadano

---

## 1. Síntesis del proyecto

SUBE Prioridad es una iniciativa ciudadana de innovación pública impulsada originalmente por Andrés Federico Di Fiore como propuesta ciudadana independiente.

La propuesta busca analizar cómo una herramienta tecnológica, diseñada bajo principios de accesibilidad, privacidad, protección de datos personales y gradualidad institucional, podría contribuir a mejorar la experiencia de viaje de personas que cuentan con una necesidad previamente acreditada de viajar sentadas o recibir asistencia preventiva dentro del transporte público.

El proyecto propone estudiar una arquitectura complementaria al sistema existente, donde una necesidad reconocida pueda representarse mediante un atributo técnico de prioridad, evitando la exposición pública de diagnósticos, condiciones médicas, historia clínica o información personal sensible.

SUBE Prioridad no busca reemplazar derechos vigentes, modificar actualmente el sistema SUBE, crear beneficios tarifarios, generar sanciones ni trasladar nuevas cargas operativas al personal de conducción.

Su objetivo es aportar una base documentada para análisis técnico, jurídico, institucional, médico, operativo y social.

---

## 2. Estado actual del proyecto

El estado actual de SUBE Prioridad es:

```text
MVP conceptual: sí
Código demostrativo: sí
API de ejemplo: sí
Documentación técnica: sí
Fundamentos jurídicos: sí
Fundamentos médicos: sí
Protección de datos personales: sí
Protocolo operativo conceptual: sí
Modelo de prueba piloto: sí
Gobernanza: sí
Neutralidad institucional: sí
Política de marca: sí
Modelo de condiciones para donación y custodia: sí

Implementación oficial vigente: no
Integración real con SUBE: no
Integración real con organismos públicos: no
Procesamiento de datos sensibles reales: no
Modificación actual de validadoras: no
```

La versión actual del repositorio debe interpretarse como una **versión documental 1.0**, conceptual, demostrativa y abierta a evaluación institucional.

No representa una implementación productiva ni una integración vigente con infraestructura pública.

---

## 3. El problema que busca abordar

En el transporte público existen personas que pueden necesitar viajar sentadas o recibir asistencia preventiva por diferentes motivos, incluyendo situaciones permanentes, temporales, visibles o no visibles.

Aunque existen mecanismos de prioridad y accesibilidad, en la práctica pueden presentarse dificultades:

- desconocimiento de otros pasajeros;
- necesidad de explicar públicamente una situación personal;
- incomodidad al solicitar asistencia;
- conflictos derivados de la falta de información;
- situaciones donde una persona necesita ayuda pero evita solicitarla;
- exposición innecesaria de datos personales o condiciones sensibles;
- dificultad para ejercer derechos existentes de manera efectiva y digna.

SUBE Prioridad parte de una pregunta central:

> ¿Puede una herramienta tecnológica facilitar el ejercicio efectivo de una prioridad existente sin exponer a la persona usuaria?

---

## 4. La propuesta conceptual

El modelo central del proyecto se basa en separar dos planos:

### Acreditación

La determinación de una necesidad de prioridad corresponde a los mecanismos, organismos, profesionales o procedimientos que definan las autoridades competentes.

El sistema tecnológico no diagnostica, no evalúa condiciones médicas, no revisa certificados y no decide quién merece prioridad.

### Operación

Una vez acreditada una necesidad por fuera del core operativo, el sistema podría representar esa condición mediante un atributo técnico mínimo, orientado únicamente a facilitar asistencia preventiva.

Conceptualmente:

```text
necesidad previamente acreditada
↓
atributo técnico protegido
↓
preferencia de asistencia
↓
validación demostrativa
↓
asistencia preventiva
↓
mejor experiencia de viaje
```

La arquitectura busca que el transporte no tenga que conocer el diagnóstico, sino únicamente una condición operativa de prioridad previamente validada por el canal competente.

---

## 5. Principios fundamentales

SUBE Prioridad se estructura sobre los siguientes principios:

### Privacidad por diseño

El sistema debe utilizar solamente la información necesaria para cumplir su finalidad.

No requiere exponer diagnósticos, historias clínicas, certificados médicos en texto plano ni información médica personal.

### Minimización de datos

La arquitectura busca evitar almacenar o procesar información sensible innecesaria.

La regla central es:

```text
el transporte no necesita conocer el diagnóstico
necesita conocer únicamente una condición operativa de prioridad
```

### Accesibilidad efectiva

El objetivo no es crear nuevos derechos ni sustituir derechos vigentes, sino analizar herramientas que puedan facilitar el ejercicio práctico de derechos existentes.

### Gradualidad

Cualquier evolución debería realizarse mediante etapas:

```text
MVP conceptual
↓
evaluación técnica
↓
laboratorio o entorno controlado
↓
prueba piloto limitada
↓
análisis de resultados
↓
eventual implementación progresiva
```

### Reversibilidad

Toda prueba piloto o implementación progresiva debería poder revisarse, corregirse, suspenderse o cerrarse si no cumple sus objetivos o si genera riesgos no previstos.

### Auditabilidad

El proyecto debe poder ser analizado técnica, jurídica, operativa, institucional y socialmente.

---

## 6. Qué es SUBE Prioridad

SUBE Prioridad es:

- una propuesta ciudadana de innovación pública;
- un MVP conceptual y demostrativo;
- una arquitectura de referencia;
- una base para evaluación institucional;
- una propuesta gradual, reversible y auditable;
- un modelo orientado a privacidad y accesibilidad;
- una herramienta conceptual para analizar asistencia preventiva en transporte público;
- una iniciativa abierta impulsada originalmente por Andrés Federico Di Fiore.

---

## 7. Qué no es SUBE Prioridad

SUBE Prioridad no es:

- una implementación oficial vigente;
- una modificación actual del sistema SUBE;
- una integración real actualmente operativa con organismos públicos;
- un sistema de sanciones;
- un beneficio tarifario;
- un subsidio;
- una base de datos médica;
- una herramienta de diagnóstico;
- un sistema de vigilancia;
- una obligación nueva para choferes;
- un reemplazo del régimen de asientos prioritarios;
- una solución cerrada;
- una implementación nacional inmediata.

Tampoco representa una integración actual con organismos públicos, registros estatales, validadoras, hardware embarcado o infraestructura operativa.

El uso de la denominación SUBE Prioridad no implica autorización oficial, adopción vigente ni vinculación institucional actual con el sistema SUBE o sus operadores.

---

## 8. Arquitectura institucional propuesta

La iniciativa distingue tres niveles:

```text
Nivel institucional

Acreditación de la necesidad
Definición de requisitos
Supervisión normativa
Protección de derechos

↓
Nivel tecnológico

Atributo técnico
Validación demostrativa
Preferencias de asistencia
Minimización de datos

↓
Nivel operativo

Experiencia de viaje
Asistencia preventiva
Colaboración voluntaria
Evaluación agregada
```

Esta separación busca evitar que el sistema operativo acceda a información sensible que no necesita.

---

## 9. Rol del personal de conducción

SUBE Prioridad considera fundamental preservar el rol del conductor.

El sistema no debe convertir al personal de conducción en:

- evaluador médico;
- fiscalizador documental;
- administrador de datos sensibles;
- árbitro principal de conflictos personales;
- responsable de decidir quién merece asistencia;
- aplicador de sanciones;
- gestor de beneficios.

La finalidad es reducir fricciones, no trasladar nuevas responsabilidades operativas al personal de conducción.

La conducción segura debe conservar prioridad.

---

## 10. Participación ciudadana y convivencia

La propuesta reconoce que la tecnología no reemplaza la convivencia social.

La asistencia entre pasajeros debe continuar siendo voluntaria, solidaria y respetuosa.

El sistema no debe generar:

- sanciones;
- castigos;
- exposición pública;
- presión social indebida;
- rankings públicos;
- vigilancia entre pasajeros;
- multas encubiertas;
- mecanismos de denuncia social.

SUBE Prioridad busca facilitar asistencia preventiva, no imponer conductas mediante coerción tecnológica.

---

## 11. Modelo de prueba piloto

Una eventual evaluación debería contemplar una prueba piloto:

- limitada;
- voluntaria;
- temporal;
- reversible;
- auditable;
- respetuosa de la privacidad;
- con indicadores definidos;
- con evaluación previa y posterior;
- sin diagnósticos en el core;
- sin datos sensibles innecesarios;
- sin obligación de colaboración;
- sin sanciones;
- sin sobrecarga al chofer;
- con canales de reclamo;
- con informe final.

La finalidad de un piloto sería obtener evidencia antes de considerar cualquier evolución.

El objetivo inicial no es implementar nacionalmente el sistema, sino evaluar utilidad, aceptación, riesgos, impacto operativo, privacidad y viabilidad institucional.

---

## 12. Valor potencial de la iniciativa

SUBE Prioridad busca explorar una combinación entre:

- innovación tecnológica;
- accesibilidad efectiva;
- privacidad;
- dignidad;
- participación ciudadana;
- diseño institucional;
- protección de datos;
- gobernanza pública;
- convivencia en el transporte.

El valor principal del proyecto no está únicamente en el software, sino en la arquitectura conceptual que propone:

```text
usar tecnología para facilitar asistencia
sin convertirla en exposición, control o vigilancia
```

La tecnología se plantea como herramienta de apoyo institucional, no como sustituto de normas, derechos existentes ni responsabilidad humana.

El proyecto aporta una base para discutir cómo mejorar la accesibilidad real en el transporte público sin obligar a las personas a revelar públicamente su situación personal.

---

## 13. Neutralidad institucional y custodia pública

SUBE Prioridad debe preservar su carácter de iniciativa ciudadana abierta, no partidaria, auditable y orientada al interés público.

Su eventual evaluación, donación, adopción institucional, prueba piloto, fork o presentación pública no debe implicar:

- apropiación partidaria;
- uso electoral;
- cierre opaco del código;
- eliminación de atribución de origen;
- explotación comercial incompatible;
- uso irrestricto de marca;
- implementación sin respeto de los principios fundacionales;
- transformación en herramienta de vigilancia, sanción o propaganda.

El proyecto fue impulsado originalmente por Andrés Federico Di Fiore, y esa atribución de origen debe preservarse en toda presentación, evaluación institucional, fork, donación, convenio o adopción futura.

---

## 14. Política de marca

La apertura del código y de la documentación no implica autorización automática para utilizar la marca, nombre, logotipos, identidad visual o denominaciones vinculadas con SUBE Prioridad de manera irrestricta.

La identidad pública del proyecto debe utilizarse únicamente de manera compatible con su finalidad original:

- asistencia preventiva;
- privacidad por diseño;
- neutralidad institucional;
- código abierto;
- auditabilidad;
- finalidad social;
- atribución de origen;
- no uso electoral;
- no confusión institucional.

El documento específico sobre esta materia es:

```text
docs/POLITICA_DE_MARCA.md
```

---

## 15. Donación, transferencia o adopción institucional

Antes de cualquier donación, cesión, transferencia, convenio, adopción institucional, autorización de uso de marca o prueba piloto real, deberían analizarse y establecerse condiciones mínimas para preservar la finalidad original del proyecto.

El repositorio incluye un modelo conceptual sobre esta materia:

```text
docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
```

Ese documento no constituye un contrato vigente ni una donación aceptada.

Su finalidad es ordenar posibles condiciones sobre:

- finalidad pública;
- neutralidad no partidaria;
- atribución de origen;
- uso de marca;
- código abierto y transparencia;
- protección de datos personales;
- separación entre acreditación y operación;
- protección del rol del chofer;
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

## 16. Bono Solidario

El Bono Solidario, si se analizara en el futuro, debe considerarse una evolución separada y no indispensable del núcleo inicial del MVP.

No debe interpretarse como:

- multa;
- sanción;
- obligación;
- ranking público;
- mecanismo de presión social;
- sistema de vigilancia;
- parte necesaria de una primera prueba piloto;
- sustitución del régimen legal de asientos prioritarios.

Su eventual análisis requerirá evaluación específica de voluntariedad, privacidad, antifraude, no discriminación, impacto operativo, compatibilidad jurídica y autorización institucional suficiente.

---

## 17. Documentación complementaria

Este resumen debe complementarse con:

- `INTRODUCCION_SUBE_PRIORIDAD.md`;
- `README.md`;
- `docs/MAPA_DE_LECTURA.md`;
- `docs/INDICE_DOCUMENTAL.md`;
- `ARCHITECTURE_GUARDRAILS.md`;
- `docs/ARQUITECTURA_DE_REFERENCIA.md`;
- `docs/ROADMAP_IMPLEMENTACION.md`;
- `docs/DECISIONES_DE_ARQUITECTURA.md`;
- `docs/PRINCIPIOS_DE_GOBERNANZA.md`;
- `docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md`;
- `docs/POLITICA_DE_MARCA.md`;
- `docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md`;
- `docs/FUNDAMENTOS_JURIDICOS.md`;
- `docs/FUNDAMENTOS_MEDICOS.md`;
- `docs/PROTECCION_DATOS_PERSONALES.md`;
- `docs/PROTOCOLO_OPERATIVO.md`;
- `docs/PRUEBA_PILOTO_MODELO.md`;
- `docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md`;
- `docs/PLIEGO_TECNICO_EXTENDIDO.md`.

La documentación principal se encuentra ordenada en:

```text
docs/INDICE_DOCUMENTAL.md
```

Para saber qué leer según el perfil de cada lector:

```text
docs/MAPA_DE_LECTURA.md
```

---

## 18. Lectura recomendada

Para una comprensión inicial:

```text
INTRODUCCION_SUBE_PRIORIDAD.md
```

Para comprender la organización documental:

```text
docs/MAPA_DE_LECTURA.md
```

Para analizar la arquitectura completa:

```text
README.md
```

Para profundizar en documentación específica:

```text
docs/INDICE_DOCUMENTAL.md
```

---

## 19. Declaración final

SUBE Prioridad es una iniciativa ciudadana abierta que propone analizar cómo una arquitectura tecnológica responsable podría contribuir a una accesibilidad más efectiva dentro del transporte público.

El proyecto no plantea una implementación inmediata ni una solución cerrada.

Propone una base documentada para evaluación, discusión y eventual análisis institucional, preservando como principios centrales:

- dignidad de las personas;
- privacidad;
- accesibilidad efectiva;
- minimización de datos;
- gradualidad;
- transparencia;
- auditabilidad;
- responsabilidad pública;
- neutralidad institucional;
- atribución de origen;
- protección de marca;
- no apropiación partidaria;
- no uso electoral;
- no vigilancia;
- no sanción.

La apertura del proyecto no habilita su apropiación partidaria, su uso electoral, el uso irrestricto de su marca, una donación sin condiciones fundacionales, el borramiento de su origen ciudadano ni su transformación en una herramienta de vigilancia, sanción, negocio cerrado o propaganda institucional incompatible con sus principios fundacionales.

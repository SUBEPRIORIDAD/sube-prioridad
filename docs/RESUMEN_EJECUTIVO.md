# Resumen Ejecutivo — SUBE Prioridad

## Documento institucional de presentación, análisis y evaluación del proyecto ciudadano

---

## 1. Síntesis del proyecto

SUBE Prioridad es una iniciativa ciudadana de innovación pública impulsada originalmente por Andrés Federico Di Fiore como propuesta independiente orientada al análisis de accesibilidad efectiva, asistencia preventiva y convivencia dentro del transporte público.

La iniciativa propone estudiar cómo una arquitectura tecnológica responsable podría contribuir a facilitar la experiencia de viaje de personas que cuentan con una necesidad previamente acreditada de viajar sentadas o recibir asistencia preventiva, preservando la privacidad y evitando la exposición innecesaria de información personal sensible.

El proyecto plantea una posible capa complementaria de asistencia, donde una necesidad reconocida pueda representarse mediante un atributo técnico de prioridad, sin trasladar al sistema de transporte información que no resulta necesaria para su funcionamiento operativo.

SUBE Prioridad no propone reemplazar derechos existentes, modificar actualmente el sistema SUBE, crear beneficios tarifarios, establecer sanciones, generar obligaciones nuevas para pasajeros ni trasladar responsabilidades adicionales al personal de conducción.

Su finalidad es aportar una base documentada para evaluación técnica, jurídica, médica, institucional, operativa y social.

---

## 2. Naturaleza actual del proyecto

SUBE Prioridad debe interpretarse actualmente como:

```text
iniciativa ciudadana abierta
↓
MVP conceptual y demostrativo
↓
arquitectura de referencia
↓
documentación técnica e institucional
↓
base para análisis y eventual evaluación institucional
```

La versión actual del repositorio debe leerse como una **versión documental 1.0**: una base pública, abierta y auditable para análisis, discusión, mejora y eventual evaluación institucional.

No constituye una implementación oficial vigente, una integración productiva, una modificación actual del sistema SUBE ni una solución cerrada.

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
Implementación nacional inmediata: no
```

No representa una implementación productiva ni una integración vigente con infraestructura pública.

---

## 3. Problema que busca abordar

En el transporte público existen personas que pueden necesitar viajar sentadas o recibir asistencia preventiva por diferentes motivos.

Esas necesidades pueden estar vinculadas con situaciones permanentes, transitorias, visibles o no visibles.

Algunos ejemplos posibles incluyen:

- discapacidad;
- movilidad reducida;
- embarazo;
- edad avanzada;
- recuperación física;
- condiciones funcionales no visibles;
- situaciones temporales de salud o movilidad;
- otras circunstancias previamente acreditadas por la vía competente.

Aunque existen mecanismos legales y sociales de prioridad, en la práctica pueden presentarse dificultades:

- desconocimiento de otros pasajeros;
- necesidad de explicar públicamente una situación personal;
- incomodidad al solicitar asistencia;
- conflictos derivados de la falta de información;
- situaciones donde una persona necesita ayuda pero evita solicitarla;
- exposición innecesaria de datos personales o condiciones sensibles;
- dificultad para ejercer derechos existentes de manera efectiva y digna;
- ausencia de herramientas preventivas que reduzcan fricción social.

SUBE Prioridad parte de una pregunta central:

> ¿Puede una herramienta tecnológica facilitar el ejercicio efectivo de una prioridad existente sin exponer a la persona usuaria?

---

## 4. Enfoque general de la solución

SUBE Prioridad no parte de la idea de reemplazar la convivencia social por tecnología.

El proyecto propone analizar si la tecnología puede actuar como una herramienta complementaria para reducir fricciones, proteger privacidad y facilitar asistencia preventiva.

El enfoque general puede resumirse así:

```text
derecho o necesidad previamente reconocida
↓
representación técnica mínima
↓
preferencia de asistencia
↓
validación operativa
↓
alerta genérica o asistencia preventiva
↓
experiencia de viaje más segura y respetuosa
```

La finalidad no es crear un sistema de control, vigilancia o sanción.

La finalidad es explorar si una arquitectura tecnológica prudente puede ayudar a que una persona no tenga que explicar públicamente su situación para recibir asistencia.

---

## 5. Separación entre acreditación y operación

Uno de los principios centrales del proyecto es separar dos planos que no deben confundirse:

```text
acreditación
↓
operación
```

### Acreditación

La determinación de una necesidad de prioridad corresponde a los mecanismos, organismos, profesionales o procedimientos que definan las autoridades competentes.

El sistema tecnológico no diagnostica, no evalúa condiciones médicas, no revisa certificados y no decide quién merece prioridad.

La acreditación pertenece al plano institucional, sanitario, administrativo o profesional que corresponda.

### Operación

Una vez acreditada una necesidad por fuera del core operativo, el sistema podría representar esa condición mediante un atributo técnico mínimo, orientado únicamente a facilitar asistencia preventiva.

El core operativo no necesita conocer la causa médica, funcional o personal de la prioridad.

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

## 6. Regla central de privacidad

La regla central del proyecto es:

```text
el transporte no necesita conocer el diagnóstico
```

Y, en términos operativos:

```text
la persona no debe revelar más información de la necesaria
para recibir asistencia preventiva
```

SUBE Prioridad propone que la información sensible no viaje al sistema operativo de transporte.

El sistema conceptual no necesita procesar en el core:

- diagnóstico médico;
- historia clínica;
- certificados médicos en texto abierto;
- DNI;
- nombre;
- domicilio;
- información sanitaria identificable;
- información personal innecesaria.

La propuesta se basa en privacidad por diseño, minimización de datos y separación entre acreditación y operación.

---

## 7. Principios fundamentales

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

### Dignidad

La persona usuaria no debería verse obligada a justificar públicamente su situación personal para recibir asistencia preventiva.

### Autonomía

La persona usuaria debería conservar control sobre la modalidad de asistencia que desea recibir, dentro de los límites que establezca una eventual prueba piloto o implementación autorizada.

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

### Neutralidad institucional

El proyecto debe preservar su carácter ciudadano, abierto, no partidario y orientado al interés público.

---

## 8. Qué es SUBE Prioridad

SUBE Prioridad es:

- una propuesta ciudadana de innovación pública;
- un MVP conceptual y demostrativo;
- una arquitectura de referencia;
- una base para evaluación institucional;
- una propuesta gradual, reversible y auditable;
- un modelo orientado a privacidad y accesibilidad;
- una herramienta conceptual para analizar asistencia preventiva en transporte público;
- una iniciativa abierta impulsada originalmente por Andrés Federico Di Fiore;
- una propuesta que busca facilitar derechos existentes sin sustituirlos;
- una base documental para diálogo técnico, jurídico, médico, institucional y ciudadano.

---

## 9. Qué no es SUBE Prioridad

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
- una implementación nacional inmediata;
- una plataforma de control social;
- una herramienta de exposición pública de personas;
- un mecanismo de ranking o denuncia entre pasajeros.

Tampoco representa una integración actual con organismos públicos, registros estatales, validadoras, hardware embarcado o infraestructura operativa.

El uso de la denominación SUBE Prioridad no implica autorización oficial, adopción vigente ni vinculación institucional actual con el sistema SUBE o sus operadores.

---

## 10. Límites no negociables

SUBE Prioridad no debería evolucionar hacia modelos que impliquen:

- vigilancia de pasajeros;
- sanciones automáticas;
- exposición de diagnósticos;
- rankings públicos;
- presión social indebida;
- uso electoral;
- apropiación partidaria;
- explotación comercial incompatible;
- cierre opaco del código;
- uso irrestricto de marca;
- traslado de responsabilidades indebidas al personal de conducción;
- sustitución de derechos existentes;
- implementación sin evaluación institucional previa.

La finalidad del proyecto es facilitar asistencia preventiva, no crear mecanismos de control social.

Toda evolución futura debería respetar los guardrails fundacionales del proyecto:

```text
privacidad por diseño
minimización de datos
separación entre acreditación y operación
no exposición de diagnósticos
no vigilancia
no sanción
no ranking público
no sobrecarga al chofer
evaluación institucional previa
neutralidad no partidaria
trazabilidad pública
```

---

## 11. Arquitectura institucional propuesta

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

También permite distinguir responsabilidades:

```text
la autoridad competente define criterios
el sistema técnico representa atributos mínimos
la operación facilita asistencia preventiva
la evaluación institucional mide resultados y riesgos
```

---

## 12. Preferencias de asistencia

El proyecto contempla conceptualmente que la persona usuaria pueda tener cierto control sobre la modalidad de asistencia.

Las modalidades posibles, siempre sujetas a evaluación y diseño institucional, podrían ser:

```text
silenciosa
discreta
preventiva
visible
```

Estas preferencias no representan diagnósticos ni categorías médicas.

Sólo indican posibles formas de experiencia operativa.

La persona usuaria no debería ser forzada a exponer públicamente su situación personal para poder viajar en mejores condiciones.

---

## 13. Rol del personal de conducción

SUBE Prioridad considera fundamental preservar el rol del conductor.

El sistema no debe convertir al personal de conducción en:

- evaluador médico;
- fiscalizador documental;
- administrador de datos sensibles;
- árbitro principal de conflictos personales;
- responsable de decidir quién merece asistencia;
- aplicador de sanciones;
- gestor de beneficios;
- operador de información clínica o sanitaria.

La finalidad es reducir fricciones, no trasladar nuevas responsabilidades operativas al personal de conducción.

La conducción segura debe conservar prioridad.

El sistema debería ayudar a disminuir conflictos, no crear nuevas cargas sobre quienes tienen a su cargo la conducción del transporte.

---

## 14. Participación ciudadana y convivencia

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

La tecnología puede ayudar a comunicar una necesidad operativa, pero no debe reemplazar la empatía, la solidaridad ni la responsabilidad social.

---

## 15. Modelo de prueba piloto

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
- con informe final;
- con posibilidad de suspensión, corrección o cierre.

La finalidad de un piloto sería obtener evidencia antes de considerar cualquier evolución.

El objetivo inicial no es implementar nacionalmente el sistema, sino evaluar utilidad, aceptación, riesgos, impacto operativo, privacidad y viabilidad institucional.

Una prueba piloto debería responder, como mínimo, estas preguntas:

```text
¿El sistema facilita asistencia preventiva?
¿Reduce conflictos o incomodidad?
¿Protege adecuadamente la privacidad?
¿Es comprensible para usuarios y pasajeros?
¿Evita sobrecargar al personal de conducción?
¿Genera riesgos de discriminación, exposición o vigilancia?
¿Es técnicamente viable?
¿Es jurídicamente compatible?
¿Debe continuar, ajustarse o cerrarse?
```

---

## 16. Indicadores posibles de evaluación

Una eventual prueba piloto podría medir indicadores agregados, no sensibles y no identificatorios.

Algunos indicadores conceptuales podrían ser:

- cantidad de activaciones demostrativas;
- comprensión del sistema por parte de usuarios;
- comprensión del sistema por parte de pasajeros;
- incidentes reportados;
- reclamos recibidos;
- nivel de aceptación de la modalidad;
- percepción de privacidad;
- percepción de seguridad;
- impacto en la experiencia de viaje;
- impacto operativo sobre el personal de conducción;
- riesgos detectados;
- ajustes recomendados.

La evaluación no debería requerir exposición de diagnósticos ni identificación pública de las personas usuarias.

---

## 17. Valor potencial de la iniciativa

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

## 18. Valor público esperado

El valor público potencial de SUBE Prioridad puede sintetizarse en cinco dimensiones:

### Accesibilidad

Busca facilitar el ejercicio efectivo de prioridades existentes, especialmente cuando la necesidad de asistencia no es visible.

### Privacidad

Evita que la persona deba exponer públicamente diagnósticos, certificados o condiciones personales sensibles.

### Prevención

Propone una asistencia anticipada o preventiva, antes de que se produzca una situación de conflicto, incomodidad o riesgo.

### Convivencia

Busca reducir fricciones entre pasajeros y fortalecer prácticas solidarias sin sanciones ni coerción.

### Gobernanza

Propone una evolución gradual, auditable, reversible y sujeta a evaluación institucional.

---

## 19. Neutralidad institucional y custodia pública

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

La eventual adopción institucional no debería borrar el origen ciudadano del proyecto ni transformar una iniciativa abierta en una herramienta cerrada, partidaria, propagandística o comercialmente apropiada.

---

## 20. Gobernanza multi-actor

Toda evaluación relevante debería contemplar una gobernanza plural.

Esa gobernanza podría incluir, según corresponda:

- autoridades competentes en transporte;
- autoridades competentes en accesibilidad o discapacidad;
- áreas de protección de datos personales;
- universidades;
- organizaciones sociales;
- organizaciones de personas usuarias;
- especialistas en privacidad;
- especialistas en seguridad informática;
- operadores de transporte;
- representantes institucionales plurales;
- equipo fundador o entidad de custodia.

La finalidad de esta gobernanza no es burocratizar el proyecto, sino proteger su finalidad pública, su neutralidad, su transparencia y su continuidad institucional.

Una gobernanza plural puede reducir riesgos de apropiación, improvisación, uso partidario, implementación apresurada o pérdida de confianza pública.

---

## 21. Política de marca

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

La política de marca busca proteger el proyecto frente a usos incompatibles, sin cerrar la colaboración ni impedir el análisis público.

Código abierto no significa uso irrestricto de marca.

---

## 22. Donación, transferencia o adopción institucional

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

La entrega, donación o adopción institucional del proyecto no debería habilitar su apropiación partidaria, su uso electoral, su cierre opaco, su explotación comercial incompatible ni el borramiento de su origen ciudadano.

---

## 23. Código abierto y trazabilidad

SUBE Prioridad se presenta como una iniciativa abierta y auditable.

La apertura del repositorio busca permitir:

- revisión pública;
- mejora colaborativa;
- auditoría técnica;
- discusión institucional;
- participación ciudadana;
- evaluación académica;
- trazabilidad documental;
- control social razonable.

Sin embargo, la apertura no debe confundirse con autorización para cualquier uso.

Toda evolución relevante debería preservar:

```text
atribución de origen
trazabilidad pública
respeto de guardrails
documentación de cambios
neutralidad institucional
protección de datos
finalidad social
```

La transparencia es parte del valor público del proyecto.

---

## 24. Bono Solidario

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

El núcleo inicial de SUBE Prioridad es la asistencia preventiva basada en una necesidad previamente acreditada y representada mediante un atributo técnico mínimo.

---

## 25. Riesgos identificados y mitigaciones documentales

El proyecto reconoce que toda tecnología aplicada a transporte, accesibilidad o asistencia puede generar riesgos si se implementa sin límites claros.

Entre los riesgos identificados se encuentran:

- exposición de personas usuarias;
- tratamiento excesivo de datos personales;
- confusión con una implementación oficial;
- uso partidario o electoral;
- apropiación comercial incompatible;
- sobrecarga del personal de conducción;
- vigilancia o control social;
- falsas expectativas públicas;
- implementación sin prueba suficiente;
- pérdida de atribución de origen;
- uso indebido de marca.

El repositorio intenta mitigar esos riesgos mediante:

- README explicativo;
- arquitectura de referencia;
- guardrails técnicos;
- protección de datos personales;
- fundamentos jurídicos;
- fundamentos médicos;
- protocolo operativo conceptual;
- modelo de prueba piloto;
- principios de gobernanza;
- neutralidad institucional;
- política de marca;
- modelo de condiciones para donación y custodia;
- mapa de lectura;
- índice documental;
- resumen ejecutivo.

La existencia de documentación no reemplaza la evaluación institucional, pero ayuda a ordenar el debate y reducir ambigüedades.

---

## 26. Documentación complementaria

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

## 27. Lectura recomendada

Este documento funciona como puerta de entrada institucional.

Para una lectura ciudadana inicial:

```text
INTRODUCCION_SUBE_PRIORIDAD.md
```

Para una presentación institucional breve:

```text
docs/RESUMEN_EJECUTIVO.md
```

Para elegir recorridos por perfil de lector:

```text
docs/MAPA_DE_LECTURA.md
```

Para comprender la organización documental:

```text
docs/INDICE_DOCUMENTAL.md
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

## 28. Regla de interpretación general

Todo el proyecto debe interpretarse bajo estas reglas:

```text
MVP conceptual
no implementación oficial vigente
no integración real con SUBE
no conexión real con organismos públicos
no procesamiento de datos sensibles reales
no diagnóstico en el core
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

## 29. Declaración final

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
- no sanción;
- no sobrecarga al personal de conducción;
- no sustitución de derechos vigentes;
- evaluación institucional previa.

La apertura del proyecto no habilita su apropiación partidaria, su uso electoral, el uso irrestricto de su marca, una donación sin condiciones fundacionales, el borramiento de su origen ciudadano ni su transformación en una herramienta de vigilancia, sanción, negocio cerrado o propaganda institucional incompatible con sus principios fundacionales.

SUBE Prioridad debe entenderse como una propuesta ciudadana seria, abierta, prudente y documentada para analizar si una herramienta tecnológica, diseñada con privacidad, accesibilidad y responsabilidad institucional, puede contribuir a una experiencia de transporte público más segura, digna y respetuosa.

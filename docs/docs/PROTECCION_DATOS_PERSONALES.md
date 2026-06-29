# Protección de Datos Personales — SUBE Prioridad

## 1. Propósito del documento

Este documento establece lineamientos conceptuales de protección de datos personales para el proyecto **SUBE Prioridad**.

Su finalidad es reforzar que la arquitectura propuesta debe desarrollarse bajo criterios de privacidad por diseño, minimización de datos, finalidad determinada, seguridad, proporcionalidad, transparencia y respeto por la dignidad de las personas usuarias.

El presente documento no constituye una política de privacidad definitiva, una evaluación de impacto formal ni una autorización para el tratamiento de datos personales.

Toda implementación real, prueba piloto o integración con sistemas externos deberá ser evaluada, autorizada y supervisada por las autoridades competentes, conforme a la normativa vigente en materia de protección de datos personales, accesibilidad, transporte público, salud e interoperabilidad administrativa.

---

## 2. Principio rector

SUBE Prioridad debe facilitar asistencia preventiva sin exponer innecesariamente información personal o sensible de las personas usuarias.

La necesidad de viajar sentado o recibir asistencia dentro del transporte público no debe obligar a una persona a revelar públicamente diagnósticos, historia clínica, certificados médicos, circunstancias íntimas o datos de salud identificables.

La arquitectura debe procurar que la asistencia se active mediante un atributo técnico de prioridad previamente habilitado, no mediante la exposición directa de información médica o administrativa.

---

## 3. Estado actual del MVP

El repositorio actual contiene un MVP conceptual, técnico y demostrativo.

En su estado actual, el MVP:

* no procesa usuarios reales;
* no se conecta con organismos públicos;
* no modifica el sistema SUBE;
* no consulta bases estatales reales;
* no valida diagnósticos médicos;
* no almacena historia clínica;
* no procesa certificados médicos en texto plano;
* no representa una implementación productiva;
* no acredita interoperabilidad real vigente.

Toda integración externa prevista en el repositorio debe interpretarse como simulada, salvo indicación expresa, autorización institucional y documentación técnica correspondiente.

---

## 4. Datos que no deben formar parte del core

El núcleo técnico de SUBE Prioridad no debería procesar ni almacenar los siguientes datos:

* DNI;
* nombre;
* apellido;
* domicilio;
* diagnóstico médico;
* historia clínica;
* certificado médico en texto plano;
* datos de salud identificables;
* información clínica;
* información sobre tratamientos;
* documentación médica escaneada;
* datos familiares innecesarios;
* datos biométricos;
* información no necesaria para la finalidad de asistencia preventiva.

La exclusión de estos datos del core es una decisión central de arquitectura.

El sistema debe trabajar, en la mayor medida posible, con atributos técnicos, tokens, hashes o identificadores pseudoanonimizados.

---

## 5. Atributo técnico de prioridad

El modelo correcto de SUBE Prioridad no es:

```text
diagnóstico médico → exposición pública → asistencia
```

El modelo correcto es:

```text
necesidad previamente acreditada
↓
atributo técnico de prioridad
↓
preferencia de asistencia
↓
validación operativa
↓
asistencia preventiva
```

El atributo técnico de prioridad no debe revelar el motivo médico, social o personal por el cual una persona requiere asistencia.

Su función es indicar, en términos operativos, que existe una habilitación previa para activar una modalidad de asistencia dentro del transporte.

---

## 6. Separación entre acreditación y operación

SUBE Prioridad debe separar claramente dos planos.

### Plano institucional

Comprende:

* criterios de acceso;
* requisitos;
* documentación respaldatoria;
* intervención de autoridades competentes;
* validación previa;
* control jurídico;
* eventuales procedimientos administrativos.

### Plano operativo

Comprende:

* atributo técnico;
* token o identificador pseudoanonimizado;
* preferencia de asistencia;
* validación en entorno de transporte;
* señal o registro operativo;
* métricas agregadas.

El sistema técnico no debe transformarse en evaluador médico, sanitario ni administrativo.

La acreditación de la necesidad de asistencia deberá quedar bajo la órbita de los organismos, profesionales o procedimientos que determinen las autoridades competentes.

---

## 7. Finalidad determinada

Cualquier tratamiento de datos personales vinculado con SUBE Prioridad deberá tener una finalidad clara, específica y legítima.

La finalidad principal debe ser:

```text
facilitar asistencia preventiva y accesibilidad efectiva dentro del transporte público
```

No deberían utilizarse datos del sistema para finalidades incompatibles, tales como:

* vigilancia individualizada;
* perfilamiento comercial;
* control migratorio;
* scoring social;
* ranking público de usuarios;
* publicidad personalizada;
* evaluación médica no autorizada;
* sanciones sociales;
* exposición de diagnósticos;
* beneficios o castigos no previstos por autoridad competente.

---

## 8. Minimización de datos

La arquitectura debe aplicar el principio de minimización.

Esto significa que sólo deberían tratarse los datos estrictamente necesarios para cumplir la finalidad de asistencia preventiva.

Antes de incorporar cualquier dato al sistema, debería preguntarse:

```text
¿Este dato es indispensable para facilitar la asistencia?
¿Existe una alternativa menos invasiva?
¿Puede reemplazarse por un atributo técnico?
¿Puede evitarse su almacenamiento?
¿Puede procesarse de forma pseudoanonimizada?
¿Puede limitarse temporalmente?
```

Si la respuesta demuestra que el dato no es necesario, no debería incorporarse.

---

## 9. Pseudoanonimización

El MVP debe priorizar identificadores pseudoanonimizados.

La pseudoanonimización permite reducir riesgos al separar la operación técnica de la identidad directa del usuario.

Entre los mecanismos posibles se encuentran:

* tokens;
* hashes;
* identificadores técnicos;
* atributos binarios o discretos;
* claves temporales;
* referencias no reversibles dentro del core;
* separación entre sistemas de acreditación y sistemas operativos.

La pseudoanonimización no elimina todos los riesgos, pero reduce la exposición directa de datos personales y debe combinarse con medidas organizativas, técnicas y jurídicas.

---

## 10. Preferencias de asistencia

SUBE Prioridad debe reconocer que no todas las personas desean recibir asistencia de la misma manera.

La arquitectura puede contemplar preferencias de asistencia, tales como:

```text
0 = modalidad silenciosa
1 = modalidad discreta
2 = modalidad preventiva
3 = modalidad visible
```

Estas preferencias no deben representar diagnósticos, categorías médicas ni perfiles de salud.

Sólo deben expresar la forma en que el usuario desea interactuar con el sistema, dentro de los límites técnicos y operativos definidos por la autoridad competente.

---

## 11. Modalidad silenciosa y discreta

La privacidad debe permitir que una persona reciba asistencia sin exposición pública innecesaria.

Por ello, la arquitectura debe admitir modalidades silenciosas o discretas cuando resulten técnicamente viables.

Estas modalidades pueden ser útiles para personas que:

* no desean revelar una situación personal;
* atraviesan una condición transitoria;
* tienen una discapacidad no visible;
* están en rehabilitación;
* requieren asistencia sin señalización pública;
* prefieren autonomía y menor exposición.

La asistencia debe estar al servicio de la persona, no al revés.

---

## 12. Prueba piloto y datos personales

Toda prueba piloto deberá diseñarse con criterios reforzados de protección de datos.

Antes de iniciar una prueba piloto deberían definirse:

* qué datos se utilizarán;
* qué datos no se utilizarán;
* quién será responsable de cada tratamiento;
* quién tendrá acceso;
* con qué finalidad;
* por cuánto tiempo;
* cómo se protegerán;
* cómo se informará a los usuarios;
* cómo podrán ejercer sus derechos;
* cómo se auditará el sistema;
* cómo se eliminarán o anonimizarán datos al finalizar la prueba.

La prueba piloto no debe convertirse en una base permanente de datos personales sin evaluación formal.

---

## 13. Consentimiento y voluntariedad en prueba piloto

Cuando una prueba piloto incluya participación de usuarios reales, la participación debería ser voluntaria e informada.

La persona usuaria debería recibir información clara sobre:

* objetivo de la prueba;
* duración;
* alcance territorial;
* datos involucrados;
* datos excluidos;
* posibles riesgos;
* canales de consulta;
* mecanismos de reclamo;
* posibilidad de baja;
* alternativas disponibles;
* autoridad u organismo responsable.

La participación voluntaria no sustituye la necesidad de base jurídica, seguridad y control institucional.

---

## 14. Canales alternativos y brecha digital

La protección de datos también debe contemplar accesibilidad.

No debe exigirse a todos los usuarios el uso exclusivo de herramientas digitales complejas.

Una implementación real debería evaluar canales alternativos para personas que no puedan o no deseen utilizar:

* teléfonos inteligentes;
* aplicaciones móviles;
* conectividad permanente;
* lectura digital compleja;
* interfaces visuales;
* trámites exclusivamente en línea.

La privacidad no debe construirse a costa de excluir a quienes enfrentan barreras digitales.

---

## 15. Interoperabilidad futura

Toda interoperabilidad real con organismos, registros, plataformas públicas o sistemas privados deberá contar con:

* marco jurídico suficiente;
* autorización institucional;
* finalidad específica;
* documentación técnica;
* medidas de seguridad;
* control de acceso;
* trazabilidad;
* evaluación de riesgos;
* auditoría;
* limitación de datos;
* mecanismos de revocación o suspensión.

En el MVP actual, las integraciones son simuladas.

Ningún documento del repositorio debe interpretarse como prueba de conexión real vigente con organismos públicos o privados.

---

## 16. Riesgos a evitar

La arquitectura debe evitar especialmente los siguientes riesgos:

* exposición pública de diagnósticos;
* creación innecesaria de bases de datos médicas;
* tratamiento de datos sensibles sin fundamento;
* identificación directa en el core operativo;
* uso secundario de datos;
* perfilamiento de usuarios vulnerables;
* vigilancia individualizada;
* conservación indefinida de registros;
* acceso indebido por terceros;
* confusión entre simulación e integración real;
* presión social sobre personas usuarias;
* discriminación o estigmatización;
* dependencia de un único proveedor o plataforma.

---

## 17. Seguridad de la información

Una eventual implementación real deberá contemplar medidas de seguridad adecuadas al riesgo.

Entre ellas podrían analizarse:

* control de acceso;
* segregación de roles;
* cifrado cuando corresponda;
* registros de auditoría;
* gestión de claves;
* entornos separados de prueba y producción;
* revisión de código;
* monitoreo de incidentes;
* políticas de conservación;
* eliminación segura;
* pruebas de seguridad;
* respuesta ante incidentes.

El MVP conceptual no reemplaza una evaluación de seguridad productiva.

---

## 18. Registro y trazabilidad

La trazabilidad debe orientarse a auditar el funcionamiento del sistema, no a vigilar individualmente a las personas.

Los registros deberían ser:

* proporcionales;
* limitados;
* seguros;
* auditables;
* orientados a la finalidad declarada;
* conservados sólo por el tiempo necesario;
* preferentemente agregados o pseudoanonimizados.

Todo registro debe poder justificarse por una necesidad técnica, operativa, jurídica o de auditoría.

---

## 19. Conservación y eliminación

Los datos vinculados con una prueba piloto o implementación real no deberían conservarse indefinidamente.

Deberían definirse criterios sobre:

* plazo de conservación;
* finalidad de conservación;
* eliminación segura;
* anonimización cuando corresponda;
* conservación agregada para estadísticas;
* bloqueo o restricción de acceso;
* cierre de pilotos;
* eliminación de datos de usuarios dados de baja.

La conservación debe ser proporcional a la finalidad.

---

## 20. Transparencia hacia el usuario

La información al usuario debe ser clara, accesible y comprensible.

Debe explicarse:

* qué hace el sistema;
* qué no hace;
* qué datos utiliza;
* qué datos no utiliza;
* qué significa el atributo de prioridad;
* qué modalidades de asistencia existen;
* quién administra el sistema;
* cómo se protege la privacidad;
* cómo reclamar;
* cómo solicitar baja;
* cómo corregir errores;
* qué autoridad interviene.

La transparencia fortalece la confianza pública y reduce malentendidos.

---

## 21. Derechos de las personas usuarias

Toda implementación real debería garantizar mecanismos para que las personas puedan ejercer los derechos que les correspondan conforme a la normativa aplicable.

Entre ellos, según corresponda:

* acceso a información sobre el tratamiento;
* rectificación de datos incorrectos;
* actualización;
* supresión o baja cuando proceda;
* oposición o revocación en los casos aplicables;
* reclamo ante canales institucionales;
* información sobre responsables del tratamiento.

Estos mecanismos deben ser accesibles, simples y no discriminatorios.

---

## 22. Datos de salud y especial prudencia

La información vinculada con salud, discapacidad, rehabilitación, movilidad reducida o condiciones personales requiere especial prudencia.

SUBE Prioridad debe evitar que el sistema operativo de transporte procese directamente diagnósticos o documentación clínica.

La eventual acreditación de una condición o necesidad deberá quedar separada del uso operativo del atributo.

El sistema de transporte no debe transformarse en repositorio de información médica.

---

## 23. Rol de universidades, fundaciones e instituciones

La participación de universidades, fundaciones, organizaciones sociales o instituciones de salud en una prueba piloto deberá respetar estrictamente la privacidad de las personas usuarias.

Estas instituciones podrían colaborar en:

* evaluación metodológica;
* accesibilidad;
* experiencia de usuario;
* análisis social;
* diseño de indicadores;
* revisión ética;
* recomendaciones de mejora.

Pero no deberían acceder a datos personales o sensibles salvo que exista fundamento, autorización, finalidad específica, medidas de seguridad y marco institucional suficiente.

Siempre que sea posible, los informes deberían trabajar con datos agregados, anonimizados o pseudoanonimizados.

---

## 24. Bono Solidario y datos personales

El Bono Solidario, al ser una posible evolución futura, requiere especial cautela desde el punto de vista de datos personales.

Su eventual diseño no debería generar:

* rankings públicos;
* exposición de usuarios colaboradores;
* vigilancia entre pasajeros;
* presión social;
* historial público de conductas;
* incentivos basados en datos sensibles;
* mecanismos de sanción;
* tratamiento innecesario de identidad real.

Cualquier análisis futuro del Bono Solidario debería incorporar reglas antifraude, minimización de datos, auditoría, voluntariedad y límites claros respecto del régimen legal de asientos prioritarios.

---

## 25. Evaluación de impacto

Antes de cualquier prueba piloto con usuarios reales, debería analizarse la conveniencia de realizar una evaluación de impacto en privacidad y protección de datos.

Esa evaluación podría considerar:

* finalidad del tratamiento;
* tipos de datos;
* actores intervinientes;
* riesgos;
* medidas de mitigación;
* alternativas menos invasivas;
* base jurídica;
* seguridad;
* conservación;
* derechos de usuarios;
* gobernanza;
* mecanismos de auditoría.

Una evaluación previa permite detectar riesgos antes de que afecten a las personas.

---

## 26. Principio de no discriminación

La protección de datos también debe prevenir usos discriminatorios.

El sistema no debe utilizarse para:

* clasificar públicamente personas;
* exponer condiciones de salud;
* generar estigmas;
* limitar derechos;
* condicionar el acceso al transporte;
* excluir a quienes no usan tecnología;
* crear categorías indebidas de usuarios;
* producir tratos humillantes.

El atributo de prioridad debe estar orientado a facilitar asistencia, no a etiquetar personas.

---

## 27. Relación con el repositorio técnico

El código del MVP debe mantenerse alineado con estos lineamientos.

Toda evolución del código debería evitar introducir campos sensibles en el core.

En particular, no deberían agregarse sin revisión:

* campos de DNI;
* nombre;
* apellido;
* diagnóstico;
* historia clínica;
* certificado médico;
* domicilio;
* datos clínicos;
* identidad real de usuarios colaboradores;
* registros innecesarios.

Los cambios técnicos deberán respetar los guardrails de arquitectura y las decisiones de diseño del proyecto.

---

## 28. Checklist mínimo para una prueba piloto

Antes de una prueba piloto con usuarios reales, debería verificarse como mínimo:

```text
[ ] Se definió la autoridad responsable.
[ ] Se definió la finalidad del tratamiento.
[ ] Se identificaron los datos estrictamente necesarios.
[ ] Se excluyeron diagnósticos e historia clínica del core operativo.
[ ] Se definieron roles y accesos.
[ ] Se informó a los usuarios.
[ ] Se previeron canales de baja o reclamo.
[ ] Se establecieron medidas de seguridad.
[ ] Se definió plazo de conservación.
[ ] Se establecieron criterios de eliminación o anonimización.
[ ] Se evaluaron riesgos.
[ ] Se definieron métricas agregadas.
[ ] Se documentó la interoperabilidad, si existiere.
[ ] Se aclaró que toda integración real requiere autorización.
[ ] Se contemplaron canales alternativos para brecha digital.
[ ] Se verificó que no se alteran derechos vigentes.
```

---

## 29. Declaración final

La protección de datos personales no es un componente accesorio de SUBE Prioridad.

Es una condición estructural de viabilidad.

El proyecto sólo puede sostenerse como propuesta de innovación pública si garantiza que la asistencia preventiva se diseñe sin exponer diagnósticos, sin crear bases médicas innecesarias, sin vigilar a las personas usuarias y sin afectar su dignidad.

SUBE Prioridad debe demostrar que es posible fortalecer la accesibilidad efectiva dentro del transporte público mediante una arquitectura gradual, prudente, respetuosa de la privacidad y sometida a evaluación institucional.

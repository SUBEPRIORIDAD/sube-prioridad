# Protección de Datos Personales — SUBE Prioridad

## 1. Propósito del documento

El presente documento establece lineamientos conceptuales de protección de datos personales para la iniciativa **SUBE Prioridad**.

Su finalidad es explicar cómo debe interpretarse el proyecto desde una lógica de privacidad por diseño, minimización de datos, separación entre acreditación institucional y operación técnica, no exposición de diagnósticos, interoperabilidad responsable y prueba piloto gradual.

Este documento no constituye una política de privacidad productiva, una evaluación de impacto definitiva ni un dictamen jurídico vinculante.

Toda implementación real deberá contar con evaluación técnica, jurídica, institucional y de seguridad de la información por parte de las autoridades competentes.

---

## 2. Principio rector

El principio rector del proyecto es:

```text
asistencia preventiva sin exposición de información sensible
```

SUBE Prioridad no debe convertir al transporte público en una base de datos médica, sanitaria, social o identificatoria.

La necesidad de asistencia debe poder representarse mediante un atributo técnico de prioridad, sin revelar a terceros la causa médica, funcional, personal o administrativa que originó esa habilitación.

---

## 3. Estado actual del MVP

El estado actual del repositorio es conceptual, técnico y demostrativo.

El MVP no representa una implementación productiva.

No se encuentra integrado a organismos públicos.

No modifica el sistema SUBE.

No opera sobre validadoras reales.

No procesa usuarios reales.

No procesa datos médicos reales.

No almacena documentación sanitaria.

Toda interoperabilidad externa debe interpretarse como simulada salvo autorización institucional expresa y documentación técnica verificable.

---

## 4. Datos que no forman parte del core

El core operativo del MVP no debe procesar:

* DNI;
* nombre;
* apellido;
* domicilio;
* teléfono;
* correo electrónico personal;
* diagnóstico médico;
* historia clínica;
* certificado médico en texto plano;
* constancias sanitarias;
* estudios médicos;
* tratamientos;
* medicación;
* condición de discapacidad específica;
* embarazo;
* edad exacta;
* condición oncológica;
* trasplante;
* rehabilitación;
* datos biométricos;
* datos de salud identificables.

La exclusión de estos datos es una condición estructural del diseño.

---

## 5. Atributo técnico de prioridad

El modelo correcto no es:

```text
persona identificada + diagnóstico + exposición en transporte
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
alerta genérica o asistencia preventiva
```

El atributo técnico de prioridad no debe revelar la causa de la asistencia.

Sólo debe indicar que, conforme a reglas definidas por autoridad competente, la persona se encuentra habilitada para solicitar asistencia preventiva.

---

## 6. Separación entre acreditación y operación

SUBE Prioridad debe separar dos planos:

```text
Plano de acreditación:
organismos, profesionales, registros o procedimientos competentes
que validan la necesidad de asistencia

Plano operativo:
sistema técnico que representa un atributo de prioridad
sin conocer el diagnóstico ni la documentación respaldatoria
```

La acreditación puede involucrar criterios médicos, funcionales, sanitarios, administrativos o sociales.

Pero el sistema operativo no debe almacenar ni exponer esos fundamentos.

---

## 7. Finalidad determinada

La finalidad conceptual del sistema es:

```text
facilitar asistencia preventiva y accesibilidad efectiva dentro del transporte público
```

El atributo técnico de prioridad no debe utilizarse para fines incompatibles, tales como:

* vigilancia;
* perfilamiento comercial;
* publicidad;
* scoring social;
* control policial;
* ranking de usuarios;
* sanciones;
* discriminación;
* análisis médico no autorizado;
* decisiones tarifarias automáticas;
* cesión a terceros sin marco jurídico;
* investigación no autorizada con datos personales.

Toda finalidad adicional requeriría evaluación y autorización específica.

---

## 8. Minimización de datos

El sistema debe tratar la menor cantidad posible de datos.

La pregunta rectora debe ser:

```text
¿este dato es estrictamente necesario para activar asistencia preventiva?
```

Si la respuesta es no, el dato no debe ingresar al core operativo.

La minimización debe aplicarse a:

* datos de entrada;
* datos de salida;
* registros técnicos;
* logs;
* métricas;
* reportes;
* evaluaciones;
* interoperabilidad;
* documentación de prueba piloto.

---

## 9. Pseudoanonimización

Cuando se requiera identificar técnicamente una habilitación, debe priorizarse el uso de:

* tokens;
* hashes;
* identificadores pseudoanonimizados;
* atributos técnicos;
* claves temporales;
* credenciales no diagnósticas;
* registros agregados.

La pseudoanonimización no equivale a anonimización absoluta.

Por eso debe combinarse con medidas de seguridad, control de acceso, finalidad específica y conservación limitada.

---

## 10. Preferencias de asistencia

SUBE Prioridad puede contemplar preferencias operativas de asistencia.

Estas preferencias no deben ser interpretadas como diagnósticos ni categorías médicas.

Un esquema conceptual posible es:

```text
0 = silenciosa
1 = discreta
2 = preventiva
3 = visible
```

Estas categorías sólo representan modalidades de experiencia de usuario.

No deben revelar por qué la persona solicita asistencia.

---

## 11. Modalidad silenciosa

La modalidad silenciosa puede permitir una asistencia sin señal pública.

Puede ser útil para preservar la privacidad en situaciones donde la persona usuaria no desea exposición.

Debe evitar registros innecesarios y no debe generar trazabilidad individual excesiva.

---

## 12. Modalidad discreta

La modalidad discreta puede emitir una señal limitada, atenuada o dirigida a un canal específico.

Debe buscar equilibrio entre efectividad y privacidad.

Su diseño debe evitar que terceros puedan inferir una condición médica o personal específica.

---

## 13. Modalidad preventiva

La modalidad preventiva puede emitir una indicación general que facilite colaboración dentro de la unidad.

Debe ser genérica, no diagnóstica y no estigmatizante.

La comunicación debería limitarse a expresar que se solicita asistencia prioritaria, sin informar causa.

---

## 14. Modalidad visible

La modalidad visible requiere especial prudencia.

Toda señal visual o sonora pública puede aumentar la exposición de la persona usuaria.

Antes de utilizarse en una prueba piloto real, debería evaluarse:

* comprensión por parte del público;
* riesgo de estigmatización;
* impacto sobre privacidad;
* intensidad sonora;
* visibilidad;
* duración;
* posibilidad de abuso;
* alternativas menos invasivas;
* consentimiento del usuario;
* canales de baja o modificación de preferencia.

---

## 15. Alertas genéricas

Las alertas deben ser genéricas.

No deben indicar:

* diagnóstico;
* enfermedad;
* discapacidad específica;
* edad;
* embarazo;
* tratamiento;
* rehabilitación;
* condición clínica;
* grupo protegido;
* causa de la prioridad.

Ejemplos conceptuales adecuados:

```text
Asistencia prioritaria solicitada
```

```text
Asiento de prioridad solicitado
```

```text
Se solicita colaboración para asistencia prioritaria
```

La autoridad competente deberá definir el texto final, canal, duración e intensidad de cualquier alerta.

---

## 16. Datos en una prueba piloto

Una prueba piloto real debería trabajar con datos mínimos y, cuando sea posible, agregados.

Podrían relevarse indicadores como:

* cantidad de activaciones;
* horario;
* línea o unidad;
* modalidad utilizada;
* fallas técnicas;
* reclamos;
* incidentes;
* percepción de privacidad;
* comprensión de la alerta;
* aceptación social;
* utilidad percibida.

No deberían relevarse diagnósticos ni datos médicos individualizados.

---

## 17. Consentimiento y voluntariedad

En una etapa piloto, la participación de usuarios prioritarios debería ser voluntaria e informada.

La persona debería conocer:

* objetivo de la prueba;
* duración;
* alcance territorial;
* datos tratados;
* datos excluidos;
* modalidad de asistencia;
* canales de consulta;
* mecanismos de baja;
* riesgos posibles;
* autoridad responsable.

La voluntariedad no debe ser meramente formal.

La persona debe poder darse de baja sin trato discriminatorio.

---

## 18. Brecha digital y canales alternativos

La protección de datos también exige contemplar accesibilidad real.

El sistema no debe excluir a personas por falta de teléfono inteligente, conectividad, alfabetización digital o acceso a trámites digitales.

Una eventual implementación debería prever canales alternativos, presenciales o asistidos, definidos por autoridad competente.

La privacidad no debe depender de la capacidad tecnológica individual.

---

## 19. Interoperabilidad futura

Toda interoperabilidad futura deberá ser especialmente prudente.

No corresponde afirmar que el proyecto ya cuenta con integración real con organismos públicos o privados.

La interoperabilidad sólo podría analizarse si existe:

* competencia institucional;
* base jurídica;
* finalidad determinada;
* autorización;
* minimización de datos;
* seguridad de la información;
* trazabilidad;
* auditoría;
* conservación limitada;
* posibilidad de suspensión;
* documentación técnica;
* evaluación de impacto.

En el estado actual del MVP, toda integración externa debe interpretarse como simulada.

---

## 20. Cruce de bases de datos

El cruce de bases de datos puede generar riesgos significativos.

Por eso no debe presentarse como automático, simple ni habilitado por defecto.

Cualquier eventual verificación contra registros externos debería diseñarse para que el sistema operativo reciba únicamente el resultado necesario, por ejemplo:

```text
atributo habilitado: sí / no
```

sin recibir diagnóstico, historia clínica, certificado o documentación respaldatoria.

---

## 21. Seguridad de la información

Una implementación real debería contemplar medidas de seguridad proporcionales al riesgo.

Entre ellas:

* cifrado en tránsito;
* cifrado en reposo cuando corresponda;
* control de accesos;
* gestión de claves;
* registros de auditoría;
* segregación de entornos;
* revisión de código;
* pruebas de seguridad;
* gestión de incidentes;
* limitación de permisos;
* trazabilidad de accesos;
* monitoreo;
* respaldo y recuperación;
* eliminación segura.

El MVP actual no debe ser interpretado como infraestructura productiva segura.

---

## 22. Logs y trazabilidad

Los logs deben diseñarse con minimización.

No deben registrar diagnósticos ni datos médicos.

No deben registrar información identificatoria innecesaria.

Los logs deben limitarse a lo necesario para:

* depuración técnica;
* seguridad;
* auditoría;
* evaluación agregada;
* detección de fallas;
* prevención de abuso.

La conservación debe ser limitada y justificada.

---

## 23. Conservación y eliminación

Los datos deben conservarse sólo durante el tiempo necesario para la finalidad definida.

En una prueba piloto debería establecerse:

* plazo de conservación;
* procedimiento de eliminación;
* bloqueo o anonimización;
* tratamiento de bajas voluntarias;
* conservación de métricas agregadas;
* eliminación de registros técnicos innecesarios.

La finalización de una prueba piloto no debe justificar acumulación indefinida de datos.

---

## 24. Transparencia

Los usuarios deben recibir información clara y accesible.

La comunicación debería explicar:

* qué es SUBE Prioridad;
* qué no es;
* qué datos usa;
* qué datos no usa;
* para qué se usa el atributo;
* quién es responsable;
* cómo reclamar;
* cómo darse de baja;
* qué derechos conserva el usuario;
* que no se exponen diagnósticos.

La transparencia debe utilizar lenguaje simple.

---

## 25. Derechos de las personas usuarias

Toda implementación real debería respetar los derechos de las personas titulares de datos.

Entre ellos:

* acceso;
* rectificación;
* actualización;
* supresión cuando corresponda;
* oposición;
* información;
* baja voluntaria;
* canales de reclamo;
* trato digno;
* no discriminación.

La asistencia preventiva no debe exigir renunciar a la privacidad.

---

## 26. Datos de salud

Los datos de salud merecen protección reforzada.

SUBE Prioridad debe evitar que el core operativo trate datos de salud identificables.

Cuando exista una necesidad médica o funcional previamente acreditada, esa acreditación debe quedar fuera del sistema operativo de transporte, bajo reglas definidas por autoridad competente.

El transporte no debe convertirse en una extensión de la historia clínica.

---

## 27. Menores de edad

Si una prueba piloto incluyera niños, niñas o adolescentes, deberían aplicarse salvaguardas reforzadas.

Entre ellas:

* interés superior del niño;
* autorización correspondiente;
* protección de identidad;
* no exposición de diagnóstico;
* acompañamiento adulto cuando corresponda;
* comunicación clara;
* limitación de datos;
* intervención de organismos competentes.

El sistema no debe revelar condiciones de salud de menores.

---

## 28. Universidades, fundaciones y organizaciones sociales

La participación de universidades, fundaciones u organizaciones sociales puede ser valiosa para evaluación, accesibilidad y diseño.

Pero su intervención debe respetar límites claros.

No deberían acceder a datos personales o sensibles salvo autorización específica, finalidad determinada y medidas de seguridad adecuadas.

Siempre que sea posible, deberían trabajar con datos agregados, anonimizados o pseudoanonimizados.

---

## 29. Operadores de transporte

Los operadores de transporte pueden participar en una prueba piloto mediante coordinación operativa, soporte técnico, comunicación, relevamiento de incidentes y evaluación.

No deberían recibir diagnósticos ni documentación médica.

Tampoco deberían decidir por sí mismos quién accede a asistencia prioritaria.

Su rol debe estar definido por autoridad competente.

---

## 30. Personal de conducción

El personal de conducción no debe ser convertido en evaluador médico ni fiscalizador de datos personales.

No debe solicitar diagnósticos.

No debe revisar certificados médicos.

No debe decidir si una persona merece prioridad.

No debe administrar datos sensibles.

El diseño debe proteger tanto al usuario como al chofer.

---

## 31. Bono Solidario

El Bono Solidario, como evolución futura, requiere tratamiento separado.

No debe integrarse al núcleo inicial sin evaluación específica.

Desde la perspectiva de protección de datos, debe evitar:

* rankings públicos;
* presión social;
* vigilancia entre pasajeros;
* exposición de usuarios prioritarios;
* identificación de colaboradores;
* incentivos indebidos;
* uso comercial de datos;
* sanciones encubiertas.

Su eventual diseño deberá contar con lineamientos propios de privacidad y antifraude.

---

## 32. Evaluación de impacto

Antes de una prueba piloto real debería evaluarse el impacto en protección de datos personales.

La evaluación debería analizar:

* finalidad;
* necesidad;
* proporcionalidad;
* riesgos;
* datos tratados;
* datos excluidos;
* responsables;
* encargados;
* medidas de seguridad;
* consentimiento o base jurídica;
* derechos de usuarios;
* conservación;
* interoperabilidad;
* incidentes;
* canales de reclamo;
* criterios de suspensión.

---

## 33. No discriminación

La protección de datos también cumple una función antidiscriminatoria.

La exposición de condiciones médicas, funcionales o personales puede generar estigma, trato desigual o conflictos.

Por eso el sistema debe evitar señales que permitan inferir diagnósticos o categorías sensibles.

La asistencia debe basarse en dignidad, no en exposición.

---

## 34. Relación con el código del repositorio

El código del MVP debe respetar estos principios.

Los endpoints, modelos, validadores, simuladores y tests no deberían incorporar campos como:

* DNI;
* nombre;
* apellido;
* diagnóstico;
* historia clínica;
* certificado médico;
* condición médica específica.

Los tests deberían verificar que el sistema declare explícitamente:

```text
datos_sensibles_procesados: false
integracion_real_con_organismos: false
```

---

## 35. Checklist mínimo para prueba piloto

Antes de cualquier prueba piloto real debería verificarse:

```text
[ ] Autoridad responsable definida.
[ ] Finalidad documentada.
[ ] Alcance territorial definido.
[ ] Participación voluntaria.
[ ] Datos excluidos del core.
[ ] Modalidad de asistencia definida.
[ ] Texto de alerta aprobado.
[ ] Evaluación de privacidad realizada.
[ ] Seguridad de la información evaluada.
[ ] Interoperabilidad prevista o descartada.
[ ] Canales de baja y reclamo.
[ ] Plazos de conservación.
[ ] Indicadores agregados.
[ ] Criterios de suspensión.
[ ] Informe final previsto.
```

---

## 36. Relación con otros documentos del repositorio

Este documento debe leerse junto con:

* `README.md`;
* `ARCHITECTURE_GUARDRAILS.md`;
* `docs/INDICE_DOCUMENTAL.md`;
* `docs/FUNDAMENTOS_JURIDICOS.md`;
* `docs/FUNDAMENTOS_MEDICOS.md`;
* `docs/PROTOCOLO_OPERATIVO.md`;
* `docs/PRUEBA_PILOTO_MODELO.md`;
* `docs/PRINCIPIOS_DE_GOBERNANZA.md`;
* `docs/DECISIONES_DE_ARQUITECTURA.md`;
* `docs/ROADMAP_IMPLEMENTACION.md`.

---

## 37. Declaración final

SUBE Prioridad sólo resulta jurídicamente, técnica e institucionalmente defendible si la privacidad forma parte de su diseño desde el inicio.

La asistencia preventiva no debe exigir exposición de diagnósticos, historia clínica ni documentación médica.

El valor del proyecto reside en demostrar que es posible pensar una herramienta de accesibilidad efectiva basada en atributos técnicos, minimización de datos, alertas genéricas, voluntariedad, evaluación institucional y protección reforzada de la dignidad de las personas usuarias.

Toda implementación real deberá ser gradual, reversible, auditable y respetuosa de la normativa aplicable en materia de protección de datos personales.

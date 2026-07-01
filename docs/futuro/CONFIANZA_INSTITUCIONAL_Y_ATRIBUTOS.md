# Confianza Institucional y Atributos Técnicos

## Línea futura no implementada — SUBE Prioridad

---

## 1. Finalidad de este documento

Este documento describe una posible línea futura de análisis para SUBE Prioridad vinculada con la confianza institucional, la emisión de atributos técnicos y la eventual validación criptográfica de información previamente acreditada.

No forma parte del MVP actual.

No representa una implementación vigente.

No acredita integración real con organismos públicos.

No implica validación actual de certificados, CUD, diagnósticos médicos, firmas digitales, trámites administrativos ni documentación sanitaria.

Su finalidad es dejar documentada una posible evolución futura sin incorporarla al código activo del MVP conceptual.

---

## 2. Estado actual del MVP

En la versión documental y técnica actual, SUBE Prioridad debe interpretarse como:

```text
MVP conceptual y demostrativo
sin implementación oficial vigente
sin integración real con SUBE
sin conexión real con organismos públicos
sin validación médica real
sin verificación de CUD
sin firma digital estatal
sin procesamiento de diagnósticos
sin tratamiento de datos sensibles reales
```

El MVP actual sólo debe demostrar una arquitectura mínima basada en:

```text
atributo técnico no sensible
preferencia de asistencia
validación demostrativa
respuesta genérica
privacidad por diseño
separación entre acreditación y operación
```

---

## 3. Regla central

La regla central del proyecto se mantiene:

```text
el transporte no necesita conocer el diagnóstico
```

Esto significa que una eventual implementación futura no debería exponer ante el sistema de transporte:

- diagnóstico médico;
- historia clínica;
- certificado médico en texto plano;
- CUD en texto plano;
- DNI;
- nombre y apellido;
- domicilio;
- datos sanitarios identificables;
- documentación sensible innecesaria.

El sistema operativo de transporte sólo debería recibir, en caso de corresponder y bajo autorización institucional competente, un atributo técnico mínimo, no sensible y previamente acreditado por fuera del core.

---

## 4. Separación entre acreditación y operación

SUBE Prioridad distingue dos planos que no deben confundirse.

### 4.1. Plano de acreditación institucional

Este plano correspondería, en una eventual implementación real, a las autoridades, organismos, profesionales, procedimientos o sistemas legalmente competentes para acreditar una necesidad de asistencia.

Podría involucrar, según la normativa aplicable y la decisión institucional correspondiente:

- organismos públicos competentes;
- registros administrativos autorizados;
- plataformas estatales;
- profesionales habilitados;
- mecanismos de acreditación ya existentes;
- procedimientos administrativos específicos;
- controles jurídicos y de protección de datos personales.

Este plano no forma parte del MVP técnico actual.

---

### 4.2. Plano de operación técnica

Este plano corresponde al funcionamiento mínimo del sistema de asistencia preventiva.

En una arquitectura compatible con los principios de SUBE Prioridad, este plano no debería recibir documentos médicos ni información sensible.

Sólo debería operar con información mínima, por ejemplo:

```text
atributo_prioridad = activo
preferencia_asistencia = discreta / preventiva / visible
estado = demostrativo / vigente / no vigente
```

El transporte no debería conocer por qué existe la prioridad.

Sólo debería conocer, cuando corresponda, que existe una necesidad previamente acreditada de asistencia.

---

## 5. Qué sería una capa futura de confianza institucional

Una capa futura de confianza institucional podría ser un mecanismo destinado a asegurar que un atributo técnico de prioridad fue emitido o habilitado por una fuente autorizada, sin revelar datos sensibles a la operación de transporte.

Esa capa podría cumplir funciones como:

- verificar la autenticidad de un atributo técnico;
- evitar alteraciones del atributo;
- limitar falsificaciones;
- permitir trazabilidad técnica no invasiva;
- separar identidad, acreditación y operación;
- reducir exposición de documentación sensible;
- permitir revocación o vencimiento del atributo;
- habilitar auditorías agregadas y no individualizantes.

Esta capa no debería convertir al sistema de transporte en verificador médico, sanitario o administrativo.

---

## 6. Qué no debe hacer esta capa futura

Una eventual capa de confianza institucional no debería:

- procesar diagnósticos médicos en el core;
- almacenar historia clínica;
- exponer CUD en validadores;
- exigir certificados a bordo;
- mostrar datos sensibles al chofer;
- permitir vigilancia de pasajeros;
- crear rankings de usuarios;
- generar sanciones automáticas;
- decidir quién merece asistencia;
- sustituir a la autoridad competente;
- modificar derechos vigentes;
- convertir la asistencia preventiva en control social.

La función de confianza institucional debería limitarse a validar técnicamente un atributo mínimo, no sensible y previamente autorizado.

---

## 7. Diferencia con el archivo eliminado `gov_crypto_sign.py`

El archivo `gov_crypto_sign.py` fue eliminado del código activo porque podía generar confusión sobre el alcance real del MVP.

Ese archivo sugería conceptos como:

```text
firma digital gubernamental
validación de CUD
firma médica
autoridades certificadoras
verificación estatal
acreditación sanitaria
```

Aunque esos temas pueden ser relevantes para una arquitectura futura, no corresponden al núcleo técnico actual del MVP.

La versión actual del proyecto no debe aparentar:

```text
integración con organismos públicos
validación real de certificados
firma digital estatal vigente
conexión con sistemas sanitarios
verificación médica automatizada
```

Por eso, la idea se traslada a documentación futura y se retira del código ejecutable.

---

## 8. Modelo conceptual futuro

Una eventual implementación futura podría seguir un flujo como el siguiente:

```text
persona usuaria
↓
acreditación ante autoridad competente
↓
emisión de atributo técnico no sensible
↓
almacenamiento o disponibilidad bajo reglas legales
↓
validación técnica del atributo
↓
preferencia de asistencia configurada por la persona
↓
uso operativo mínimo en transporte
↓
alerta genérica, discreta o visible
↓
asistencia preventiva o colaboración voluntaria
```

En este flujo, el transporte no accede al diagnóstico.

El sistema operativo sólo utiliza un atributo técnico mínimo.

---

## 9. Ejemplo conceptual de atributo técnico

Un atributo técnico futuro podría representarse de forma abstracta así:

```json
{
  "atributo": "prioridad_asistencia",
  "estado": "activo",
  "preferencia": "preventiva",
  "vigencia": "limitada",
  "origen": "autoridad_competente",
  "datos_sensibles": false
}
```

Este ejemplo es meramente conceptual.

No representa un formato real.

No representa una integración vigente.

No debe utilizarse para producción.

---

## 10. Condiciones mínimas para analizar esta capa en el futuro

Antes de incorporar cualquier mecanismo real de confianza institucional, deberían existir:

- marco jurídico suficiente;
- autoridad competente claramente identificada;
- finalidad específica;
- evaluación de protección de datos personales;
- análisis de impacto en privacidad;
- revisión técnica independiente;
- criterios de minimización de datos;
- reglas de revocación y vencimiento;
- auditoría no invasiva;
- documentación pública;
- consentimiento o base legal suficiente, según corresponda;
- mecanismos de reclamo;
- gobernanza institucional;
- prueba piloto limitada;
- evaluación previa y posterior.

Sin esas condiciones, esta capa no debería incorporarse al código activo.

---

## 11. Criptografía y firma digital

La criptografía puede ser útil en una etapa futura para proteger la autenticidad e integridad de atributos técnicos.

Sin embargo, cualquier uso real de firma digital, certificados, claves públicas, sellos de tiempo, validación de cadenas de confianza o mecanismos equivalentes debe diseñarse con asesoramiento técnico y jurídico especializado.

El MVP actual no implementa criptografía gubernamental.

El MVP actual no valida firmas digitales reales.

El MVP actual no verifica certificados oficiales.

El MVP actual no consulta registros públicos ni privados.

---

## 12. Riesgos a evitar

Una mala implementación de esta capa podría generar riesgos relevantes:

```text
apariencia de integración oficial inexistente
tratamiento indebido de datos sensibles
exposición de diagnósticos
confusión entre asistencia y fiscalización
sobrecarga del chofer
vigilancia de pasajeros
registro excesivo de eventos individuales
dependencia de proveedores cerrados
uso político o propagandístico
pérdida de confianza pública
```

Por eso, esta línea futura debe mantenerse separada del MVP hasta que exista evaluación institucional competente.

---

## 13. Relación con la prueba piloto

Una primera prueba piloto de SUBE Prioridad no necesita implementar una capa criptográfica gubernamental.

Para una prueba piloto inicial puede ser suficiente trabajar con:

```text
tokens demostrativos
atributos simulados
usuarios voluntarios
preferencias de asistencia
validaciones no productivas
evaluación agregada
documentación clara
```

La confianza institucional plena debería analizarse sólo si el proyecto avanza hacia etapas más formales, con intervención de autoridades competentes.

---

## 14. Relación con protección de datos personales

Toda evolución futura debe respetar los lineamientos del documento:

```text
docs/PROTECCION_DATOS_PERSONALES.md
```

En especial:

- privacidad por diseño;
- minimización de datos;
- finalidad específica;
- proporcionalidad;
- seguridad;
- separación entre acreditación y operación;
- no exposición de diagnósticos;
- no tratamiento innecesario de datos sensibles;
- no vigilancia;
- no trazabilidad individual injustificada.

---

## 15. Relación con gobernanza y custodia pública

Toda capa futura de confianza institucional debe ser compatible con:

```text
docs/PRINCIPIOS_DE_GOBERNANZA.md
docs/NEUTRALIDAD_INSTITUCIONAL_Y_CUSTODIA_PUBLICA.md
docs/POLITICA_DE_MARCA.md
docs/MODELO_CONDICIONES_DONACION_Y_CUSTODIA.md
```

Esto implica que no debería utilizarse para:

- apropiación partidaria;
- uso electoral;
- cierre opaco del código;
- explotación comercial incompatible;
- borramiento de la atribución de origen;
- vigilancia;
- sanción;
- control social indebido.

---

## 16. Criterio de implementación futura

La incorporación de una capa futura de confianza institucional sólo debería considerarse cuando el proyecto haya superado etapas previas, tales como:

```text
MVP conceptual
↓
laboratorio técnico
↓
prueba piloto limitada
↓
evaluación de resultados
↓
revisión jurídica y técnica
↓
definición institucional competente
↓
diseño de interoperabilidad responsable
↓
eventual implementación controlada
```

No debe incorporarse prematuramente al core demostrativo.

---

## 17. Decisión de arquitectura

La decisión actual de arquitectura es:

```text
No incluir verificación gubernamental, firma médica, validación de CUD ni criptografía estatal en el código activo del MVP.
```

La razón es preservar:

- claridad del alcance;
- coherencia documental;
- privacidad;
- minimización;
- neutralidad institucional;
- no confusión con una implementación oficial;
- separación entre acreditación y operación;
- credibilidad técnica del repositorio.

---

## 18. Estado del documento

Este documento tiene carácter:

```text
conceptual
prospectivo
no operativo
no productivo
no vinculante
no implementado
```

Debe leerse como una guía para futuras discusiones técnicas e institucionales.

No habilita por sí mismo ninguna integración, validación real, prueba piloto, tratamiento de datos sensibles ni uso institucional.

---

## 19. Regla de interpretación

En caso de duda, prevalece la regla fundacional:

```text
El MVP no verifica diagnósticos.
El MVP no valida certificados médicos.
El MVP no se conecta con organismos públicos.
El MVP no procesa datos sensibles reales.
El MVP sólo demuestra un atributo técnico mínimo y no sensible.
```

---

## 20. Cierre

La confianza institucional puede ser una dimensión relevante para una eventual implementación futura de SUBE Prioridad.

Sin embargo, en la versión actual del proyecto, esa dimensión debe permanecer fuera del código activo.

El repositorio debe mostrar con claridad que SUBE Prioridad es hoy una iniciativa ciudadana abierta, conceptual, prudente, auditable y orientada al interés público.

La evolución hacia mecanismos de confianza institucional sólo debería analizarse con intervención de autoridades competentes, revisión jurídica, evaluación técnica, protección de datos personales, gobernanza transparente y respeto estricto por la privacidad de las personas usuarias.

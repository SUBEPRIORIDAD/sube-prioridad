# SUBE Prioridad

**SUBE Prioridad** es un proyecto conceptual, técnico y demostrativo orientado a explorar mecanismos de asistencia preventiva, comunicación accesible y reconocimiento solidario dentro del transporte público.

El proyecto trabaja sobre una hipótesis de innovación pública abierta: permitir que una persona con una necesidad de asistencia previamente acreditada pueda configurar preferencias de comunicación y recibir apoyo contextual, sin exponer diagnósticos, certificados, CUD visible, DNI ni datos sensibles dentro del transporte.

El repositorio incluye una arquitectura modular en Python, una API demo con FastAPI, simuladores, reglas antifraude, tests automatizados y documentación técnica.

---

## Estado del proyecto

Este repositorio se encuentra en etapa de **MVP conceptual/demo**.

Actualmente modela:

- Atributo técnico SUBE Prioridad.
- Preferencias de asistencia y alerta.
- Validación demo posterior al pago.
- Alertas pasivas, discretas, visibles o lumínicas.
- Sincronización solidaria.
- Bono Solidario demo.
- Ventanas temporales tipo Red SUBE demo.
- Proximidad móvil no excluyente.
- Alternativas sin celular.
- NFC celular-tarjeta en modo conceptual.
- Validadora asistida como alternativa piloto auditable.
- Acumulación demo para próximo viaje elegible.
- Flujo end-to-end.
- Tests automatizados.
- CI en GitHub Actions.

---

## Importante

Este proyecto **no es una implementación oficial**.

Este proyecto **no integra sistemas reales** de:

- SUBE.
- Red SUBE.
- Nación Servicios.
- Mi Argentina.
- ANDIS.
- SISA.
- RENAPER.
- CNRT.
- Empresas operadoras.
- Validadores reales.
- Molinetes reales.
- Tarjetas reales.
- Cuentas reales.
- Dispositivos oficiales.

El proyecto tampoco:

- Aplica tarifas reales.
- Modifica saldo real.
- Escribe chips reales.
- Acredita beneficios reales.
- Otorga derechos tarifarios vigentes.
- Crea obligaciones legales nuevas.
- Reemplaza normativa vigente.
- Reemplaza asientos prioritarios legales.
- Impone cargas nuevas a choferes o personal operativo.

---

## Principio central

El transporte no necesita conocer el diagnóstico.

SUBE Prioridad trabaja con la idea de un **atributo técnico no sensible**, previamente acreditado por canales externos, que permite activar preferencias de asistencia sin revelar información médica o personal.

El sistema debe preservar:

- Autonomía.
- Privacidad.
- Accesibilidad.
- Gradualidad.
- Interoperabilidad futura.
- No exposición de datos sensibles.
- No obligación de tener celular.
- No carga indebida al personal de transporte.

---

## Qué problema aborda

En el transporte público pueden existir situaciones donde una persona necesita asistencia, asiento, espacio, tiempo o una señal preventiva, pero no quiere o no puede explicar públicamente su situación.

El proyecto propone una capa técnica que permita:

1. Configurar preferencias de asistencia.
2. Activar una alerta posterior a la validación paga.
3. Facilitar la comunicación sin exposición verbal forzada.
4. Permitir asistencia preventiva.
5. Reconocer colaboraciones voluntarias de otros pasajeros.
6. Mantener límites estrictos de privacidad y no discriminación.

---
## 🛡️ Documentación de Gobernanza y Arquitectura Avanzada

Para garantizar el cumplimiento normativo, la resiliencia en el borde y la escalabilidad del sistema, se han incorporado manuales técnicos obligatorios para guiar el desarrollo continuo del ecosistema:

*   [Manifiesto de Defensa de Interoperabilidad (Sandboxing)](./DOC_INTEROPERABILIDAD.md): Establece las directivas operacionales, restricciones físicas y salvaguardas de ciberseguridad inmutables para el aislamiento de la capa de red del Hito 1 y 2.
*   [Hoja de Ruta y Directivas de Homologación (Gap Analysis)](./TECHNICAL_ROADMAP_NACION_SERVICIOS.md): Guía de arquitectura de grado industrial para perfiles Senior/Principal. Detalla los requerimientos de hardware reales (módulos SAM, MIFARE, CAN bus/SAE) necesarios para la transición del prototipo hacia el ecosistema real de Nación Servicios S.A.

---

## Componentes principales

### 1. Atributo SUBE Prioridad

Representa una condición técnica demo de asistencia previamente acreditada.

No contiene diagnóstico, CUD visible, DNI, certificado médico ni historia clínica.

### 2. Preferencias del usuario

La persona puede elegir cómo desea comunicar su necesidad de asistencia:

- Silenciosa.
- Pasiva.
- Discreta.
- Visible.
- Lumínica.
- Asistida.
- Diferida.

### 3. Alerta posterior a validación

Luego de una validación paga demo, el sistema puede activar una señal según preferencias.

Ejemplos conceptuales:

- Registro silencioso.
- Alerta interna pasiva.
- Señal visual discreta.
- Señal lumínica.
- Notificación a estación o personal autorizado, si fue elegida por el usuario.

### 4. Sincronización solidaria

Permite modelar una interacción voluntaria entre una persona con SUBE Prioridad y otra persona usuaria del transporte que colabora.

### 5. Bono Solidario

El Bono Solidario es una funcionalidad demo para reconocer una cesión voluntaria de asiento de uso general.

No se aplica sobre asientos prioritarios legales.

No reemplaza obligaciones existentes.

No permite reclamo unilateral del colaborador.

No genera dinero real ni saldo real.

---

## Bono Solidario MVP

El MVP del Bono Solidario contempla tres opciones principales de sincronización.

### Opción 1 — Celular a celular con contexto Red SUBE demo

Permite una sincronización entre dispositivos móviles usando como respaldo el contexto de validación:

- Misma red demo.
- Misma línea o servicio.
- Misma unidad o contexto.
- Ventana temporal compatible.
- Confirmación del usuario SUBE Prioridad.

Esta opción puede usar QR, código temporal, BLE o sesión móvil demo.

### Opción 2 — Celular NFC del usuario SUBE Prioridad hacia tarjeta SUBE del colaborador

Si el usuario SUBE Prioridad tiene celular con NFC, puede leer/tokenizar en modo demo la tarjeta SUBE física del colaborador.

El MVP no escribe sobre la tarjeta real.

El MVP no modifica el chip.

El MVP genera una instrucción conceptual pendiente para el próximo viaje elegible.

### Opción 3 — Validadora asistida con segunda aproximación de tarjeta

En colectivos, Tren de la Costa u otros medios con validadora a bordo, luego de la validación paga del usuario SUBE Prioridad se puede abrir una ventana corta.

Durante esa ventana, la persona que cedió voluntariamente un asiento de uso general podría acercar su tarjeta a la validadora para registrar el evento demo.

Esta alternativa puede contemplar consola, validadora, terminal u operador, pero siempre como opción piloto auditable.

El chofer no decide el beneficio.

El chofer no verifica datos personales.

El chofer no verifica discapacidad.

El chofer no administra sanciones.

El chofer no debe asumir una obligación nueva.

---

## Regla demo del +50%

El Bono Solidario se modela como un adicional conceptual de **+50%** sobre un descuento base demo tipo Red SUBE.

Ejemplo conceptual:

```text
Descuento base demo tipo Red SUBE: 50%
Bono Solidario demo adicional: 50%
Tope demo configurable: 100%
Resultado demo: hasta 100% para próximo viaje elegible

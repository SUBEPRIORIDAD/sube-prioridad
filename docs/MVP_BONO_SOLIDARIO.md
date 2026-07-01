# MVP Bono Solidario — SUBE Prioridad

## 1. Naturaleza del MVP

El Bono Solidario es una funcionalidad conceptual del proyecto SUBE Prioridad.

Su objetivo es modelar una forma de reconocimiento solidario cuando una persona usuaria común del transporte público cede voluntariamente un asiento de uso general a una persona usuaria con atributo SUBE Prioridad activo.

El MVP no representa una implementación oficial vigente.

El MVP no integra sistemas reales de SUBE, Red SUBE, Nación Servicios, operadores de transporte, validadores, molinetes, tarjetas reales, cuentas reales, aplicaciones oficiales ni bases estatales.

El MVP no aplica descuentos reales, no modifica saldo, no altera tarifas, no escribe chips de tarjetas, no genera beneficios económicos reales y no crea derechos tarifarios actuales.

## 2. Qué busca demostrar

El MVP busca demostrar que puede existir un flujo técnico, gradual y auditable para:

1. Detectar una validación paga de una persona con atributo SUBE Prioridad.
2. Abrir una ventana temporal lógica asociada al viaje.
3. Permitir una sincronización solidaria con otra persona usuaria.
4. Confirmar que la cesión fue voluntaria.
5. Evitar reclamos unilaterales del colaborador.
6. Evitar exposición de datos sensibles.
7. Evitar cargas nuevas para choferes o personal operativo.
8. Generar una instrucción demo para un beneficio de próximo viaje.
9. Aplicar filtros antifraude.
10. Mantener todo en modo conceptual y demostrativo.

## 3. Qué NO es el Bono Solidario

El Bono Solidario no es:

- Un beneficio oficial vigente.
- Una tarifa real.
- Una modificación real de Red SUBE.
- Una acreditación real en tarjeta.
- Una escritura real sobre el chip SUBE.
- Un saldo real.
- Una devolución de dinero.
- Un sistema de donaciones.
- Una billetera.
- Una recompensa económica inmediata.
- Una obligación legal para otros pasajeros.
- Una obligación para choferes.
- Un sistema de vigilancia.
- Un ranking de usuarios.
- Un sistema de sanciones.
- Un mecanismo para reemplazar asientos prioritarios legales.
- Un mecanismo para exponer diagnósticos, CUD, DNI o datos de salud.

## 4. Regla central

El Bono Solidario sólo se modela para casos de cesión voluntaria de asiento de uso general.

No se aplica sobre asientos legalmente prioritarios, porque esos asientos responden a un régimen distinto y obligatorio.

La colaboración reconocida por el MVP es una colaboración voluntaria adicional, no el cumplimiento de una obligación legal previa.

## 5. Principio de privacidad

El sistema no debe revelar:

- DNI.
- Nombre.
- Apellido.
- Domicilio.
- Teléfono.
- Email.
- Diagnóstico médico.
- CUD visible.
- Certificado médico.
- Historia clínica.
- Obra social.
- Patología.
- GPS exacto.
- IMEI.
- MAC.
- Saldo.
- Dinero real.

La lógica del MVP trabaja con tokens demostrativos, atributos técnicos y contexto de validación.

El transporte no necesita conocer el diagnóstico.

## 6. Atributo SUBE Prioridad

El MVP supone la existencia conceptual de un atributo técnico llamado SUBE Prioridad.

Ese atributo indica que existe una necesidad de asistencia previamente acreditada por canales externos o institucionales, sin revelar el motivo médico, diagnóstico, certificado o CUD dentro del transporte.

El atributo debe estar activo al momento de la validación.

El atributo no contiene datos sensibles visibles.

## 7. Ventana temporal

El Bono Solidario no se genera de manera abierta o indefinida.

Debe existir una ventana temporal lógica.

La ventana depende del contexto:

| Contexto | Tipo de ventana demo | Ejemplo conceptual |
|---|---:|---|
| Colectivo con validadora a bordo | Corta | 8 a 10 minutos |
| Tren de la Costa o validadora a bordo | Corta | 8 a 10 minutos |
| Molinete de estación | Extendida | hasta 60 minutos |
| Andén o plataforma | Extendida | hasta 60 minutos |
| Canal asistido o terminal | Extendida/auditable | configurable |
| Confirmación diferida | Mayor auditoría | configurable |

La ventana temporal sirve para facilitar la sincronización y, al mismo tiempo, reducir el riesgo de fraude.

## 8. Tres opciones MVP de sincronización

El MVP contempla tres opciones principales.

### 8.1. Opción 1 — Sincronización celular a celular con contexto Red SUBE demo

Esta opción supone que ambas personas tienen dispositivos móviles disponibles.

El sistema puede usar señales como:

- QR temporal demo.
- Código temporal demo.
- BLE demo.
- Sesión móvil demo.
- Contexto de Red SUBE demo.
- Misma red.
- Misma línea o servicio.
- Misma unidad o viaje.
- Ventana temporal compatible.
- Confirmación del usuario SUBE Prioridad.

Esta opción es una vía reforzada, pero no debe ser la única.

La falta de celular no debe bloquear el Bono Solidario por sí sola.

### 8.2. Opción 2 — Celular NFC del usuario SUBE Prioridad hacia tarjeta SUBE del colaborador

Esta opción permite que la persona usuaria con atributo SUBE Prioridad, si tiene celular con NFC, acerque o reciba la tarjeta SUBE física de la persona que cedió el asiento.

El celular NFC no escribe sobre una tarjeta real en el MVP.

El flujo demo sólo tokeniza la tarjeta del colaborador y genera una instrucción conceptual pendiente para el próximo viaje elegible.

La instrucción demo puede representar que, en una futura implementación oficial, una cuenta, tarjeta, dispositivo asociado, validadora o terminal compatible pueda reconocer ese evento.

Esta opción es útil cuando el colaborador no tiene celular.

### 8.3. Opción 3 — Validadora asistida con segunda aproximación de tarjeta

Esta opción está pensada para colectivos, Tren de la Costa u otros medios con validadora a bordo.

Flujo conceptual:

1. La persona con atributo SUBE Prioridad valida y paga su viaje.
2. La validación abre una ventana temporal corta.
3. Una persona usuaria común cede voluntariamente un asiento de uso general.
4. La persona SUBE Prioridad confirma la cesión.
5. El colaborador puede acercar su tarjeta SUBE a la validadora.
6. El sistema registra un evento demo de Bono Solidario.
7. La instrucción queda pendiente para el próximo viaje elegible.

Esta alternativa puede requerir un modo asistido desde validadora, consola, terminal u operador.

La participación del chofer, si existiera en un piloto, debe ser opcional, mínima, configurable y sustituible.

El chofer no decide el beneficio.

El chofer no verifica diagnósticos.

El chofer no controla datos personales.

El chofer no administra sanciones.

El chofer no debe recibir una carga operativa nueva.

## 9. Buena fe social

El MVP puede registrar una declaración de buena fe social o reconocimiento contextual.

Esa buena fe puede servir como señal de auditoría.

Pero no decide por sí sola la generación del Bono Solidario.

El sistema no debe depender de presión social, exposición pública, ranking, sanciones ni vigilancia entre pasajeros.

## 10. Confirmación del usuario SUBE Prioridad

La confirmación del usuario SUBE Prioridad es central.

El colaborador no puede reclamar unilateralmente el Bono Solidario.

La cesión debe ser reconocida por la persona beneficiaria del asiento o por un canal asistido compatible.

Sin confirmación, el MVP debe rechazar o enviar a revisión el evento.

## 11. Beneficio demo

El beneficio demo se modela como un adicional conceptual del 50%.

Ese adicional se suma al descuento base demo tipo Red SUBE, con tope configurable.

Ejemplo conceptual:

```text
Descuento base demo tipo Red SUBE: 50%
Bono Solidario demo adicional: 50%
Tope demo configurable: 100%
Resultado demo: hasta 100% para próximo viaje elegible

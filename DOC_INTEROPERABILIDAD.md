# Manifiesto de Defensa de la Capa de Interoperabilidad y Resiliencia (Edge)
## Iniciativa Ciudadana "SUBE Prioridad" — Impulsada por Andrés Federico di Fiore

Este documento técnico de gobernanza establece las directivas arquitectónicas, restricciones físicas y salvaguardas de ciberseguridad inmutables para la rama `feature/interoperabilidad`. 

Cualquier extensión de código o microprograma de simulación inyectado en esta rama debe alinearse estrictamente con los principios de resiliencia periférica de la Fase Core (Hito 1 y 2).

---

## 🛡️ 1. Propósito de la Capa de Interoperabilidad
Establecer los estándares, protocolos de comunicación y mecanismos de fallo seguro (*Fail-Safe*) que permiten al Atributo SUBE Prioridad interactuar de manera asíncrona, segura y transparente con el sistema nervioso centralizado del transporte público en Argentina.

### Objetivos Técnicos Críticos:
* **Abstracción Médica Absoluta:** Conexión cifrada hacia endpoints del Estado (Mi Argentina, ANDIS, SISA) mediante tokens JWT, transformando payloads externos en un parámetro binario plano (`Atributo_Prioridad = 1`) sin almacenar datos clínicos ni CUD visibles.
* **Gobernanza del Tiempo de Pasada (Latencia <500ms):** El microprograma de a bordo debe resolver la prioridad de forma local indexando el chip criptográfico mediante Edge Computing.
* **Soporte Offline Estricto:** Tolerancia completa a zonas ciegas mediante almacenamiento Flash efímero en la validadora.

---

## 🚫 2. Restricciones de Aislamiento Mandatarias (Sandbox)
Para garantizar la consistencia técnica y la aprobación limpia del pipeline de GitHub Actions, se imponen las siguientes prohibiciones dentro de esta rama:

1. **Aislamiento Total del Bono Solidario:** Queda terminantemente prohibido activar, modificar o enlazar rutinas comerciales, ventanas de incentivos cooperativos o segundas pasadas de tarjeta dentro de los scripts operativos de esta capa. El Hito 3 permanece aislado de forma lógica (`_ENABLE_FUTURES_HITOS = False`).
2. **Cumplimiento del Habeas Data (Ley N.º 25.326):** Se prohíbe la persistencia, concatenación o escritura de DNI, nombres, apellidos, geolocalizaciones precisas o texto libre de diagnósticos médicos en los archivos de log (`audit_logger.py`) o memorias de caché (`cache_manager.py`). Todo payload secundario debe ser purgado por el filtro activo (`purge_prohibited_fields`).
3. **Invariabilidad del Servicio Comercial:** Ningún fallo del cortocircuito periférico o del firmware de asistencia accesoria puede interrumpir o retrasar el cobro base de la tarifa del boleto SUBE tradicional.

---

## ⚙️ 3. Directivas de Código Liviano en Borde
* Las comunicaciones distribuidas deben procesar formatos JSON estrictos de bajo peso binario.
* Las validadoras urbanas implementarán el algoritmo probabilístico *Exponential Backoff con Jitter* para la mitigación eficiente de colisiones de radio ante transmisiones de ráfaga (*Batch Processing*) asíncronas en terminales saturadas.
* Ante caídas severas de red WAN, el controlador conmutará inmediatamente al estado degradado fuera de línea (*TransportEdgeCircuitBreaker*), salvaguardando la fluidez del molinete del pasajero.

---
*Documento de gobernanza arquitectónica v1.0.0 — Protegiendo el núcleo de accesibilidad digital.*

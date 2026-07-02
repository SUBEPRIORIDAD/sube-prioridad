# Hoja de Ruta de Ingeniería y Directivas de Escalabilidad para Homologación (Fase II)
## Ecosistema "SUBE Prioridad" — Guía de Arquitectura para Ingenieros Senior / Principal
### Documento de Transición Crítica: De Prototipo Analítico a Código de Producción de Borde

Este documento actúa como un plano de arquitectura técnica y directiva inmutable para los ingenieros encargados de evolucionar el MVP actual hacia una solución embebida de grado industrial. El fin es sustituir las capas simuladas por drivers físicos e interoperabilidad federal, resguardando la latencia crítica (<300ms), la Ley N.º 25.326 (Habeas Data) y el blindaje analítico core ya validado.

---

## 🧭 1. Directivas Obligatorias de Codificación y Control de Cambios

Cualquier refactorización o inyección de dependencias en los scripts de Python existentes debe alinearse estrictamente con las siguientes restricciones de diseño:

1. **Invariabilidad de la Pasada de Tarjeta (Bucle Crítico):** Las llamadas de red WAN sincrónicas quedan terminantemente prohibidas en el bucle principal de `validator.py`. El procesamiento criptográfico local debe completarse en microsegundos para garantizar que la latencia total de la validadora física no retrase el flujo de molinete exigido por Nación Servicios S.A.
2. **Blindaje de la Capa de Sanitización:** Todo payload entrante desde pasarelas externas o terminales distribuidas debe ser interceptado obligatoriamente por el filtro activo recursivo `purge_prohibited_fields`. Ningún proceso de ingeniería puede persistir DNI, nombres o texto libre de diagnósticos médicos en archivos log o bases de datos de memoria locales.
3. **Encapsulamiento de Funcionalidades Futuras:** El módulo del Bono Solidario y el motor de acumulación diferida de incentivos para pasajeros colaboradores deben permanecer aislados lógicamente detrás de las banderas de control (`_ENABLE_FUTURES_HITOS = False`) hasta certificar las transacciones base de la tarifa plana.

---

## 🏗️ 2. Arquitectura de Transición: Del Prototipo al Ecosistema Real

El ingeniero senior a cargo deberá reemplazar las simulaciones analíticas actuales por los siguientes componentes distribuidos y estándares de bajo nivel:

### 📡 A. Red Federada de Interoperabilidad (`xroad_gateway.py`)
*   **Estado del MVP:** Simula respuestas asíncronas JSON estáticas para Mi Argentina y bases estatales.
*   **Refactorización Requerida:** Reescribir el módulo implementando el estándar oficial del **Nodo Central de Interoperabilidad Federal X-Road Argentina**. Se debe configurar seguridad basada en **certificados X.509**, autenticación mutua por canal cifrado (mTLS) y el consumo asíncrono y desacoplado de tokens **JWT (JSON Web Tokens)** firmados digitalmente por los organismos emisores (ANDIS, SISA, RENAPER) para constatar la vigencia de la prioridad de accesibilidad sin almacenar variables sensibles.

### 🛡️ B. Criptografía en Borde y Drivers de Tarjeta (`validator.py`)
*   **Estado del MVP:** Evalúa eventos de proximidad analizando strings y clases lógicas en memoria (`EventoValidacion`).
*   **Refactorización Requerida:** Integrar librerías de comunicación embebida de bajo nivel (ej: bindings de C o wrappers nativos sobre subprocesos de hardware) capaces de transmitir comandos **APDU** hacia lectores de tarjetas inalámbricas. El script debe interoperar de forma directa con los **módulos SAM (Secure Application Module)** alojados en las ranuras físicas de las validadoras para intercambiar llaves simétricas cripto-asimétricas y escribir/leer sectores seguros en tarjetas físicas **MIFARE Classic o DESFire EV1** en tiempo de ejecución.

### 🎛️ C. Persistencia Rugerizada Local y Conmutación (`cache_manager.py`)
*   **Estado del MVP:** Administra el cortocircuito (*Circuit Breaker*) y el caché transaccional en listas de memoria de Python.
*   **Refactorización Requerida:** Migrar la persistencia volátil hacia una base de datos local en memoria compartida, compacta y rugerizada contra cortes abruptos de energía (ej: **Redis embebido o SQLite integrado de alta velocidad**). Esto asegurará que las listas de revocación (Blacklists de tarjetas dadas de baja) y los acumuladores de stress temporal sobrevivan a un apagón del motor o falla del alternador del coche de transporte público.

### 🚍 D. Vinculación con Bus Automotriz e Infraestructura (`red_sube_trip_window_matcher.py`)
*   **Estado del MVP:** Valida la ventana horaria de combinación de 2 horas (Red SUBE) basándose en marcas de tiempo genéricas de CPU.
*   **Refactorización Requerida:** Conectar el motor de emparejamiento con la red local del colectivo a través del protocolo automotriz **CAN bus** y el estándar **SAE (Sistema de Ayuda a la Explotación)**. El script de cálculo de secciones no puede depender del servidor, sino que debe capturar las coordenadas geográficas reales del receptor **GPS** de la unidad para auditar la simultaneidad física del cross-checking y cruzar las zonas con los cuadros tarifarios vigentes de la CNRT para liquidar de forma precisa los subsidios financieros del clearing bancario.

### 🧪 E. Inyección de Fallas en Suite de Testing (`test_validator.py` y `test_antifraud.py`)
*   **Estado del MVP:** Valida el éxito de las aserciones unitarias y flujos felices en el pipeline del CI.
*   **Refactorización Requerida:** Expandir la suite de testing automatizada agregando pruebas de stress destructivas. Es mandatorio simular ataques de repetición de señal de radio (*Replay Attacks*), inyección de tramas binarias corruptas en el lector NFC y payloads con desbordamiento de búfer (*Buffer Overflow*) cargados de campos prohibidos (`PROHIBITED_FIELDS`), certificando que el sistema conmute de forma inmediata al estado degradado fuera de línea (*Fail-Safe*) sin colgar el molinete del pasajero.

---
*Manual técnico de transición y escalabilidad de infraestructura v1.0.0 — SUBE Prioridad.*


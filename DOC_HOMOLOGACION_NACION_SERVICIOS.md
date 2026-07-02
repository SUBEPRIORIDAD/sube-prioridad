# Directivas de Homologación Tecnológica y Análisis de Brecha (Gap Analysis)
## Ecosistema "SUBE Prioridad" — Entorno de Transición de Prototipo a Producción Real
### Documentación de Ingeniería Avanzada para Desarrollo Futuro

Este documento técnico establece las directivas arquitectónicas obligatorias que cualquier ingeniero de software debe implementar al modificar la suite core existente (`minimal_information_roles.py`, `validator.py`, `cache_manager.py`). El objetivo es guiar la transición desde el simulador analítico en memoria (Edge) hacia la homologación e integración física con los sistemas distribuidos de Nación Servicios S.A. y la Red SUBE nacional.

---

## 🧭 1. Hoja de Ruta Operacional para la Modificación del Código

Para expandir o alterar las capacidades analíticas validadas del sistema sin introducir regresiones o romper el pipeline automatizado de GitHub Actions, el equipo de ingeniería debe seguir estrictamente estas tres salvaguardas:

1. **Aislamiento Criptográfico Directo:** No se debe alterar la velocidad del bucle principal del firmware local (`LocalEdgeValidator`). Las rutinas de descifrado y procesamiento de llaves SAM deben desacoplarse en hilos asíncronos paralelos para mantener la latencia de pasada por debajo del umbral crítico homologado de `300.0 ms`.
2. **Preservación de la Purga de Privacidad (Habeas Data):** Toda nueva conexión o parsing de tramas externas debe interceptarse obligatoriamente mediante el filtro activo `purge_prohibited_fields`. Queda terminantemente prohibido almacenar o persistir datos de identidad civil (DNI, nombres) o historiales clínicos en memorias caché o logs de auditoría locales.
3. **Mantenimiento de Feature Flags:** Los desarrollos correspondientes a etapas de incentivos o gamificación cívica (Bono Solidario) deben permanecer estrictamente aislados mediante la bandera lógica `_ENABLE_FUTURES_HITOS = False` hasta la completa certificación de la capa física de transporte.

---

## 📊 2. Brechas Críticas y Requerimientos de Producción Real

Para que la suite analítica actual sea integrada en la infraestructura real de la República Argentina, los próximos desarrollos deben sustituir las simulaciones lógicas por los siguientes componentes de hardware y red distribuidos:

### 🛡️ A. Capa Física y Criptografía de Tarjetas (Módulos SAM y MIFARE)
*   **Estado Actual:** Las validaciones de proximidad procesan strings y estructuras planas simuladas (`tarjeta_id`, `ValidationEdgeRequest`).
*   **Requerimiento Real:** El sistema debe interactuar de forma nativa con los chips criptográficos de las tarjetas **MIFARE Classic o DESFire**. Las pasadas deben validarse mediante el intercambio de llaves simétricas seguras alojadas físicamente en los **módulos SAM (Secure Application Module)** integrados en las ranuras internas de las validadoras de colectivos y trenes, firmando digitalmente cada bloque transaccional.

### 🚍 B. Integración con el Bus de Datos Automotriz (Protocolo SAE)
*   **Estado Actual:** Las acciones de mitigación discreta se simulan mediante textos planos (`execute_immediate_edge_habitaculo_alert`).
*   **Requerimiento Real:** El microprograma del validador de a bordo debe integrarse con el **SAE (Sistema de Ayuda a la Explotación)** del colectivo utilizando el bus de comunicación automotriz **CAN bus**. La instrucción de alerta discreta al habitáculo del chofer debe traducirse en tramas binarias compatibles con las consolas homologadas físicas de las unidades comerciales (*Metronec*, *Dipsa*, etc.).

### 📡 C. Sincronización WAN Itinerante y Lotes de Playón (Batch Processing)
*   **Estado Actual:** Los búferes locales acumulan los eventos remanentes de ráfaga en la memoria virtual lineal del servidor en la nube.
*   **Requerimiento Real:** Los algoritmos de mitigación y *Exponential Backoff* deben adaptarse a módems rugerizados con conmutación dinámica inteligente entre redes celulares **4G/5G** (itinerantes en ruta) y antenas de microondas **Wi-Fi de 5.8 GHz** instaladas en los playones físicos de las empresas de transporte, descargando los lotes transaccionales de forma masiva al final del día.

### 🔌 D. Interoperabilidad Federal Federada (X-Road Argentina)
*   **Estado Actual:** La suite asume parámetros de prioridad previamente auditados e inyectados lógicamente de forma local (`priority_attribute_active = True`).
*   **Requerimiento Real:** El backend central de la SUBE debe consumir servicios web distribuidos mediante el **Nodo Central de Interoperabilidad Federal X-Road de la República Argentina**. Se deben establecer túneles TLS mutuos con las APIs oficiales de la **ANDIS** (auditoría en tiempo real de la vigencia del Certificado Único de Discapacidad), el **SISA** (constatación anónima de la condición elegible) y el **RENAPER** (validación de supervivencia civil).

### 🏛️ E. Compensación de Subsidios y Clearing Financiero
*   **Estado Actual:** El procesamiento se enfoca puramente en la asistencia, resguardo y mitigación de anomalías de la tarjeta de prioridad.
*   **Requerimiento Real:** Cada validación exitosa con beneficio debe impactar en el sistema de **Clearing Financiero y Liquidación Bancaria** regulado por el Banco de la Nación Argentina. El software de producción real debe calcular de forma estricta los cuadros tarifarios vigentes, las secciones de viaje por coordenadas GPS y la Red SUBE en la ventana cronológica de 2 horas para liquidar de forma precisa los subsidios estatales a los operadores de transporte.

---
*Documento de Directivas de Arquitectura y Homologación v1.0.0 — Guía de desarrollo continuo.*

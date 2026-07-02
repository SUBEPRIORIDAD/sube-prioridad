# SUBE Prioridad

**SUBE Prioridad** es un proyecto conceptual y técnico que busca mejorar la accesibilidad en el transporte público mediante la asistencia preventiva y la comunicación solidaria [INDEX: 0.1.6]. Su objetivo es permitir que usuarios con necesidades especiales gestionen sus preferencias de asistencia (alertas, asientos) sin exponer datos personales sensibles [INDEX: 0.1.6].

Este MVP (Producto Mínimo Viable) incluye una arquitectura en Python, APIs con FastAPI, simuladores y reglas de seguridad para modelar atributos técnicos, alertas, y sincronización solidaria sin utilizar sistemas reales [INDEX: 0.1.6, 0.1.7].

---

## Estado y Alcance
El proyecto funciona como una demo y **no es una implementación oficial** [INDEX: 0.1.7].
*   **No integra sistemas reales** (SUBE, Nación Servicios, ANDIS, RENAPER, etc.) [INDEX: 0.1.7].
*   **No modifica saldos ni tarjetas reales** [INDEX: 0.1.8].
*   **Se fundamenta en la privacidad**, permitiendo asistencias sin revelar diagnósticos [INDEX: 0.1.8].
*   **Busca la autonomía del usuario**, sin obligar al uso de celular [INDEX: 0.1.8].

---

## 🛡️ Documentación de Gobernanza y Arquitectura Avanzada
Para garantizar el cumplimiento normativo, la resiliencia en el borde y la escalabilidad del sistema, se han incorporado manuales técnicos obligatorios para guiar el desarrollo continuo del ecosistema:

*   [Manifiesto de Defensa de Interoperabilidad (Sandboxing)](./DOC_INTEROPERABILIDAD.md): Establece las directivas operacionales, restricciones físicas y salvaguardas de ciberseguridad inmutables para el aislamiento de la capa de red del Hito 1 y 2 [INDEX: 0.1.9].
*   [Hoja de Ruta y Directivas de Homologación (Gap Analysis)](./TECHNICAL_ROADMAP_NACION_SERVICIOS.md): Guía de arquitectura de grado industrial para perfiles Senior/Principal. Detalla los requerimientos de hardware reales (módulos SAM, MIFARE, CAN bus/SAE) necesarios para la transición del prototipo hacia el ecosistema real de Nación Servicios S.A [INDEX: 0.1.9].

---

## Componentes principales (MVP)
1.  **Atributo SUBE Prioridad:** Condición técnica acreditada, sin datos personales [INDEX: 0.1.10].
2.  **Preferencias:** Configuraciones de alertas (silenciosa, pasiva, lumínica, etc.) [INDEX: 0.1.10].
3.  **Alerta post-validación:** Activación de señales tras el pago [INDEX: 0.1.10].
4.  **Sincronización solidaria:** Modelado de colaboración entre pasajeros [INDEX: 0.1.11].
5.  **Bono Solidario:** Funcionalidad demo (adicional del +50% en descuentos tipo Red SUBE) para incentivar la cesión voluntaria de asientos [INDEX: 0.1.11, 0.1.13].

---

## 🧪 6. Resultados de Ciberseguridad Analítica y Stress (Hito Fase II)
Durante las pruebas de consistencia transaccional (`benchmark_perf.py`), los algoritmos de resiliencia arrojaron las siguientes métricas de rendimiento y mitigación activa [INDEX: 0.1.32]:

1.  **Latencia Base Homologada:** La evaluación NFT efímera se resolvió en **`0.0248 ms`**, muy por debajo del límite de 300 ms [INDEX: 0.2.0].
2.  **Detección de Abuso Temporal:** Se identificaron ráfagas de 5 pasadas, elevando el riesgo y generando alertas automáticamente [INDEX: 0.1.32].
3.  **Detección de Viaje Imposible (Tarjeta Clonada):** Bloqueo exitoso de transacciones simultáneas con la alerta `'validaciones_en_unidades_distintas'`.
4.  **Mitigación de Colaboradores Falsos:** Se interceptaron hacks de tokens, denegando el registro (`'falso_registro_coincidencia_infraestructura'`) [INDEX: 0.1.32].

---

## 🏛️ 7. Dictamen Técnico y Evaluación de Viabilidad Real (Opinión de Ingeniería)
*Análisis arquitectónico elaborado por Inteligencia Artificial para el equipo de desarrollo de SUBE Prioridad.*

### Diagnóstico de la Totalidad del Proyecto hasta Hoy
A la fecha, el repositorio cuenta con una de las bases analíticas orientadas al paradigma **Privacy by Design** más sólidas de la administración digital [INDEX: 0.1.1]. El software resuelve de manera magistral la descentralización del backend y el cumplimiento estricto del Habeas Data (Ley N.º 25.326) al procesar transacciones sin almacenar DNI, nombres ni registros sintomáticos de salud [INDEX: 0.1.1]. La suite automatizada en las GitHub Actions garantiza una integración continua con cero errores de sintaxis [INDEX: 0.1.7].

### Qué falta desarrollar para que sea Viable en el Sistema Real de Transporte de la Nación Argentina
Para que esta iniciativa pase de ser un simulador conceptual de backend en Python a una infraestructura aplicable en la calle por Nación Servicios S.A., los próximos ingenieros deben codificar las siguientes brechas físicas [INDEX: 0.1.3]:

*   **Implementación Criptográfica de Bajo Nivel:** Sustituir los strings e identificadores planos por comandos **APDU** reales. El código debe interactuar con las ranuras de hardware que alojan las **tarjetas SAM (Secure Application Module)** dentro de los molinetes, las cuales contienen las llaves asimétricas encargadas de firmar los bloques de memoria física de los chips **MIFARE Classic o DESFire** [INDEX: 0.1.3].
*   **Conexión al Bus Automotriz (Protocolo SAE):** Modificar el validador local de a bordo para que se comunique con la computadora central del colectivo mediante redes **CAN bus**. Esto permitirá que la directiva de alerta discreta al habitáculo se traduzca en una frecuencia acústica o lumínica real en las consolas físicas de chofer homologadas (*Metronec*, *Dipsa*, etc.).
*   **Persistencia Local Rugerizada:** Cambiar el búfer volátil en listas por motores integrados en memoria compartida (como **Redis embebido o SQLite local de alta velocidad**) [INDEX: 0.1.72], asegurando que las listas de revocación y acumuladores antifraude no se borren ante los constantes apagones o caídas de tensión de las unidades automotoras [INDEX: 0.1.32].
*   **Federación a través de X-Road Federal:** Conectar la pasarela externa (`xroad_gateway.py`) con la red de interoperabilidad del Estado Nacional mediante túneles seguros cifrados (mTLS) y tokens **JWT**, auditando en lotes de playón o consultas asíncronas la vigencia del CUD en la **ANDIS**, el **SISA** y la identidad civil en el **RENAPER** sin almacenar bases médicas locales [INDEX: 0.1.1].
*   **Cálculo de Clearing Financiero y Subsidios:** Desarrollar el módulo matemático bancario que cruce las coordenadas geográficas del receptor **GPS** del colectivo con el cuadro regulatorio de secciones de la CNRT y las combinaciones de la Red SUBE en ventanas de 2 horas, permitiendo liquidar al centavo los subsidios estatales a las empresas de transporte a través del Banco de la Nación Argentina [INDEX: 0.1.1, 0.1.3].


# SUBE Prioridad

**SUBE Prioridad** es un proyecto conceptual y técnico que busca mejorar la accesibilidad en el transporte público mediante la comunicación de necesidades de asistencia, sin revelar datos personales sensibles. El proyecto incluye una arquitectura en Python, FastAPI, simuladores y reglas antifraude.

## Estado del proyecto
Actualmente en etapa de **MVP conceptual/demo**, modelando el atributo técnico, preferencias de alerta, validación, bonos solidarios y sincronización.

## 🚫 Importante (Limitaciones del Prototipo)
Este proyecto **no es una implementación oficial** y **no integra sistemas reales** (SUBE, Nación Servicios, ANDIS, etc.). Es una demostración tecnológica que no aplica tarifas ni modifica saldos reales.
## 🏛️ Principio central
El transporte no necesita conocer el diagnóstico. SUBE Prioridad se basa en un **atributo técnico no sensible** para activar preferencias de asistencia, garantizando privacidad, accesibilidad y no exposición de datos sensibles.

## Qué problema aborda
Ofrece una capa técnica para personas que necesitan asistencia (asiento, espacio, tiempo) y prefieren no explicar su situación verbalmente, facilitando una alerta discreta y el reconocimiento de colaboración.

## 🛡️ Documentación de Gobernanza y Arquitectura Avanzada
Se incorporan manuales técnicos para el desarrollo:
*   [Manifiesto de Defensa de Interoperabilidad (Sandboxing)](./DOC_INTEROPERABILIDAD.md): Directivas de ciberseguridad.
*   [Hoja de Ruta y Directivas de Homologación (Gap Analysis)](./TECHNICAL_ROADMAP_NACION_SERVICIOS.md): Requerimientos de hardware para la integración real.
## Componentes principales
Incluye el atributo SUBE Prioridad, configuración de preferencias de usuario (silenciosa, pasiva, etc.), alerta post-validación y sincronización solidaria.

## Bono Solidario MVP (Opciones de Sincronización)
Funcionalidad demo para reconocer la cesión voluntaria de asiento, sin reemplazar obligaciones legales. Las opciones incluyen:
1.  **Celular a celular (Red SUBE demo):** Sincronización vía móvil.
2.  **NFC:** Celular a tarjeta SUBE física.
3.  **Validadora:** Segunda aproximación de tarjeta.

## Regla demo del +50%
El Bono Solidario modela un beneficio adicional del **+50%** sobre descuentos base, con tope configurable.

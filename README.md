# SUBE Prioridad - Sistema Descentralizado de Gestión de Asientos Prioritarios

Evolución tecnológica conceptual para el ecosistema de transporte público de la República Argentina (Tarjeta SUBE). El sistema optimiza la infraestructura de hardware existente de Nación Servicios S.A. mediante actualizaciones de software y firmware, garantizando resiliencia operativa y protección estricta de datos sensibles.

---

## 🛠️ 1. Arquitectura de Ciberseguridad y Abstracción Médica (Ley Nº 25.326)

El sistema implementa el **Principio de Abstracción Médica** para dar cumplimiento estricto a los Artículos 2, 7 y 11 de la **Ley Nº 25.326 de Protección de Datos Personales** y su **Decreto Reglamentario Nº 1558/2001**:

* **Tokenización de Atributos:** Las pasarelas de interoperabilidad del Estado (ANDIS/Ministerio de Salud) transforman diagnósticos clínicos complejos (CIE-10/11) en un *token de atributo binario* (`0x01` para activo, `0x00` para inactivo). 
* **Aislamiento de Identidad (Disociación):** Las validadoras de colectivos, trenes y subtes jamás procesan el Documento Nacional de Identidad (DNI) ni el historial clínico del usuario. Solo leen la firma criptográfica del token almacenado en el hardware del plástico.
* **Purga de Memoria:** El firmware de la validadora ejecuta la verificación en memoria volátil protegida (SRAM). Al expirar la ventana de transacción, los datos son destruidos de forma irreversible, mitigando ataques de volcado de memoria (*memory dumping*).

---

## 📶 2. Resiliencia Operativa y Funcionamiento 100% Offline (MIFARE Cripto)

Dada la intermitencia de conectividad celular (4G/5G) en tramos interurbanos de Argentina, la lógica de validación de la prioridad no depende de consultas a servidores remotos en tiempo real:


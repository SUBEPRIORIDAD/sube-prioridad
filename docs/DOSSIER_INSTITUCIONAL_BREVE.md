# Dossier Institucional Breve — SUBE Prioridad

## 1. Presentación

SUBE Prioridad es una propuesta ciudadana de innovación pública orientada a fortalecer la accesibilidad efectiva, la asistencia preventiva y la convivencia dentro del transporte público argentino.

La iniciativa propone evaluar una herramienta complementaria que permita facilitar que personas con una necesidad previamente acreditada de viajar sentadas puedan acceder a condiciones de viaje más seguras, respetuosas y adecuadas.

El proyecto no se presenta como una implementación actualmente desplegada ni como una solución tecnológica cerrada.

Se presenta como una arquitectura de referencia, acompañada por un MVP conceptual y documentación técnica, jurídica, operativa y social, puesta a disposición de las autoridades competentes para su análisis.

---

## 2. Problema público identificado

En el transporte público existen personas que, por discapacidad, embarazo, edad avanzada, movilidad reducida, rehabilitación médica u otras circunstancias debidamente acreditadas, pueden necesitar viajar sentadas para preservar su seguridad, salud, bienestar o autonomía.

Muchas de esas necesidades no siempre resultan visibles para el resto de los pasajeros.

En la práctica cotidiana, esta falta de visibilidad puede generar:

* dificultades para acceder a un asiento;
* situaciones incómodas o conflictivas;
* exposición innecesaria de circunstancias personales;
* dependencia de explicaciones verbales;
* barreras de comunicación;
* riesgos durante el viaje;
* pérdida de autonomía.

SUBE Prioridad busca analizar una respuesta preventiva, respetuosa y tecnológicamente prudente frente a este problema.

---

## 3. Objetivo general

El objetivo general de SUBE Prioridad es facilitar la asistencia preventiva dentro del transporte público mediante un mecanismo complementario, gradual y respetuoso de la privacidad.

La finalidad no es reemplazar normas vigentes, sino fortalecer su efectividad práctica.

El sistema apunta a que una necesidad previamente acreditada pueda traducirse, en el plano operativo, en un atributo técnico de prioridad, sin exponer diagnósticos ni datos médicos sensibles.

---

## 4. Qué es SUBE Prioridad

SUBE Prioridad es:

* una propuesta ciudadana de innovación pública;
* una arquitectura conceptual de asistencia preventiva;
* un modelo de validación basado en atributos técnicos;
* un MVP demostrativo en repositorio abierto;
* una iniciativa orientada a prueba piloto;
* una herramienta complementaria del régimen vigente;
* una propuesta gradual, reversible y auditable;
* una arquitectura adaptable a distintas escalas territoriales.

Su núcleo consiste en analizar cómo las capacidades tecnológicas existentes o futuras del ecosistema de transporte podrían colaborar con la accesibilidad efectiva, sin imponer una solución única ni definitiva.

---

## 5. Qué no es SUBE Prioridad

SUBE Prioridad no es:

* una implementación oficial actualmente desplegada;
* un reemplazo del régimen legal de asientos prioritarios;
* un subsidio;
* un beneficio tarifario;
* un sistema de evaluación médica;
* una base de datos de diagnósticos;
* una obligación nueva para los choferes;
* una sanción para pasajeros;
* una herramienta de vigilancia;
* una integración real con organismos públicos en el estado actual del MVP;
* una imposición tecnológica cerrada.

La propuesta debe ser evaluada por las autoridades competentes antes de cualquier implementación real.

---

## 6. Principios rectores

El proyecto se apoya en los siguientes principios:

### Accesibilidad efectiva

La accesibilidad no debe limitarse al reconocimiento formal de derechos, sino procurar condiciones reales de uso seguro, digno y adecuado del transporte público.

### Privacidad por diseño

El sistema no debe exponer diagnósticos, historias clínicas ni información médica identificable.

### Minimización de datos

El núcleo técnico debe utilizar únicamente los datos estrictamente necesarios para validar un atributo de prioridad.

### Gradualidad

La implementación debe comenzar con etapas limitadas, evaluables y reversibles.

### Neutralidad tecnológica

La arquitectura no debe depender de un proveedor, dispositivo, tarjeta, aplicación o hardware específico.

### No sustitución de derechos

La propuesta no modifica ni debilita derechos ya reconocidos por la normativa vigente.

### Control institucional

Toda implementación real debe quedar sujeta a evaluación y decisión de las autoridades competentes.

---

## 7. Modelo conceptual

El modelo de SUBE Prioridad puede expresarse de manera simple:

```text
necesidad previamente acreditada
↓
atributo técnico de prioridad
↓
preferencia de asistencia
↓
validación operativa
↓
experiencia de viaje más segura y respetuosa
```

La acreditación de la necesidad no corresponde al sistema técnico, sino a los organismos, profesionales o procedimientos que determinen las autoridades competentes.

El sistema sólo debería operar sobre un atributo técnico previamente habilitado.

---

## 8. MVP actual

El repositorio público contiene un MVP conceptual y demostrativo.

El MVP permite representar algunos componentes de la arquitectura, tales como:

* validación pseudoanonimizada;
* endpoint de verificación;
* guardrails de privacidad;
* simulador de interoperabilidad;
* motor inicial de reglas antifraude;
* documentación de arquitectura;
* roadmap de implementación;
* principios de gobernanza.

El MVP no procesa usuarios reales.

No se conecta con organismos públicos.

No modifica el sistema SUBE.

No representa una implementación productiva.

---

## 9. Propuesta de prueba piloto

La primera meta institucional razonable es promover una prueba piloto limitada.

Una prueba piloto podría desarrollarse en:

* una línea de colectivo;
* pocas líneas seleccionadas;
* un corredor determinado;
* un municipio;
* una jurisdicción voluntaria;
* un entorno institucional controlado.

La prueba piloto debería ser:

* voluntaria;
* temporal;
* reversible;
* auditada;
* respetuosa de la privacidad;
* sin exposición de diagnósticos;
* sin nuevas cargas al chofer;
* sin modificación de derechos vigentes;
* con métricas claras;
* con canales de reclamo;
* con evaluación previa y posterior.

---

## 10. Beneficios esperados

Entre los beneficios potenciales que podrían evaluarse se encuentran:

* mejora en la accesibilidad efectiva;
* reducción de situaciones incómodas o conflictivas;
* mayor autonomía de personas que necesitan asistencia;
* menor exposición de circunstancias personales;
* fortalecimiento de la convivencia ciudadana;
* aprovechamiento prudente de infraestructura existente;
* generación de evidencia para políticas públicas;
* posibilidad de escalamiento gradual;
* construcción de un modelo adaptable a otras jurisdicciones.

Estos beneficios deben ser medidos y verificados en etapas piloto antes de cualquier expansión.

---

## 11. Protección de datos

La protección de datos personales es un eje central del proyecto.

El core del sistema no debería procesar:

* diagnóstico médico;
* historia clínica;
* certificado médico en texto plano;
* DNI;
* nombre;
* apellido;
* domicilio;
* datos sensibles innecesarios.

Cualquier implementación real deberá contar con base jurídica suficiente, medidas de seguridad, finalidad determinada, auditoría y evaluación institucional previa.

---

## 12. Bono Solidario

El Bono Solidario es una posible evolución futura del ecosistema SUBE Prioridad.

No forma parte del núcleo inicial necesario del proyecto.

Su eventual desarrollo sólo debería evaluarse luego de contar con un sistema base estable, reglas antifraude, evidencia verificable, evaluación social y autorización institucional.

No debe funcionar como multa, sanción, obligación, ranking público ni mecanismo de presión social.

Tampoco debe aplicarse sobre asientos prioritarios legales ni transformar deberes existentes en incentivos.

---

## 13. Solicitud institucional

Se solicita a las autoridades competentes considerar, analizar y evaluar la factibilidad jurídica, técnica, operativa, económica, presupuestaria y social de SUBE Prioridad.

En particular, se propone evaluar:

1. La recepción formal de la iniciativa ciudadana.
2. La revisión técnica e institucional de la arquitectura propuesta.
3. La intervención de organismos competentes.
4. La protección de datos personales.
5. La compatibilidad con el régimen vigente de transporte y accesibilidad.
6. La posibilidad de diseñar una prueba piloto limitada.
7. La definición de métricas de evaluación.
8. La participación de usuarios, especialistas y actores del sistema.

---

## 14. Rol de la ciudadanía

Las firmas ciudadanas que acompañan la propuesta expresan interés social en que SUBE Prioridad sea evaluado por las autoridades competentes.

El apoyo ciudadano no reemplaza la evaluación técnica ni la decisión estatal.

Su función es visibilizar una necesidad concreta y respaldar el pedido de análisis institucional, legislativo y administrativo de la propuesta.

---

## 15. Documentación disponible

El proyecto cuenta con documentación complementaria organizada en el repositorio, incluyendo:

* README general;
* Arquitectura de Referencia;
* Roadmap de Implementación;
* Decisiones de Arquitectura;
* Principios de Gobernanza;
* Estrategia Legislativa y Participación Ciudadana;
* Pliego Técnico Extendido;
* Guardrails de Arquitectura;
* Anexos técnicos y fundamentos operativos.

Esta documentación permite analizar el proyecto desde una perspectiva técnica, jurídica, social, médica, operativa e institucional.

---

## 16. Declaración final

SUBE Prioridad propone una arquitectura pública, gradual y prudente para fortalecer la accesibilidad efectiva dentro del transporte público argentino.

Su valor no reside únicamente en el desarrollo tecnológico, sino en la posibilidad de articular privacidad, asistencia preventiva, convivencia ciudadana, innovación pública y evaluación institucional.

La propuesta no busca imponer una solución cerrada, sino abrir un proceso serio de análisis que permita determinar si una prueba piloto puede contribuir a mejorar la experiencia de viaje de quienes necesitan asistencia sin exponer su dignidad, su intimidad ni sus datos sensibles.

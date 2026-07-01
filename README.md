# SUBE Prioridad

**MVP conceptual y demostrativo para asistencia preventiva, accesibilidad efectiva y convivencia ciudadana en el transporte público.**

SUBE Prioridad es una propuesta ciudadana de innovación pública orientada a analizar herramientas complementarias que puedan facilitar que personas con una necesidad previamente acreditada de viajar sentadas accedan a condiciones de viaje más seguras, respetuosas y adecuadas dentro del transporte público.

Este repositorio contiene un **MVP conceptual, técnico y demostrativo**, acompañado por documentación de arquitectura, fundamentos jurídicos, fundamentos médicos, estrategia legislativa, lineamientos de protección de datos personales, modelo de prueba piloto, protocolo operativo, gobernanza, decisiones de arquitectura y anexos técnicos.

---

## Versión documental 1.0

Este repositorio consolida la versión documental 1.0 de SUBE Prioridad.

La documentación principal se encuentra organizada en:

[`docs/INDICE_DOCUMENTAL.md`](docs/INDICE_DOCUMENTAL.md)

Se recomienda comenzar por ese índice para comprender el alcance del MVP, los límites del proyecto, la arquitectura de referencia, la prueba piloto propuesta, los fundamentos jurídicos y médicos, la estrategia institucional, los principios de gobernanza, las decisiones de arquitectura y el pliego técnico extendido.

La versión 1.0 no representa una implementación oficial vigente ni una integración productiva con SUBE, organismos públicos, validadoras, hardware embarcado o infraestructura estatal.

---

## 1. Estado actual del repositorio

El estado actual del proyecto es:

```text
MVP conceptual: sí
Código demostrativo: sí
API de ejemplo: sí
Tests básicos: sí
Docker: sí
Documentación estratégica: sí
Fundamentos jurídicos: sí
Fundamentos médicos: sí
Protocolo operativo conceptual: sí
Lineamientos de protección de datos: sí
Principios de gobernanza: sí
Decisiones de arquitectura: sí
Implementación productiva: no
Integración real con organismos públicos: no
Modificación del sistema SUBE: no
Procesamiento de datos médicos sensibles: no
```

El repositorio no representa una implementación oficial, productiva ni integrada actualmente con organismos públicos, sistemas SUBE, validadoras, infraestructura estatal o plataformas externas.

Toda eventual implementación real deberá ser evaluada, autorizada y supervisada por las autoridades competentes.

---

## 2. Objetivo del proyecto

El objetivo de SUBE Prioridad es proponer una arquitectura gradual, modular y respetuosa de la privacidad para fortalecer la accesibilidad efectiva dentro del transporte público.

La propuesta busca analizar si una necesidad previamente acreditada puede traducirse, en el plano operativo, en un atributo técnico de prioridad, sin que el usuario deba exponer públicamente diagnósticos, historia clínica o circunstancias personales sensibles.

El foco del proyecto no es reemplazar derechos existentes, sino contribuir a que puedan ejercerse de manera más efectiva, digna y segura.

---

## 3. Qué es SUBE Prioridad

SUBE Prioridad es:

* una propuesta ciudadana de innovación pública;
* una arquitectura conceptual de asistencia preventiva;
* un MVP técnico demostrativo;
* una herramienta pensada para evaluación institucional;
* una posible base para prueba piloto limitada;
* una propuesta gradual, reversible y auditable;
* un modelo orientado a privacidad por diseño;
* una arquitectura adaptable a distintas jurisdicciones.

Su núcleo conceptual puede resumirse así:

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

---

## 4. Núcleo funcional del MVP piloto

La prueba piloto conceptual de SUBE Prioridad busca evaluar si una necesidad previamente acreditada puede representarse mediante un atributo técnico mínimo, no sensible y configurable por la persona usuaria.

El flujo funcional esperado es:

```text
persona con necesidad previamente acreditada
↓
atributo técnico de prioridad
↓
preferencia de asistencia
↓
validación demostrativa
↓
alerta genérica, discreta o visible
↓
colaboración voluntaria o asistencia preventiva
↓
evaluación agregada
```

El sistema no debe revelar diagnósticos, historia clínica, certificados médicos, DNI, nombre, domicilio ni datos sensibles.

La finalidad del MVP no es probar una integración productiva con SUBE, sino demostrar una arquitectura de asistencia preventiva capaz de reducir fricción social, proteger la privacidad y facilitar una experiencia de viaje más segura y respetuosa.

---

## 5. Qué no es SUBE Prioridad

SUBE Prioridad no es:

* una implementación oficial actualmente desplegada;
* un sistema productivo;
* una integración real vigente con organismos públicos;
* una conexión real vigente con ANDIS, SISA, RENAPER, Mi Argentina, Nación Servicios S.A. o CNRT;
* un reemplazo del régimen legal de asientos prioritarios;
* un subsidio;
* un beneficio tarifario;
* un sistema de evaluación médica;
* una base de datos de diagnósticos;
* una herramienta de vigilancia;
* una obligación nueva para choferes;
* un mecanismo de sanción para pasajeros;
* un ranking público de usuarios;
* una solución tecnológica cerrada;
* una implementación nacional inmediata.

La propuesta debe entenderse como una arquitectura abierta, conceptual y evaluable.

---

## 6. Principios rectores

El proyecto se basa en los siguientes principios:

* privacidad por diseño;
* minimización de datos;
* accesibilidad efectiva;
* dignidad de las personas;
* autonomía del usuario;
* neutralidad tecnológica;
* interoperabilidad responsable;
* gradualidad;
* reversibilidad;
* auditabilidad;
* no sustitución de derechos vigentes;
* no imposición de nuevas cargas operativas al personal de conducción.

---

## 7. Privacidad y minimización de datos

El core del MVP no procesa:

* DNI;
* nombre;
* apellido;
* domicilio;
* diagnóstico médico;
* historia clínica;
* certificado médico en texto plano;
* datos de salud identificables;
* identidad real de pasajeros colaboradores.

El modelo técnico trabaja con atributos, tokens o identificadores pseudoanonimizados.

La finalidad es permitir asistencia preventiva sin exponer información sensible de la persona usuaria.

La regla central es:

```text
el transporte no necesita conocer el diagnóstico
```

El repositorio incluye un documento específico sobre esta materia en:

[`docs/PROTECCION_DATOS_PERSONALES.md`](docs/PROTECCION_DATOS_PERSONALES.md)

---

## 8. Fundamentos jurídicos

SUBE Prioridad se apoya en un enfoque jurídico basado en accesibilidad efectiva, igualdad real, dignidad de las personas usuarias, protección de datos personales, razonabilidad, progresividad, no discriminación y evaluación institucional.

El repositorio incluye fundamentos jurídicos conceptuales en:

[`docs/FUNDAMENTOS_JURIDICOS.md`](docs/FUNDAMENTOS_JURIDICOS.md)

Ese documento desarrolla el marco constitucional, convencional, legal, federal e institucional relevante para analizar la iniciativa, incluyendo derechos de personas con discapacidad, personas mayores, personas gestantes, personas con movilidad reducida, protección de datos personales, transporte público, marco SUBE, prueba piloto y antecedentes provinciales de accesibilidad cognitiva.

---

## 9. Fundamentos médicos

SUBE Prioridad también cuenta con fundamentos médicos, sanitarios y funcionales conceptuales.

El proyecto no diagnostica, no evalúa médicamente, no reemplaza certificados oficiales, no sustituye autoridades sanitarias y no convierte al transporte público en un espacio de evaluación clínica.

Su finalidad es reconocer que muchas personas pueden necesitar viajar sentadas o recibir asistencia preventiva por razones permanentes o transitorias, visibles o no visibles, sin verse obligadas a exponer públicamente diagnósticos o documentación médica.

El repositorio incluye estos fundamentos en:

[`docs/FUNDAMENTOS_MEDICOS.md`](docs/FUNDAMENTOS_MEDICOS.md)

---

## 10. Protocolo operativo conceptual

El proyecto incluye un protocolo operativo conceptual destinado a ordenar cómo podría funcionar una eventual experiencia de asistencia preventiva en el transporte público.

Ese protocolo describe roles, flujo operativo, acreditación previa, atributo técnico de prioridad, modalidades de asistencia, alertas genéricas, canales de alerta, comunicación a bordo, rol del chofer, registro de eventos, incidentes, criterios de suspensión, capacitación mínima, canales de reclamo, evaluación operativa e informe final.

No constituye una instrucción operativa vigente ni una implementación productiva.

Debe interpretarse como una guía conceptual adaptable para pruebas piloto, laboratorios técnicos o evaluaciones institucionales.

El documento se encuentra en:

[`docs/PROTOCOLO_OPERATIVO.md`](docs/PROTOCOLO_OPERATIVO.md)

---

## 11. Separación entre acreditación y operación

SUBE Prioridad distingue dos planos:

```text
Plano institucional:
acreditación, requisitos, documentación, autoridad competente

Plano operativo:
atributo técnico, preferencia de asistencia, validación, experiencia de viaje
```

La acreditación de la necesidad de asistencia no corresponde al sistema técnico del MVP.

Esa acreditación debería quedar, en cualquier implementación real, bajo la órbita de los organismos, profesionales o procedimientos que determinen las autoridades competentes.

---

## 12. Rol del usuario

La persona usuaria debe conservar autonomía sobre la forma en que desea recibir asistencia.

El MVP contempla preferencias conceptuales como:

```text
0 = silenciosa
1 = discreta
2 = preventiva
3 = visible
```

Estas preferencias no representan diagnósticos ni categorías médicas.

Sólo indican modalidades de experiencia de usuario.

---

## 13. Rol del chofer

El personal de conducción no debe ser convertido en:

* evaluador médico;
* fiscalizador documental;
* administrador de datos sensibles;
* árbitro principal de conflictos entre pasajeros;
* aplicador de sanciones;
* responsable de decidir quién merece asistencia.

La conducción segura debe conservar prioridad operativa.

El sistema debe reducir conflictos, no trasladarlos al chofer.

---

## 14. Colaboración voluntaria

SUBE Prioridad no obliga a otros pasajeros a actuar.

La asistencia o cesión de asiento debe mantenerse como conducta voluntaria, solidaria y no sancionatoria.

El sistema no debe generar multas, castigos, rankings públicos ni presión social indebida.

---

## 15. Estado del MVP técnico

El MVP actual permite representar algunos componentes de la arquitectura, entre ellos:

* API demostrativa;
* validación pseudoanonimizada;
* endpoint de verificación;
* endpoint de salud;
* endpoint de guardrails;
* simulación de interoperabilidad;
* motor inicial de reglas antifraude;
* guardrails de arquitectura;
* tests básicos;
* ejecución local;
* ejecución con Docker.

Este MVP no procesa usuarios reales ni se conecta con sistemas productivos.

---

## 16. Endpoints disponibles

La API demostrativa incluye:

```text
GET  /
GET  /health
GET  /project/guardrails
POST /api/v1/prioridad/verificar
```

Estos endpoints existen para fines conceptuales, técnicos y de prueba.

No implican conexión real con organismos, sistemas SUBE, validadoras, registros externos o infraestructura estatal.

---

## 17. Interoperabilidad

La arquitectura contempla la posibilidad de interoperabilidad futura con organismos, registros o plataformas externas cuando exista:

* marco jurídico suficiente;
* autorización institucional;
* documentación técnica;
* seguridad informática;
* trazabilidad;
* protección de datos personales;
* finalidad específica.

En el estado actual del repositorio, toda integración externa debe interpretarse como simulada.

Ningún archivo del repositorio acredita conexión real vigente con organismos públicos o privados.

---

## 18. Bono Solidario

El Bono Solidario se considera una posible evolución futura del ecosistema SUBE Prioridad.

No forma parte del núcleo inicial necesario del proyecto.

No debe entenderse como:

* multa;
* sanción;
* obligación;
* ranking público;
* mecanismo de presión social;
* sistema de vigilancia;
* beneficio por liberar asientos prioritarios legales;
* parte indispensable de una primera prueba piloto.

Su eventual análisis debería realizarse sólo después de contar con un sistema base estable, evaluado y autorizado.

---

## 19. Prueba piloto

La primera meta institucional razonable del proyecto es la evaluación de una prueba piloto limitada.

Una prueba piloto debería ser:

* voluntaria;
* temporal;
* reversible;
* auditable;
* respetuosa de la privacidad;
* sin exposición de diagnósticos;
* sin modificación de derechos vigentes;
* sin nuevas cargas operativas al chofer;
* con indicadores previamente definidos;
* con evaluación antes, durante y después.

El repositorio incluye un modelo conceptual de prueba piloto en:

[`docs/PRUEBA_PILOTO_MODELO.md`](docs/PRUEBA_PILOTO_MODELO.md)

---

## 20. Arquitectura de referencia

SUBE Prioridad no debe leerse únicamente como una aplicación ni como una API.

Debe entenderse como un MVP de una arquitectura de referencia para una posible política pública gradual.

La arquitectura fue pensada para poder evolucionar desde:

```text
MVP conceptual
↓
laboratorio técnico
↓
prueba piloto limitada
↓
piloto ampliado
↓
implementación regional
↓
eventual implementación nacional
↓
modelo adaptable a otras jurisdicciones
```

Siempre bajo evaluación técnica, jurídica, presupuestaria, operativa, social e institucional.

El documento de arquitectura de referencia se encuentra en:

[`docs/ARQUITECTURA_DE_REFERENCIA.md`](docs/ARQUITECTURA_DE_REFERENCIA.md)

---

## 21. Documentación estratégica del proyecto

La documentación principal del repositorio se organiza en los siguientes documentos:

* [`docs/INDICE_DOCUMENTAL.md`](docs/INDICE_DOCUMENTAL.md): guía de lectura y organización general de la documentación.
* [`docs/DOSSIER_INSTITUCIONAL_BREVE.md`](docs/DOSSIER_INSTITUCIONAL_BREVE.md): síntesis institucional para autoridades, legisladores, asesores y ciudadanía.
* [`docs/PETITORIO_MODELO.md`](docs/PETITORIO_MODELO.md): modelo orientativo de petitorio ciudadano para acompañar firmas y presentaciones.
* [`docs/MODELO_PROYECTO_RESOLUCION.md`](docs/MODELO_PROYECTO_RESOLUCION.md): modelo orientativo para impulsar formalmente la evaluación institucional.
* [`docs/PRUEBA_PILOTO_MODELO.md`](docs/PRUEBA_PILOTO_MODELO.md): modelo conceptual de prueba piloto limitada, voluntaria, reversible y auditable.
* [`docs/PROTOCOLO_OPERATIVO.md`](docs/PROTOCOLO_OPERATIVO.md): protocolo operativo conceptual para ordenar una eventual experiencia de asistencia preventiva.
* [`docs/PROTECCION_DATOS_PERSONALES.md`](docs/PROTECCION_DATOS_PERSONALES.md): lineamientos de privacidad, minimización de datos, separación entre acreditación y operación, prueba piloto e interoperabilidad responsable.
* [`docs/FUNDAMENTOS_JURIDICOS.md`](docs/FUNDAMENTOS_JURIDICOS.md): fundamentos jurídicos, constitucionales, convencionales, federales e institucionales del proyecto.
* [`docs/FUNDAMENTOS_MEDICOS.md`](docs/FUNDAMENTOS_MEDICOS.md): fundamentos médicos, sanitarios y funcionales conceptuales del proyecto.
* [`docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md`](docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md): estrategia para impulsar el análisis legislativo, administrativo y ciudadano.
* [`docs/ARQUITECTURA_DE_REFERENCIA.md`](docs/ARQUITECTURA_DE_REFERENCIA.md): visión arquitectónica general del proyecto.
* [`docs/ROADMAP_IMPLEMENTACION.md`](docs/ROADMAP_IMPLEMENTACION.md): hoja de ruta conceptual para una evolución gradual.
* [`docs/DECISIONES_DE_ARQUITECTURA.md`](docs/DECISIONES_DE_ARQUITECTURA.md): decisiones técnicas y conceptuales que orientan el diseño.
* [`docs/PRINCIPIOS_DE_GOBERNANZA.md`](docs/PRINCIPIOS_DE_GOBERNANZA.md): criterios de transparencia, protección de datos, auditabilidad y control institucional.
* [`ARCHITECTURE_GUARDRAILS.md`](ARCHITECTURE_GUARDRAILS.md): límites técnicos que toda evolución del código debe respetar.
* [`docs/PLIEGO_TECNICO_EXTENDIDO.md`](docs/PLIEGO_TECNICO_EXTENDIDO.md): documento técnico amplio que conserva la visión integral original del proyecto.

Estos documentos deben leerse de manera complementaria.

Se recomienda comenzar por:

[`docs/INDICE_DOCUMENTAL.md`](docs/INDICE_DOCUMENTAL.md)

---

## 22. Pliego técnico extendido

El repositorio conserva un pliego técnico extendido con la visión integral original del Programa SUBE Prioridad.

Ese documento debe interpretarse como documentación conceptual, prospectiva y evolutiva.

No representa una implementación productiva ni una integración real vigente con SUBE, organismos públicos, validadoras, hardware embarcado ni infraestructura estatal.

Ver:

[`docs/PLIEGO_TECNICO_EXTENDIDO.md`](docs/PLIEGO_TECNICO_EXTENDIDO.md)

---

## 23. Ejecución local

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la API:

```bash
uvicorn main:app --reload
```

Abrir documentación interactiva:

```text
http://127.0.0.1:8000/docs
```

---

## 24. Tests

Ejecutar tests:

```bash
pytest -q
```

Verificar compilación básica:

```bash
python -m py_compile main.py validator.py cache_manager.py circuit_breaker.py xroad_gateway.py
```

---

## 25. Docker

Construir y ejecutar con Docker Compose:

```bash
docker compose up --build
```

---

## 26. Estructura técnica orientativa

El repositorio incluye, entre otros archivos:

```text
main.py
validator.py
cache_manager.py
circuit_breaker.py
xroad_gateway.py
test_main.py
test_antifraud.py
requirements.txt
Dockerfile
docker-compose.yml
ARCHITECTURE_GUARDRAILS.md
docs/
```

La estructura podrá evolucionar conforme avance el proyecto, manteniendo coherencia con los guardrails y la documentación estratégica.

---

## 27. Regla de interpretación general

Todo el repositorio debe interpretarse bajo estas reglas:

```text
MVP conceptual
no implementación oficial vigente
no integración real con SUBE
no conexión real con organismos públicos
no procesamiento de datos sensibles
no diagnóstico médico en el core
no modificación actual de validadoras reales
no alteración del cobro del transporte
no sanciones automáticas
no nuevas cargas indebidas al chofer
no sustitución de derechos vigentes
```

---

## 28. Autoría e iniciativa

SUBE Prioridad es una iniciativa ciudadana de innovación pública impulsada por Andrés Federico Di Fiore.

El repositorio se pone a disposición como base abierta para análisis, discusión, mejora, evaluación institucional y eventual prueba piloto por parte de autoridades competentes, universidades, organizaciones sociales, operadores y ciudadanía.

---

## 29. Licencia

Este proyecto se publica bajo licencia MIT, salvo indicación expresa en contrario para documentos, marcas, logos, archivos institucionales o materiales de terceros.

La publicación abierta del repositorio no implica autorización de implementación productiva ni uso institucional por parte de organismos públicos o privados.

---

## 30. Declaración final

SUBE Prioridad es una propuesta ciudadana de innovación pública orientada a fortalecer la accesibilidad efectiva, la asistencia preventiva y la convivencia dentro del transporte público.

El repositorio no pretende demostrar una solución cerrada ni una implementación definitiva.

Su finalidad es ofrecer una arquitectura conceptual, documentada y técnicamente demostrable para que pueda ser analizada, discutida, mejorada y eventualmente evaluada por las autoridades competentes.

El valor del proyecto reside en articular tecnología, privacidad, accesibilidad, dignidad, fundamentos jurídicos, fundamentos médicos, protocolo operativo, participación ciudadana, gobernanza, gradualidad institucional y código abierto en una propuesta seria, prudente y escalable.

La versión documental 1.0 consolida el repositorio como una base pública, abierta y auditable para explorar si una necesidad previamente acreditada puede representarse mediante un atributo técnico de prioridad, mínimo y no sensible, que facilite asistencia preventiva sin exponer diagnósticos, sin alterar el sistema de cobro, sin sustituir derechos existentes y sin trasladar cargas indebidas al personal de conducción.

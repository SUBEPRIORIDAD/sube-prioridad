# SUBE Prioridad

**MVP conceptual y demostrativo para asistencia preventiva, accesibilidad y convivencia ciudadana en el transporte público.**

SUBE Prioridad es una propuesta de innovación pública orientada a facilitar que personas con necesidad acreditada de viajar sentadas puedan acceder de manera más rápida, segura y respetuosa a un asiento dentro del sistema de transporte público.

El presente repositorio contiene una implementación técnica inicial de carácter **conceptual, modular y demostrativo**.

No constituye una implementación definitiva, obligatoria ni integrada en producción con organismos públicos o sistemas reales de transporte.

---

## 1. Estado actual del repositorio

Estado técnico actual:

```text
MVP conceptual ejecutable
API FastAPI básica
Validación pseudoanonimizada por hash
Tests automatizados
CI con GitHub Actions
Dockerfile y docker-compose
Módulos simulados de interoperabilidad
Motor antifraude inicial para escenarios futuros
```

El repositorio busca demostrar una posible arquitectura de base, no imponer una solución técnica única.

---

## 2. Objetivo del proyecto

El objetivo principal de SUBE Prioridad es explorar herramientas que permitan:

* facilitar el acceso a un asiento a personas con necesidad acreditada de viajar sentadas;
* reducir situaciones de exposición innecesaria;
* fortalecer la asistencia preventiva;
* preservar la dignidad, privacidad y autonomía del usuario;
* aprovechar infraestructura tecnológica existente;
* promover una cultura de colaboración ciudadana dentro del transporte público.

La tecnología no es el fin del proyecto. Es una herramienta al servicio de la accesibilidad efectiva, la seguridad y la convivencia.

---

## 3. Qué es SUBE Prioridad

SUBE Prioridad propone estudiar la incorporación de un **atributo técnico de prioridad** dentro del ecosistema de transporte, asociado a usuarios previamente habilitados mediante los mecanismos que determinen las autoridades competentes.

Ese atributo podría permitir que el sistema reconozca, de forma respetuosa y no invasiva, que una persona requiere asistencia para viajar sentada.

Modelo conceptual:

```text
usuario habilitado -> atributo técnico de prioridad -> preferencia de asistencia
```

Ejemplo de respuesta técnica:

```json
{
  "atributo_prioridad_activo": true,
  "perfil_alertas_ux": 2,
  "fecha_caducidad": "2026-12-31T00:00:00Z",
  "entorno": "simulado_mvp",
  "datos_sensibles_procesados": false,
  "integracion_real_con_organismos": false
}
```

---

## 4. Qué no es SUBE Prioridad

SUBE Prioridad no pretende:

* sustituir derechos ya reconocidos;
* modificar el régimen legal de asientos prioritarios;
* crear privilegios arbitrarios;
* imponer obligaciones adicionales al chofer;
* generar sanciones automáticas a pasajeros;
* alterar la recaudación del sistema SUBE;
* exponer diagnósticos médicos;
* procesar historia clínica;
* reemplazar la solidaridad humana;
* imponer una tecnología específica;
* afirmar integraciones reales que aún no existen.

El proyecto debe entenderse como una propuesta complementaria, progresiva y sujeta a evaluación técnica, jurídica, operativa y presupuestaria.

---

## 5. Privacidad y minimización de datos

El core del MVP no debe procesar ni almacenar:

* DNI;
* nombre y apellido;
* domicilio;
* historia clínica;
* diagnóstico médico específico;
* certificados médicos en texto plano;
* identidad real de pasajeros colaboradores;
* información sensible innecesaria.

El sistema trabaja conceptualmente con:

* hashes;
* tokens pseudoanonimizados;
* atributos técnicos;
* preferencias de asistencia;
* eventos operativos no identificatorios.

La finalidad es validar la existencia de una necesidad de asistencia sin exponer la causa médica, personal o administrativa que la originó.

---

## 6. Preferencias de asistencia

El MVP contempla conceptualmente distintos perfiles de asistencia, bajo control del usuario:

```text
0 = modalidad silenciosa
1 = modalidad discreta
2 = modalidad preventiva
3 = modalidad visible
```

Estos perfiles no clasifican personas ni diagnósticos. Sólo representan preferencias de interacción con el sistema.

La asistencia debe estar al servicio de la autonomía personal y no reemplazarla.

---

## 7. Interoperabilidad

El repositorio incluye módulos orientados a representar posibles integraciones futuras con sistemas públicos o plataformas de validación.

Actualmente, esas integraciones son **simuladas**.

No existe en este repositorio una conexión real con:

* ANDIS;
* SISA;
* RENAPER;
* Mi Argentina;
* Nación Servicios S.A.;
* CNRT;
* otros organismos públicos.

Cualquier integración real requeriría autorización formal, documentación técnica, convenios correspondientes y evaluación de las autoridades competentes.

---

## 8. Bono Solidario

El Bono Solidario se contempla como una **posible evolución futura** de SUBE Prioridad.

No forma parte del núcleo esencial inicial del MVP.

Su finalidad conceptual sería reconocer actos voluntarios de colaboración realizados por pasajeros que cedan asientos de uso general a usuarios de SUBE Prioridad.

El Bono Solidario no debe implementarse como:

* multa;
* castigo;
* obligación;
* ranking público;
* sistema de vigilancia;
* mecanismo de presión social;
* beneficio por ocupar o liberar asientos prioritarios legales.

Cualquier evolución hacia reconocimientos simbólicos, beneficios operativos o incentivos tarifarios debería estar sujeta a validaciones técnicas, controles antifraude, evidencia objetiva y aprobación de las autoridades competentes.

---

## 9. Blindaje antifraude

El MVP incluye una base inicial de motor antifraude para escenarios de reconocimiento futuro.

Principios considerados:

* validación temporal;
* coincidencia de línea;
* coincidencia de unidad;
* correlación de eventos;
* control de recurrencia;
* prevención de colusión entre tarjetas;
* auditoría sin datos personales;
* rechazo de autoasignación.

Ningún evento individual debería ser suficiente para acreditar una interacción de valor.

La confianza del sistema debe surgir de la combinación de múltiples señales verificables.

---

## 10. Arquitectura actual

Archivos principales:

```text
main.py                         API principal FastAPI
validator.py                    Motor antifraude inicial
test_main.py                    Tests de API
test_antifraud.py               Tests del motor antifraude
cache_manager.py                Caché TTL simple
circuit_breaker.py              Protección ante fallas de servicios externos
xroad_gateway.py                Simulador de interoperabilidad
requirements.txt                Dependencias Python
Dockerfile                      Imagen de ejecución
docker-compose.yml              Ejecución local con Docker
ARCHITECTURE_GUARDRAILS.md      Principios de arquitectura
docs/PLIEGO_TECNICO_EXTENDIDO.md Pliego técnico extendido y visión integral
```

---

## 11. Ejecutar localmente

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

Endpoint de salud:

```text
http://127.0.0.1:8000/health
```

---

## 12. Ejecutar tests

```bash
pytest -q
```

Compilar archivos principales:

```bash
python -m py_compile main.py validator.py cache_manager.py circuit_breaker.py xroad_gateway.py
```

---

## 13. Ejecutar con Docker

Construir y ejecutar:

```bash
docker compose up --build
```

La API quedará disponible en:

```text
http://localhost:8000
```

---

## 14. Estado de madurez

Este repositorio debe leerse como:

```text
MVP conceptual: sí
API demostrativa: sí
Tests básicos: sí
CI inicial: sí
Integraciones reales: no
Producción: no
Decisión estatal de implementación: no
Bono Solidario productivo: no
```

---

## 15. Principios de evolución

Toda modificación futura del repositorio deberá respetar:

* accesibilidad universal;
* privacidad desde el diseño;
* minimización de datos;
* autonomía del usuario;
* implementación gradual;
* uso prudente de infraestructura existente;
* neutralidad tecnológica;
* auditabilidad;
* no exposición de datos sensibles;
* no alteración de derechos vigentes;
* no imposición de cargas operativas indebidas.

---

## 16. Documentación complementaria

El repositorio conserva documentación ampliada en:

```text
docs/PLIEGO_TECNICO_EXTENDIDO.md
```

Ese documento debe leerse como una especificación conceptual, prospectiva y evolutiva. No debe interpretarse como una implementación productiva actualmente desplegada ni como una integración real vigente con organismos públicos, sistemas SUBE, validadoras, hardware embarcado o infraestructura estatal.

## Documentación estratégica del proyecto

La documentación principal del repositorio se organiza en los siguientes documentos:

* [`docs/INDICE_DOCUMENTAL.md`](docs/INDICE_DOCUMENTAL.md): guía de lectura y organización general de la documentación.
* [`docs/DOSSIER_INSTITUCIONAL_BREVE.md`](docs/DOSSIER_INSTITUCIONAL_BREVE.md): síntesis institucional para autoridades, legisladores, asesores y ciudadanía.
* [`docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md`](docs/ESTRATEGIA_LEGISLATIVA_Y_PARTICIPACION_CIUDADANA.md): estrategia para impulsar el análisis legislativo, administrativo y ciudadano de la propuesta.
* [`docs/ARQUITECTURA_DE_REFERENCIA.md`](docs/ARQUITECTURA_DE_REFERENCIA.md): visión arquitectónica general del proyecto.
* [`docs/ROADMAP_IMPLEMENTACION.md`](docs/ROADMAP_IMPLEMENTACION.md): hoja de ruta conceptual para una evolución gradual desde MVP hasta eventuales pruebas piloto o implementaciones de mayor escala.
* [`docs/DECISIONES_DE_ARQUITECTURA.md`](docs/DECISIONES_DE_ARQUITECTURA.md): decisiones técnicas y conceptuales que orientan el diseño del sistema.
* [`docs/PRINCIPIOS_DE_GOBERNANZA.md`](docs/PRINCIPIOS_DE_GOBERNANZA.md): criterios de transparencia, protección de datos, auditabilidad y control institucional.
* [`ARCHITECTURE_GUARDRAILS.md`](ARCHITECTURE_GUARDRAILS.md): límites técnicos que toda evolución del código debe respetar.
* [`docs/PLIEGO_TECNICO_EXTENDIDO.md`](docs/PLIEGO_TECNICO_EXTENDIDO.md): documento técnico amplio que conserva la visión integral original del proyecto.

Estos documentos deben leerse de manera complementaria. El repositorio representa actualmente un MVP conceptual y demostrativo; toda implementación real deberá ser evaluada por las autoridades competentes.


---

## 17. Arquitectura de Referencia

La visión de largo plazo del proyecto se documenta en:

```text
docs/ARQUITECTURA_DE_REFERENCIA.md
```

Ese documento describe los principios de ingeniería que orientan la evolución de SUBE Prioridad como una arquitectura abierta, modular, escalable y tecnológicamente neutral.

Su contenido complementa al presente README y al Pliego Técnico Extendido, explicando cómo el MVP conceptual podría evolucionar progresivamente desde pruebas piloto hasta implementaciones de mayor escala, siempre sujetas a evaluación técnica, jurídica, presupuestaria y operativa por parte de las autoridades competentes.

La Arquitectura de Referencia no constituye una especificación obligatoria ni una implementación definitiva, sino un marco conceptual destinado a facilitar futuras decisiones de diseño, interoperabilidad y gobernanza.


## 18. Aporte ciudadano

SUBE Prioridad se presenta como una propuesta ciudadana de interés público, abierta a análisis, mejora, adaptación y eventual evaluación por parte de los organismos competentes.

La iniciativa no se ofrece como solución cerrada ni como explotación comercial privada.

Su valor principal reside en abrir una conversación técnica, institucional y social sobre nuevas formas de fortalecer la accesibilidad, la asistencia preventiva y la convivencia dentro del transporte público.

---

## 19. Licencia y uso

Mientras no se defina una licencia específica, este repositorio debe considerarse material de análisis, documentación y desarrollo conceptual.

Antes de cualquier uso institucional, productivo o comercial, deberán revisarse las condiciones jurídicas, administrativas, técnicas y regulatorias correspondientes.

---

## 20. Declaración final

SUBE Prioridad busca demostrar que una acción cotidiana como la validación de un viaje podría transformarse, cuando las circunstancias lo requieran, en una oportunidad para facilitar asistencia, promover inclusión y fortalecer la solidaridad ciudadana.

El mayor valor del proyecto no reside en una tecnología específica, sino en la posibilidad de utilizar capacidades existentes para construir un transporte público más accesible, seguro, respetuoso y humano.

# Firma y Confianza Institucional — Simulacro Técnico Futuro

## SUBE Prioridad

---

## 1. Finalidad de este documento

Este documento conserva y actualiza una idea técnica inicial del proyecto SUBE Prioridad: demostrar que la propuesta podría apoyarse, en una etapa futura, en mecanismos de confianza digital, firma, validación de integridad y atributos técnicos verificables.

El objetivo no es afirmar que exista una integración real vigente.

El objetivo es mostrar que la tecnología necesaria para proteger un atributo mínimo de prioridad **ya existe**, es técnicamente viable y podría ser analizada por autoridades competentes si el proyecto avanzara hacia etapas institucionales posteriores.

Este documento debe leerse como:

```text
simulacro técnico
documentación futura
prueba conceptual de viabilidad
no implementación oficial
no integración real
no validación médica real
no uso productivo
```

---

## 2. Advertencia institucional expresa

Las referencias a organismos, normas, tecnologías, firmas digitales, certificados, validadores, autoridades certificantes, sistemas estatales o infraestructura pública se utilizan exclusivamente como **referencias conceptuales o ejemplos de tecnologías existentes**.

Su mención no implica:

- participación real de esos organismos;
- autorización institucional;
- convenio vigente;
- adopción oficial;
- integración técnica real;
- validación de certificados reales;
- acceso a bases públicas o privadas;
- conexión con sistemas SUBE reales;
- conexión con sistemas sanitarios reales;
- procesamiento de datos sensibles reales.

El uso de nombres institucionales o normativos en este documento sólo busca mostrar que existen herramientas jurídicas y tecnológicas que podrían servir como referencia para una discusión futura.

---

## 3. Relación con el proyecto original

La idea original de Andrés Federico Di Fiore partía de una intuición central:

```text
si una necesidad ya fue acreditada por fuera del transporte,
el transporte no debería exigir que la persona vuelva a explicar su diagnóstico.
```

Desde esa intuición, el proyecto propone separar dos planos:

```text
acreditación institucional
↓
atributo técnico mínimo
↓
uso operativo en transporte
```

El transporte no necesita conocer el diagnóstico.

El transporte no necesita ver un certificado médico.

El transporte no necesita conocer la historia clínica.

El transporte sólo podría necesitar, en una etapa futura y bajo evaluación competente, saber que existe un atributo técnico previamente habilitado.

---

## 4. Qué se busca demostrar

Este simulacro busca demostrar que es técnicamente posible:

- tomar un atributo mínimo no sensible;
- representarlo como token o hash;
- firmar o proteger su integridad;
- verificar que no haya sido alterado;
- evitar revelar diagnóstico, DNI, CUD, certificado o historia clínica;
- operar con validación local o de borde;
- separar la acreditación de la operación;
- mantener privacidad por diseño.

El punto central es:

```text
no se valida la enfermedad;
no se valida el diagnóstico;
no se valida a la persona frente al chofer;
se verifica la integridad técnica de un atributo mínimo.
```

---

## 5. Qué no hace este simulacro

Este documento y el bloque de código incluido no hacen lo siguiente:

- no validan CUD real;
- no consultan ANDIS;
- no consultan SISA;
- no consultan RENAPER;
- no consultan Mi Argentina;
- no consultan Nación Servicios S.A.;
- no consultan CNRT;
- no verifican firmas digitales reales;
- no usan certificados oficiales reales;
- no procesan datos médicos reales;
- no identifican personas;
- no integran validadoras reales;
- no modifican el sistema SUBE;
- no habilitan una prueba piloto real.

---

## 6. Por qué se conserva esta idea

La idea se conserva porque fue útil para explicar la viabilidad del proyecto ante autoridades, instituciones y personas con capacidad de evaluación técnica.

Su valor está en mostrar que SUBE Prioridad no depende de una tecnología imposible o inexistente.

La propuesta puede apoyarse, en el futuro, en tecnologías ya conocidas:

```text
hashes criptográficos
firmas digitales
tokens verificables
atributos técnicos
validación de integridad
certificados digitales
validación offline
validación en el borde
```

Pero en la versión actual del proyecto, esas tecnologías deben mantenerse como simulacro o línea futura, no como integración real.

---

## 7. Evolución del bloque original

El bloque original mencionaba firma gubernamental, CUD, firma médica, Ley 25.506, ONTI y ANDIS.

Esa formulación tenía fuerza demostrativa, pero podía generar confusión sobre el alcance real del MVP.

Por eso, el bloque se actualiza con tres cambios:

```text
1. Se conserva la idea de confianza institucional.
2. Se elimina cualquier apariencia de validación oficial real.
3. Se transforma el ejemplo en un simulacro técnico no productivo.
```

El nuevo enfoque es más compatible con la versión documental 1.0 de SUBE Prioridad.

---

## 8. Simulacro técnico actualizado

El siguiente bloque conserva el espíritu de la idea inicial, pero la reformula de manera compatible con el MVP conceptual.

Puede ejecutarse como demostración aislada.

No debe integrarse al core productivo del MVP.

```python
"""
SUBE Prioridad — Simulacro de firma y confianza institucional futura.

Este archivo es una demostración conceptual aislada.

No representa integración real con SUBE.
No representa integración real con organismos públicos.
No valida CUD real.
No valida certificados médicos reales.
No procesa diagnósticos.
No procesa DNI.
No consulta bases públicas ni privadas.
No implementa firma gubernamental real.
No reemplaza la acreditación institucional competente.

Finalidad:
    Mostrar que un atributo técnico mínimo, no sensible y previamente
    acreditado por fuera del transporte podría ser protegido mediante
    mecanismos criptográficos existentes, sin revelar datos sensibles.

Nota:
    Las referencias a normas, organismos o tecnologías existentes son
    meramente ilustrativas. No implican participación, autorización,
    convenio ni integración real.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict


PROJECT_NAME = "SUBE Prioridad"
DEMO_VERSION = "0.1.0"
DEMO_MODE = True


PROHIBITED_FIELDS = {
    "dni",
    "documento",
    "nombre",
    "apellido",
    "domicilio",
    "direccion",
    "diagnostico",
    "diagnóstico",
    "historia_clinica",
    "historia_clínica",
    "certificado_medico",
    "certificado_médico",
    "cud",
    "patologia",
    "patología",
    "medico",
    "médico",
    "obra_social",
}


@dataclass(frozen=True)
class AtributoFirmadoDemo:
    """
    Representa un atributo técnico mínimo protegido por una firma simulada.

    No contiene identidad civil.
    No contiene diagnóstico.
    No contiene CUD.
    No contiene certificado médico.
    No contiene historia clínica.
    """

    payload: Dict[str, Any]
    firma_demo: str
    algoritmo: str
    modo: str


class SubeInstitutionalTrustSimulator:
    """
    Simulador de confianza institucional futura para SUBE Prioridad.

    Esta clase reemplaza la idea original de un validador gubernamental
    directo por un simulador neutral de atributo técnico.

    No valida una firma estatal real.
    No usa claves oficiales.
    No consulta organismos.
    No acredita condiciones médicas.
    """

    def __init__(self) -> None:
        """
        Clave demostrativa local.

        En una implementación real, la confianza no debería depender de una
        clave escrita en el código, sino de una arquitectura institucional,
        jurídica, criptográfica y operacional auditada.
        """
        self._demo_trust_anchor = (
            "SUBE_PRIORIDAD_DEMO_TRUST_ANCHOR_NO_PRODUCTIVO"
        ).encode("utf-8")

    def crear_atributo_prioridad_demo(self) -> Dict[str, Any]:
        """
        Crea un atributo técnico mínimo y no sensible.

        El atributo no explica por qué existe la prioridad.
        Sólo indica una preferencia operativa de asistencia.
        """
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=10)

        return {
            "project": PROJECT_NAME,
            "version": DEMO_VERSION,
            "demo_mode": DEMO_MODE,
            "attribute_type": "priority_assistance",
            "priority_status": "demo_active",
            "assistance_preference": "preventive",
            "sensitive_data": False,
            "issued_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
        }

    def firmar_atributo_demo(self, payload: Dict[str, Any]) -> AtributoFirmadoDemo:
        """
        Protege el atributo con una firma HMAC-SHA256 demostrativa.

        HMAC-SHA256 es una primitiva criptográfica real.
        En este ejemplo se usa sólo para demostrar integridad técnica.
        """
        self._assert_no_prohibited_fields(payload)

        mensaje = self._canonical_json(payload)

        firma = hmac.new(
            self._demo_trust_anchor,
            mensaje,
            hashlib.sha256,
        ).hexdigest()

        return AtributoFirmadoDemo(
            payload=payload,
            firma_demo=firma,
            algoritmo="HMAC-SHA256-DEMO",
            modo="simulacro_no_productivo",
        )

    def verificar_atributo_demo(self, atributo: AtributoFirmadoDemo) -> bool:
        """
        Verifica que el atributo no haya sido alterado.

        Devuelve True si el payload coincide con la firma demostrativa.
        Devuelve False si el payload fue modificado.
        """
        self._assert_no_prohibited_fields(atributo.payload)

        mensaje = self._canonical_json(atributo.payload)

        firma_esperada = hmac.new(
            self._demo_trust_anchor,
            mensaje,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(firma_esperada, atributo.firma_demo)

    def simular_alteracion(self, atributo: AtributoFirmadoDemo) -> AtributoFirmadoDemo:
        """
        Modifica el atributo para demostrar que la verificación falla.
        """
        payload_modificado = dict(atributo.payload)
        payload_modificado["assistance_preference"] = "visible"

        return AtributoFirmadoDemo(
            payload=payload_modificado,
            firma_demo=atributo.firma_demo,
            algoritmo=atributo.algoritmo,
            modo=atributo.modo,
        )

    def _canonical_json(self, payload: Dict[str, Any]) -> bytes:
        """
        Serializa el payload de manera estable.

        Esto permite que la firma sea reproducible y verificable.
        """
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

    def _assert_no_prohibited_fields(self, payload: Dict[str, Any]) -> None:
        """
        Impide usar el simulacro con campos sensibles o identificatorios.
        """
        normalized_keys = {str(key).strip().lower() for key in payload.keys()}
        forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

        if forbidden:
            raise ValueError(
                "El atributo contiene campos prohibidos para SUBE Prioridad: "
                + ", ".join(forbidden)
            )


def main() -> None:
    simulator = SubeInstitutionalTrustSimulator()

    atributo = simulator.crear_atributo_prioridad_demo()
    firmado = simulator.firmar_atributo_demo(atributo)

    print("SUBE Prioridad — Simulacro de confianza institucional futura")
    print("Estado: demostrativo, no productivo, no oficial")
    print()

    print("Atributo técnico no sensible:")
    print(json.dumps(firmado.payload, indent=2, ensure_ascii=False))
    print()

    print("Algoritmo demostrativo:")
    print(firmado.algoritmo)
    print()

    print("Firma válida sobre atributo original:")
    print(simulator.verificar_atributo_demo(firmado))
    print()

    alterado = simulator.simular_alteracion(firmado)

    print("Firma válida luego de alterar el atributo:")
    print(simulator.verificar_atributo_demo(alterado))
    print()

    print("Conclusión:")
    print(
        "El simulacro demuestra que un atributo técnico mínimo puede "
        "protegerse criptográficamente sin incluir DNI, diagnóstico, CUD, "
        "certificado médico, historia clínica ni datos sensibles."
    )


if __name__ == "__main__":
    main()
```

---

## 9. Resultado esperado del simulacro

La ejecución conceptual del bloque debería mostrar:

```text
Firma válida sobre atributo original:
True

Firma válida luego de alterar el atributo:
False
```

Esto demuestra una idea importante:

```text
si el atributo técnico es alterado,
la verificación falla.
```

Esa lógica permite explicar que la propuesta es técnicamente viable sin convertir al sistema de transporte en evaluador médico.

---

## 10. Diferencia con una implementación real

Este simulacro usa una clave demostrativa local.

Una implementación real no debería usar claves escritas en el código.

Una implementación real requeriría:

- autoridad competente;
- marco jurídico;
- evaluación de protección de datos;
- infraestructura de confianza;
- gestión segura de claves;
- revocación;
- vencimiento;
- auditoría;
- trazabilidad no invasiva;
- documentación pública;
- revisión técnica independiente;
- gobernanza institucional;
- prueba piloto limitada.

---

## 11. Relación con CUD, certificados y datos médicos

El proyecto no descarta que, en una etapa futura y bajo decisión institucional competente, una necesidad previamente acreditada pueda originarse en registros, certificados o trámites existentes.

Pero el core operativo de SUBE Prioridad no debe procesar esa documentación.

La arquitectura correcta es:

```text
documentación sensible o acreditación
permanece fuera del transporte

atributo técnico mínimo
puede operar dentro del sistema
```

Por eso, este simulacro no usa CUD real.

No usa firma médica real.

No usa diagnóstico.

No usa identidad civil.

No usa historia clínica.

---

## 12. Por qué este enfoque fortalece la viabilidad

Este enfoque permite explicar a autoridades e instituciones que SUBE Prioridad no requiere inventar tecnología desde cero.

La propuesta puede dialogar, en una etapa futura, con herramientas ya conocidas:

```text
tokens
hashes
firmas
atributos verificables
validación offline
validación de borde
certificados digitales
infraestructura de confianza
```

Pero mantiene una regla prudente:

```text
la viabilidad técnica no equivale a implementación vigente.
```

---

## 13. Fórmula institucional recomendada

Para explicar este simulacro ante autoridades, puede utilizarse la siguiente fórmula:

```text
SUBE Prioridad no propone que el transporte conozca diagnósticos ni certificados médicos.

La propuesta demuestra que, si una autoridad competente acreditara previamente una necesidad de asistencia, esa acreditación podría traducirse en un atributo técnico mínimo, no sensible y verificable.

El simulacro muestra que la integridad de ese atributo puede protegerse con tecnologías criptográficas existentes, sin exponer datos sensibles ni convertir al chofer o al validador en evaluadores médicos.
```

---

## 14. Regla de uso de nombres reales

Cuando este documento mencione normas, organismos, tecnologías, estándares, sistemas o infraestructuras existentes, debe entenderse bajo esta regla:

```text
la mención es ilustrativa;
la mención no implica participación;
la mención no implica autorización;
la mención no implica integración real;
la mención no implica obligación futura;
la mención no implica adopción institucional;
la mención sólo demuestra que existen referencias técnicas o jurídicas posibles.
```

Esta regla protege el proyecto frente a confusiones institucionales.

---

## 15. Relación con el MVP actual

El MVP actual debe seguir siendo mínimo.

El core del proyecto no necesita implementar firma institucional real.

El core sólo necesita demostrar:

```text
atributo técnico no sensible
preferencia de asistencia
validación demostrativa
rechazo de datos prohibidos
respuesta genérica
privacidad por diseño
```

Este documento pertenece a una línea futura.

No debe mezclarse con el código principal del MVP.

---

## 16. Relación con el documento de confianza institucional

Este documento se complementa con:

```text
docs/futuro/CONFIANZA_INSTITUCIONAL_Y_ATRIBUTOS.md
```

La diferencia es:

```text
CONFIANZA_INSTITUCIONAL_Y_ATRIBUTOS.md
explica la arquitectura futura de confianza institucional.

FIRMA_Y_CONFIANZA_INSTITUCIONAL.md
conserva el simulacro técnico que demuestra viabilidad criptográfica.
```

Ambos documentos deben interpretarse como futuros, conceptuales y no productivos.

---

## 17. Decisión de arquitectura

La decisión actual es:

```text
no incorporar firma institucional real al core del MVP;
sí conservar un simulacro técnico aislado para demostrar viabilidad.
```

Esto permite equilibrar dos necesidades:

```text
prudencia institucional
+
fuerza demostrativa técnica
```

---

## 18. Cierre

La idea inicial de firma y confianza institucional fue valiosa porque permitió mostrar que SUBE Prioridad no es una fantasía tecnológica.

Sin embargo, la versión actual del proyecto exige mayor precisión.

Por eso, la idea se conserva como simulacro técnico futuro, con límites claros:

```text
no implementación oficial
no integración real
no validación de CUD real
no firma médica real
no datos sensibles
no vigilancia
no sanción
no sobrecarga al chofer
```

El valor del simulacro está en demostrar que un atributo técnico mínimo, previamente acreditado por fuera del transporte, podría protegerse con tecnologías existentes sin revelar la razón médica, social o funcional que justifica la asistencia.

La regla final se mantiene:

```text
el transporte no necesita conocer el diagnóstico.
```

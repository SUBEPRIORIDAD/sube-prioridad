"""
SUBE Prioridad — Simulador MVP de atributo técnico no sensible.

Este módulo forma parte del MVP conceptual y demostrativo.

No representa una implementación oficial vigente.
No representa integración real con SUBE.
No representa conexión real con organismos públicos.
No modifica validadoras reales.
No procesa DNI.
No procesa nombre ni apellido.
No procesa domicilio.
No procesa diagnóstico.
No procesa historia clínica.
No procesa CUD.
No procesa certificados médicos.
No almacena datos sensibles.
No genera sanciones.
No genera vigilancia.
No reemplaza derechos vigentes.
No impone cargas al personal de conducción.

Finalidad:
    Mostrar, con código simple y ejecutable, cómo una necesidad previamente
    acreditada fuera del transporte podría representarse como un atributo
    técnico mínimo, no sensible y demostrativo para facilitar asistencia
    preventiva.

Uso:
    python mvp_simulator.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List


PROJECT_NAME = "SUBE Prioridad"
MVP_VERSION = "0.2.0"
DEMO_MODE = True


PROHIBITED_FIELDS = {
    "dni",
    "documento",
    "nombre",
    "apellido",
    "domicilio",
    "direccion",
    "dirección",
    "diagnostico",
    "diagnóstico",
    "historia_clinica",
    "historia_clínica",
    "certificado_medico",
    "certificado_médico",
    "cud",
    "discapacidad",
    "patologia",
    "patología",
    "medico",
    "médico",
    "obra_social",
    "telefono",
    "teléfono",
    "email",
    "correo",
}


class AssistancePreference(str, Enum):
    """
    Preferencias demostrativas de asistencia.

    Estas categorías no son diagnósticos.
    No describen una condición médica.
    Sólo indican la modalidad de experiencia operativa deseada.
    """

    SILENCIOSA = "silenciosa"
    DISCRETA = "discreta"
    PREVENTIVA = "preventiva"
    VISIBLE = "visible"


class ValidationStatus(str, Enum):
    """
    Estados demostrativos del simulador MVP.
    """

    VALID = "valid"
    INVALID = "invalid"


@dataclass(frozen=True)
class PriorityAttribute:
    """
    Atributo técnico mínimo y no sensible.

    No contiene identidad civil.
    No contiene diagnóstico.
    No contiene CUD.
    No contiene certificado médico.
    No contiene historia clínica.
    """

    token: str
    assistance_preference: AssistancePreference
    demo_accreditation: bool = True


@dataclass(frozen=True)
class MvpSimulationResult:
    """
    Resultado operativo simulado.

    La respuesta es genérica y no revela la causa de la prioridad.
    """

    project: str
    version: str
    demo_mode: bool
    status: ValidationStatus
    assistance_preference: AssistancePreference | None
    alert_message: str
    driver_burden: str
    privacy_notice: str
    timestamp_utc: str
    warnings: List[str]


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza cualquier payload que intente incluir datos sensibles,
    identificatorios o incompatibles con el MVP.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_priority_attribute(
    token: str,
    assistance_preference: AssistancePreference,
) -> PriorityAttribute:
    """
    Crea un atributo demostrativo de prioridad.

    El token es conceptual.
    No representa una tarjeta SUBE real.
    No representa una credencial real.
    No representa una persona identificada.
    """
    if not token or not token.strip():
        raise ValueError("El token demostrativo no puede estar vacío.")

    return PriorityAttribute(
        token=token.strip(),
        assistance_preference=assistance_preference,
        demo_accreditation=True,
    )


def simulate_priority_validation(
    attribute: PriorityAttribute,
    context: Dict[str, Any] | None = None,
) -> MvpSimulationResult:
    """
    Simula la validación operativa de un atributo técnico de prioridad.

    El contexto puede incluir datos operativos no sensibles, por ejemplo:
        vehicle_demo_id
        route_demo_id
        validator_demo_id

    No deben incluirse datos personales ni sensibles.
    """
    context = context or {}
    assert_no_prohibited_fields(context)

    if not attribute.demo_accreditation:
        return _invalid_result("Atributo demostrativo no acreditado.")

    if not attribute.token.startswith("demo-priority-"):
        return _invalid_result("Token demostrativo inválido.")

    return MvpSimulationResult(
        project=PROJECT_NAME,
        version=MVP_VERSION,
        demo_mode=DEMO_MODE,
        status=ValidationStatus.VALID,
        assistance_preference=attribute.assistance_preference,
        alert_message=_build_alert_message(attribute.assistance_preference),
        driver_burden=(
            "El personal de conducción no evalúa diagnósticos, "
            "no solicita certificados y no administra datos sensibles."
        ),
        privacy_notice=(
            "La validación demostrativa no revela DNI, nombre, diagnóstico, "
            "CUD, certificado médico ni historia clínica."
        ),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        warnings=[
            "MVP conceptual y demostrativo.",
            "Sin integración real con SUBE.",
            "Sin conexión real con organismos públicos.",
            "Sin procesamiento de datos sensibles reales.",
            "Sin sanciones, vigilancia ni ranking de pasajeros.",
        ],
    )


def _build_alert_message(preference: AssistancePreference) -> str:
    """
    Construye una alerta genérica y no diagnóstica.
    """
    messages = {
        AssistancePreference.SILENCIOSA: (
            "Preferencia silenciosa registrada. Sin alerta visible."
        ),
        AssistancePreference.DISCRETA: (
            "Asistencia prioritaria solicitada de manera discreta."
        ),
        AssistancePreference.PREVENTIVA: (
            "Asistencia preventiva sugerida. Se recomienda facilitar condiciones de viaje."
        ),
        AssistancePreference.VISIBLE: (
            "Asistencia prioritaria visible solicitada. Mensaje genérico sin diagnóstico."
        ),
    }

    return messages[preference]


def _invalid_result(reason: str) -> MvpSimulationResult:
    """
    Resultado inválido sin exponer información sensible.
    """
    return MvpSimulationResult(
        project=PROJECT_NAME,
        version=MVP_VERSION,
        demo_mode=DEMO_MODE,
        status=ValidationStatus.INVALID,
        assistance_preference=None,
        alert_message=reason,
        driver_burden=(
            "El personal de conducción no debe resolver la validez del atributo."
        ),
        privacy_notice=(
            "No se procesa ni solicita información sensible para esta respuesta."
        ),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        warnings=[
            "Validación demostrativa.",
            "Sin datos sensibles.",
            "Sin decisión médica.",
            "Sin sanción.",
        ],
    )


def result_to_dict(result: MvpSimulationResult) -> Dict[str, Any]:
    """
    Convierte el resultado a diccionario serializable.
    """
    return {
        "project": result.project,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "assistance_preference": (
            result.assistance_preference.value
            if result.assistance_preference is not None
            else None
        ),
        "alert_message": result.alert_message,
        "driver_burden": result.driver_burden,
        "privacy_notice": result.privacy_notice,
        "timestamp_utc": result.timestamp_utc,
        "warnings": result.warnings,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una simulación completa del MVP.

    Esta función es útil para GitHub Actions, pruebas locales y demostraciones.
    """
    attribute = create_demo_priority_attribute(
        token="demo-priority-attribute-001",
        assistance_preference=AssistancePreference.PREVENTIVA,
    )

    result = simulate_priority_validation(
        attribute=attribute,
        context={
            "vehicle_demo_id": "demo-bus-001",
            "route_demo_id": "demo-route-001",
            "validator_demo_id": "demo-validator-001",
        },
    )

    return result_to_dict(result)


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))

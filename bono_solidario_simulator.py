"""
SUBE Prioridad — Simulador conceptual de Bono Solidario.

Este módulo forma parte de una línea futura, opcional y separada del core
inicial de prioridad.

No representa implementación oficial vigente.
No representa integración real con SUBE.
No representa integración real con Red SUBE.
No acredita puntos reales.
No otorga beneficios reales.
No modifica tarifas.
No procesa DNI.
No procesa nombre ni apellido.
No procesa domicilio.
No procesa diagnóstico.
No procesa historia clínica.
No procesa CUD.
No procesa certificados médicos.
No genera sanciones.
No genera rankings.
No genera vigilancia.
No obliga a pasajeros.
No impone cargas al personal de conducción.

Finalidad:
    Demostrar, de manera conceptual y ejecutable, cómo podría registrarse
    un reconocimiento solidario futuro cuando un usuario SUBE Prioridad
    decide voluntariamente reconocer que otra persona le cedió un asiento
    de uso general dentro de un transporte público de Argentina.

Regla central:
    El Bono Solidario queda en manos del usuario SUBE Prioridad.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Bono Solidario"
SIMULATOR_VERSION = "0.1.0"
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


class SeatType(str, Enum):
    """
    Tipo de asiento involucrado en el acto solidario.

    El Bono Solidario sólo debe considerarse para asientos de uso general.
    No debe premiar la liberación de asientos prioritarios legales.
    """

    GENERAL_USE = "general_use"
    LEGAL_PRIORITY = "legal_priority"


class SolidaryRecognitionStatus(str, Enum):
    """
    Estados posibles del reconocimiento solidario demostrativo.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True)
class TransportContext:
    """
    Contexto operativo mínimo y demostrativo.

    No representa una unidad real.
    No representa una línea real.
    No representa una operación productiva.
    """

    country: str
    vehicle_demo_id: str
    route_demo_id: str
    trip_demo_id: str
    time_window_demo_id: str


@dataclass(frozen=True)
class SolidarySeatYieldEvent:
    """
    Evento conceptual de cesión voluntaria de asiento.

    El evento no identifica personas reales.
    Sólo representa tokens demostrativos no sensibles.
    """

    priority_user_token: str
    collaborator_token: str
    seat_type: SeatType
    voluntary_seat_yield: bool
    priority_user_decides_to_recognize: bool
    transport_context: TransportContext


@dataclass(frozen=True)
class SolidaryRecognitionResult:
    """
    Resultado del reconocimiento solidario demostrativo.

    No acredita puntos reales.
    No sincroniza con Red SUBE real.
    No otorga beneficios reales.
    """

    project: str
    module: str
    version: str
    demo_mode: bool
    status: SolidaryRecognitionStatus
    solidary_point_demo: int
    recognition_enabled_by_priority_user: bool
    same_transport_context: bool
    reason: str
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    timestamp_utc: str


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza cualquier payload que intente incluir datos personales,
    sensibles, médicos o incompatibles con el proyecto.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_transport_context(
    country: str = "Argentina",
    vehicle_demo_id: str = "demo-bus-001",
    route_demo_id: str = "demo-route-001",
    trip_demo_id: str = "demo-trip-001",
    time_window_demo_id: str = "demo-window-001",
) -> TransportContext:
    """
    Crea un contexto demostrativo de transporte público de Argentina.

    La referencia a Argentina responde al alcance conceptual del proyecto.
    No representa operación real.
    """
    return TransportContext(
        country=country,
        vehicle_demo_id=vehicle_demo_id,
        route_demo_id=route_demo_id,
        trip_demo_id=trip_demo_id,
        time_window_demo_id=time_window_demo_id,
    )


def create_demo_solidary_event(
    priority_user_token: str,
    collaborator_token: str,
    priority_user_decides_to_recognize: bool,
    seat_type: SeatType = SeatType.GENERAL_USE,
    voluntary_seat_yield: bool = True,
    transport_context: Optional[TransportContext] = None,
) -> SolidarySeatYieldEvent:
    """
    Crea un evento demostrativo de cesión voluntaria de asiento.

    El reconocimiento queda siempre en manos del usuario SUBE Prioridad.
    """
    if not priority_user_token or not priority_user_token.strip():
        raise ValueError("El token demostrativo del usuario SUBE Prioridad no puede estar vacío.")

    if not collaborator_token or not collaborator_token.strip():
        raise ValueError("El token demostrativo del colaborador no puede estar vacío.")

    payload = {
        "priority_user_token": priority_user_token,
        "collaborator_token": collaborator_token,
    }
    assert_no_prohibited_fields(payload)

    return SolidarySeatYieldEvent(
        priority_user_token=priority_user_token.strip(),
        collaborator_token=collaborator_token.strip(),
        seat_type=seat_type,
        voluntary_seat_yield=voluntary_seat_yield,
        priority_user_decides_to_recognize=priority_user_decides_to_recognize,
        transport_context=transport_context or create_demo_transport_context(),
    )


def simulate_solidary_recognition(
    event: SolidarySeatYieldEvent,
    expected_context: Optional[TransportContext] = None,
) -> SolidaryRecognitionResult:
    """
    Simula el reconocimiento conceptual del Bono Solidario.

    Condiciones mínimas:
        - transporte público de Argentina;
        - cesión voluntaria;
        - asiento de uso general;
        - decisión voluntaria del usuario SUBE Prioridad;
        - mismo contexto demostrativo de transporte;
        - sin datos sensibles;
        - sin intervención del chofer.
    """
    assert_no_prohibited_fields(
        {
            "priority_user_token": event.priority_user_token,
            "collaborator_token": event.collaborator_token,
        }
    )

    same_context = _same_transport_context(
        event.transport_context,
        expected_context or event.transport_context,
    )

    if event.transport_context.country.strip().lower() != "argentina":
        return _rejected_result(
            reason=(
                "El Bono Solidario conceptual está pensado para transporte público "
                "de Argentina. Este evento demostrativo no cumple ese contexto."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
        )

    if not event.voluntary_seat_yield:
        return _rejected_result(
            reason=(
                "No se registra una cesión voluntaria de asiento. "
                "Sin acto solidario voluntario no corresponde punto solidario demostrativo."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
        )

    if event.seat_type != SeatType.GENERAL_USE:
        return _rejected_result(
            reason=(
                "El Bono Solidario no debe premiar la liberación de asientos prioritarios legales. "
                "Sólo puede analizarse sobre asientos de uso general."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
        )

    if not event.priority_user_decides_to_recognize:
        return _rejected_result(
            reason=(
                "El usuario SUBE Prioridad no decidió reconocer el acto solidario. "
                "El Bono Solidario queda en manos del usuario SUBE Prioridad y no es automático."
            ),
            recognition_enabled_by_priority_user=False,
            same_transport_context=same_context,
        )

    if not same_context:
        return _rejected_result(
            reason=(
                "No se verifica el mismo contexto demostrativo de transporte. "
                "El reconocimiento futuro requiere coincidencia mínima de unidad, línea, viaje "
                "o ventana temporal."
            ),
            recognition_enabled_by_priority_user=True,
            same_transport_context=False,
        )

    return SolidaryRecognitionResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=SIMULATOR_VERSION,
        demo_mode=DEMO_MODE,
        status=SolidaryRecognitionStatus.ACCEPTED,
        solidary_point_demo=1,
        recognition_enabled_by_priority_user=True,
        same_transport_context=True,
        reason=(
            "Reconocimiento solidario demostrativo aceptado. "
            "El usuario SUBE Prioridad decidió voluntariamente reconocer una cesión "
            "de asiento de uso general dentro de un transporte público de Argentina."
        ),
        privacy_notice=(
            "El reconocimiento no revela DNI, nombre, diagnóstico, CUD, certificado médico "
            "ni historia clínica."
        ),
        driver_burden=(
            "El personal de conducción no verifica, no decide, no media y no administra "
            "el Bono Solidario."
        ),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: SolidaryRecognitionResult) -> Dict[str, Any]:
    """
    Convierte el resultado a un diccionario serializable.
    """
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "solidary_point_demo": result.solidary_point_demo,
        "recognition_enabled_by_priority_user": result.recognition_enabled_by_priority_user,
        "same_transport_context": result.same_transport_context,
        "reason": result.reason,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una simulación completa del Bono Solidario.

    Esta función sirve para pruebas locales y GitHub Actions.
    """
    context = create_demo_transport_context()

    event = create_demo_solidary_event(
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
    )

    return result_to_dict(result)


def _same_transport_context(
    actual: TransportContext,
    expected: TransportContext,
) -> bool:
    """
    Verifica coincidencia mínima demostrativa del contexto operativo.

    No realiza geolocalización real.
    No consulta sistemas externos.
    No identifica personas.
    """
    return (
        actual.country == expected.country
        and actual.vehicle_demo_id == expected.vehicle_demo_id
        and actual.route_demo_id == expected.route_demo_id
        and actual.trip_demo_id == expected.trip_demo_id
        and actual.time_window_demo_id == expected.time_window_demo_id
    )


def _rejected_result(
    reason: str,
    recognition_enabled_by_priority_user: bool,
    same_transport_context: bool,
) -> SolidaryRecognitionResult:
    return SolidaryRecognitionResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=SIMULATOR_VERSION,
        demo_mode=DEMO_MODE,
        status=SolidaryRecognitionStatus.REJECTED,
        solidary_point_demo=0,
        recognition_enabled_by_priority_user=recognition_enabled_by_priority_user,
        same_transport_context=same_transport_context,
        reason=reason,
        privacy_notice=(
            "No se procesa ni solicita información sensible para esta respuesta."
        ),
        driver_burden=(
            "El personal de conducción no debe resolver ni administrar el reconocimiento."
        ),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def _common_warnings() -> List[str]:
    return [
        "Módulo futuro, opcional y separado del core de prioridad.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin puntos reales.",
        "Sin beneficios reales.",
        "Sin modificación tarifaria.",
        "Sin datos sensibles.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
        "Sin sanciones.",
        "Sin ranking público.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "El Bono Solidario queda en manos del usuario SUBE Prioridad.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))

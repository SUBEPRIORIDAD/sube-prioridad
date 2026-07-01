"""
SUBE Prioridad — Simulador conceptual blindado de Bono Solidario.

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

Regla de blindaje:
    Ningún evento individual debe ser suficiente por sí solo para construir
    confianza productiva. Esta demo usa validaciones mínimas, límites y
    señales de riesgo para mostrar cómo evitar abusos sin convertir el
    sistema en una herramienta de vigilancia.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Bono Solidario"
SIMULATOR_VERSION = "0.2.0"
DEMO_MODE = True

DEFAULT_EVENT_TTL_MINUTES = 5
MAX_RECOGNITIONS_PER_PRIORITY_USER_PER_TRIP = 1
MAX_RECOGNITIONS_PER_COLLABORATOR_PER_TRIP = 2


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

    ACCEPTED:
        El evento cumple las reglas mínimas de la demo.

    REJECTED:
        El evento incumple una regla dura.

    NEEDS_REVIEW:
        El evento no necesariamente es inválido, pero presenta un patrón
        que en una implementación futura debería revisarse antes de acreditar
        cualquier reconocimiento.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class TransportContext:
    """
    Contexto operativo mínimo y demostrativo.

    No representa una unidad real.
    No representa una línea real.
    No representa una operación productiva.
    No implica geolocalización.
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

    event_demo_id: str
    priority_user_token: str
    collaborator_token: str
    seat_type: SeatType
    voluntary_seat_yield: bool
    priority_user_decides_to_recognize: bool
    transport_context: TransportContext
    issued_at_utc: datetime
    expires_at_utc: datetime


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
    review_required: bool
    risk_flags: List[str]
    reason: str
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    timestamp_utc: str


@dataclass
class DemoRecognitionLedger:
    """
    Libro demostrativo en memoria para blindaje del Bono Solidario.

    No es una base de datos.
    No persiste información real.
    No identifica personas reales.
    Sólo permite simular reglas anti-replay y límites por viaje.
    """

    used_event_ids: Set[str] = field(default_factory=set)
    recognitions_by_priority_user_trip: Dict[str, int] = field(default_factory=dict)
    recognitions_by_collaborator_trip: Dict[str, int] = field(default_factory=dict)

    def register_accepted_event(self, event: SolidarySeatYieldEvent) -> None:
        """
        Registra un evento aceptado dentro del ledger demostrativo.
        """
        self.used_event_ids.add(event.event_demo_id)

        priority_key = _priority_user_trip_key(event)
        collaborator_key = _collaborator_trip_key(event)

        self.recognitions_by_priority_user_trip[priority_key] = (
            self.recognitions_by_priority_user_trip.get(priority_key, 0) + 1
        )
        self.recognitions_by_collaborator_trip[collaborator_key] = (
            self.recognitions_by_collaborator_trip.get(collaborator_key, 0) + 1
        )


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
    event_demo_id: str = "demo-solidary-event-001",
    seat_type: SeatType = SeatType.GENERAL_USE,
    voluntary_seat_yield: bool = True,
    transport_context: Optional[TransportContext] = None,
    issued_at_utc: Optional[datetime] = None,
    ttl_minutes: int = DEFAULT_EVENT_TTL_MINUTES,
) -> SolidarySeatYieldEvent:
    """
    Crea un evento demostrativo de cesión voluntaria de asiento.

    El reconocimiento queda siempre en manos del usuario SUBE Prioridad.
    """
    if not event_demo_id or not event_demo_id.strip():
        raise ValueError("El identificador demostrativo del evento no puede estar vacío.")

    if not priority_user_token or not priority_user_token.strip():
        raise ValueError("El token demostrativo del usuario SUBE Prioridad no puede estar vacío.")

    if not collaborator_token or not collaborator_token.strip():
        raise ValueError("El token demostrativo del colaborador no puede estar vacío.")

    payload = {
        "event_demo_id": event_demo_id,
        "priority_user_token": priority_user_token,
        "collaborator_token": collaborator_token,
    }
    assert_no_prohibited_fields(payload)

    issued_at = issued_at_utc or datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=ttl_minutes)

    return SolidarySeatYieldEvent(
        event_demo_id=event_demo_id.strip(),
        priority_user_token=priority_user_token.strip(),
        collaborator_token=collaborator_token.strip(),
        seat_type=seat_type,
        voluntary_seat_yield=voluntary_seat_yield,
        priority_user_decides_to_recognize=priority_user_decides_to_recognize,
        transport_context=transport_context or create_demo_transport_context(),
        issued_at_utc=issued_at,
        expires_at_utc=expires_at,
    )


def simulate_solidary_recognition(
    event: SolidarySeatYieldEvent,
    expected_context: Optional[TransportContext] = None,
    ledger: Optional[DemoRecognitionLedger] = None,
    now_utc: Optional[datetime] = None,
) -> SolidaryRecognitionResult:
    """
    Simula el reconocimiento conceptual del Bono Solidario.

    Condiciones mínimas:
        - transporte público de Argentina;
        - cesión voluntaria;
        - asiento de uso general;
        - decisión voluntaria del usuario SUBE Prioridad;
        - mismo contexto demostrativo de transporte;
        - evento no expirado;
        - evento no reutilizado;
        - usuario prioritario y colaborador no pueden ser el mismo token;
        - límites demostrativos por viaje;
        - sin datos sensibles;
        - sin intervención del chofer.
    """
    assert_no_prohibited_fields(
        {
            "event_demo_id": event.event_demo_id,
            "priority_user_token": event.priority_user_token,
            "collaborator_token": event.collaborator_token,
        }
    )

    ledger = ledger or DemoRecognitionLedger()
    current_time = now_utc or datetime.now(timezone.utc)

    risk_flags: List[str] = []

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
            risk_flags=["outside_argentina_context"],
        )

    if _looks_like_free_text(event.priority_user_token):
        return _rejected_result(
            reason=(
                "El token del usuario SUBE Prioridad parece texto libre. "
                "El simulador sólo acepta tokens técnicos demostrativos."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
            risk_flags=["priority_user_token_looks_like_free_text"],
        )

    if _looks_like_free_text(event.collaborator_token):
        return _rejected_result(
            reason=(
                "El token del colaborador parece texto libre. "
                "El simulador sólo acepta tokens técnicos demostrativos."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
            risk_flags=["collaborator_token_looks_like_free_text"],
        )

    if event.priority_user_token == event.collaborator_token:
        return _rejected_result(
            reason=(
                "El usuario SUBE Prioridad y el colaborador no pueden ser el mismo token. "
                "Esto evita auto-reconocimientos demostrativos."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
            risk_flags=["self_recognition_attempt"],
        )

    if event.event_demo_id in ledger.used_event_ids:
        return _rejected_result(
            reason=(
                "El evento demostrativo ya fue utilizado. "
                "Esto evita replay fraud o reutilización del mismo reconocimiento."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
            risk_flags=["replay_event_id"],
        )

    if current_time > event.expires_at_utc:
        return _rejected_result(
            reason=(
                "El evento demostrativo expiró. "
                "El Bono Solidario futuro debería operar dentro de una ventana temporal breve."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
            risk_flags=["expired_event"],
        )

    if not event.voluntary_seat_yield:
        return _rejected_result(
            reason=(
                "No se registra una cesión voluntaria de asiento. "
                "Sin acto solidario voluntario no corresponde punto solidario demostrativo."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
            risk_flags=["no_voluntary_seat_yield"],
        )

    if event.seat_type != SeatType.GENERAL_USE:
        return _rejected_result(
            reason=(
                "El Bono Solidario no debe premiar la liberación de asientos prioritarios legales. "
                "Sólo puede analizarse sobre asientos de uso general."
            ),
            recognition_enabled_by_priority_user=event.priority_user_decides_to_recognize,
            same_transport_context=same_context,
            risk_flags=["legal_priority_seat_not_eligible"],
        )

    if not event.priority_user_decides_to_recognize:
        return _rejected_result(
            reason=(
                "El usuario SUBE Prioridad no decidió reconocer el acto solidario. "
                "El Bono Solidario queda en manos del usuario SUBE Prioridad y no es automático."
            ),
            recognition_enabled_by_priority_user=False,
            same_transport_context=same_context,
            risk_flags=["priority_user_did_not_recognize"],
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
            risk_flags=["different_transport_context"],
        )

    priority_key = _priority_user_trip_key(event)
    collaborator_key = _collaborator_trip_key(event)

    priority_user_count = ledger.recognitions_by_priority_user_trip.get(priority_key, 0)
    collaborator_count = ledger.recognitions_by_collaborator_trip.get(collaborator_key, 0)

    if priority_user_count >= MAX_RECOGNITIONS_PER_PRIORITY_USER_PER_TRIP:
        return _needs_review_result(
            reason=(
                "El usuario SUBE Prioridad ya emitió un reconocimiento en este viaje demostrativo. "
                "Un nuevo reconocimiento no se rechaza por sanción, pero debería requerir revisión "
                "antes de acreditar cualquier punto futuro."
            ),
            recognition_enabled_by_priority_user=True,
            same_transport_context=True,
            risk_flags=["priority_user_trip_limit_exceeded"],
        )

    if collaborator_count >= MAX_RECOGNITIONS_PER_COLLABORATOR_PER_TRIP:
        return _needs_review_result(
            reason=(
                "El colaborador registra múltiples reconocimientos en el mismo viaje demostrativo. "
                "Este patrón podría ser legítimo, pero requiere revisión para evitar colusión "
                "o acumulación artificial de puntos."
            ),
            recognition_enabled_by_priority_user=True,
            same_transport_context=True,
            risk_flags=["collaborator_trip_limit_exceeded"],
        )

    ledger.register_accepted_event(event)

    return SolidaryRecognitionResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=SIMULATOR_VERSION,
        demo_mode=DEMO_MODE,
        status=SolidaryRecognitionStatus.ACCEPTED,
        solidary_point_demo=1,
        recognition_enabled_by_priority_user=True,
        same_transport_context=True,
        review_required=False,
        risk_flags=[],
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
        "review_required": result.review_required,
        "risk_flags": result.risk_flags,
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
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-001",
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
        ledger=ledger,
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


def _priority_user_trip_key(event: SolidarySeatYieldEvent) -> str:
    return "|".join(
        [
            event.priority_user_token,
            event.transport_context.vehicle_demo_id,
            event.transport_context.route_demo_id,
            event.transport_context.trip_demo_id,
            event.transport_context.time_window_demo_id,
        ]
    )


def _collaborator_trip_key(event: SolidarySeatYieldEvent) -> str:
    return "|".join(
        [
            event.collaborator_token,
            event.transport_context.vehicle_demo_id,
            event.transport_context.route_demo_id,
            event.transport_context.trip_demo_id,
            event.transport_context.time_window_demo_id,
        ]
    )


def _looks_like_free_text(token: str) -> bool:
    """
    Detecta valores que parecen frases libres o intentos de abuso.

    La demo no interpreta frases.
    Sólo acepta tokens técnicos demostrativos simples.
    """
    normalized = token.lower().strip()

    suspicious_terms = {
        "quiero",
        "gratis",
        "beneficio",
        "bono",
        "solidario",
        "tarifa",
        "social",
        "diagnostico",
        "diagnóstico",
        "cud",
        "certificado",
        "medico",
        "médico",
        "andis",
        "sancion",
        "sanción",
        "ranking",
    }

    if any(term in normalized for term in suspicious_terms):
        return True

    if len(normalized.split()) > 1:
        return True

    return False


def _rejected_result(
    reason: str,
    recognition_enabled_by_priority_user: bool,
    same_transport_context: bool,
    risk_flags: Optional[List[str]] = None,
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
        review_required=False,
        risk_flags=risk_flags or [],
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


def _needs_review_result(
    reason: str,
    recognition_enabled_by_priority_user: bool,
    same_transport_context: bool,
    risk_flags: Optional[List[str]] = None,
) -> SolidaryRecognitionResult:
    return SolidaryRecognitionResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=SIMULATOR_VERSION,
        demo_mode=DEMO_MODE,
        status=SolidaryRecognitionStatus.NEEDS_REVIEW,
        solidary_point_demo=0,
        recognition_enabled_by_priority_user=recognition_enabled_by_priority_user,
        same_transport_context=same_transport_context,
        review_required=True,
        risk_flags=risk_flags or [],
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

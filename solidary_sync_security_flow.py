"""
SUBE Prioridad — Flujo de seguridad para sincronización solidaria.

Este módulo modela de manera conceptual el blindaje entre:

    usuario SUBE Prioridad
    pasajero que cede voluntariamente un asiento de uso general
    contexto demostrativo de transporte
    confirmación voluntaria del usuario prioritario
    sincronización no productiva
    control antifraude

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No acredita puntos reales.
No otorga beneficios reales.
No modifica tarifas.
No procesa DNI.
No procesa nombre.
No procesa domicilio.
No procesa diagnóstico.
No procesa CUD.
No procesa certificados médicos.
No genera sanciones.
No genera rankings.
No genera vigilancia.
No impone cargas al chofer.

Regla central:
    El colaborador no puede reclamar solo.
    El chofer no decide.
    El sistema no premia asientos prioritarios legales.
    El usuario SUBE Prioridad conserva el control de la confirmación.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Flujo de Seguridad de Sincronización Solidaria"
FLOW_VERSION = "0.1.0"
DEMO_MODE = True

DEFAULT_SYNC_TTL_MINUTES = 5
MAX_ACCEPTED_SYNC_EVENTS_PER_PRIORITY_USER_TRIP = 1
MAX_ACCEPTED_SYNC_EVENTS_PER_COLLABORATOR_TRIP = 2


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
    GENERAL_USE = "general_use"
    LEGAL_PRIORITY = "legal_priority"


class SyncStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


class SyncStage(str, Enum):
    PRIORITY_SIGNAL_CREATED = "priority_signal_created"
    COLLABORATOR_SIGNAL_CREATED = "collaborator_signal_created"
    CONTEXT_MATCHED = "context_matched"
    USER_CONFIRMATION_RECEIVED = "user_confirmation_received"
    SECURITY_CHECKS_PASSED = "security_checks_passed"
    DEMO_SYNC_READY = "demo_sync_ready"


@dataclass(frozen=True)
class TransportSyncContext:
    """
    Contexto mínimo demostrativo.

    No contiene geolocalización real.
    No representa unidad real.
    No consulta sistemas externos.
    """

    country: str
    network_demo_id: str
    route_demo_id: str
    vehicle_demo_id: str
    trip_demo_id: str
    time_window_demo_id: str


@dataclass(frozen=True)
class PriorityUserSignal:
    """
    Señal técnica demostrativa del usuario SUBE Prioridad.

    No contiene identidad civil.
    No contiene diagnóstico.
    No contiene CUD.
    """

    priority_user_token: str
    priority_attribute_token: str
    previously_accredited_need: bool
    priority_user_confirms_sync: bool


@dataclass(frozen=True)
class CollaboratorSeatYieldSignal:
    """
    Señal demostrativa del pasajero colaborador.

    El colaborador no puede activar el reconocimiento por sí solo.
    """

    collaborator_token: str
    voluntary_seat_yield: bool
    collaborator_claims_reward: bool
    seat_type: SeatType


@dataclass(frozen=True)
class SyncWindow:
    issued_at_utc: datetime
    expires_at_utc: datetime


@dataclass(frozen=True)
class SolidarySyncRequest:
    """
    Solicitud conceptual de sincronización solidaria.

    No procesa datos sensibles.
    No produce efectos reales.
    """

    sync_event_demo_id: str
    priority_signal: PriorityUserSignal
    collaborator_signal: CollaboratorSeatYieldSignal
    actual_context: TransportSyncContext
    expected_context: TransportSyncContext
    sync_window: SyncWindow


@dataclass(frozen=True)
class SolidarySyncResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: SyncStatus
    accepted_demo_sync: bool
    solidary_point_demo: int
    stages_completed: List[SyncStage]
    risk_flags: List[str]
    reason: str
    priority_user_control: str
    collaborator_limit: str
    driver_burden: str
    privacy_notice: str
    warnings: List[str]
    timestamp_utc: str


@dataclass
class SyncSecurityLedger:
    """
    Ledger demostrativo en memoria.

    No es base de datos.
    No persiste datos reales.
    Sólo permite simular anti-replay y límites por viaje.
    """

    used_sync_event_ids: Set[str] = field(default_factory=set)
    accepted_by_priority_user_trip: Dict[str, int] = field(default_factory=dict)
    accepted_by_collaborator_trip: Dict[str, int] = field(default_factory=dict)

    def register_accepted_sync(self, request: SolidarySyncRequest) -> None:
        self.used_sync_event_ids.add(request.sync_event_demo_id)

        priority_key = _priority_user_trip_key(request)
        collaborator_key = _collaborator_trip_key(request)

        self.accepted_by_priority_user_trip[priority_key] = (
            self.accepted_by_priority_user_trip.get(priority_key, 0) + 1
        )
        self.accepted_by_collaborator_trip[collaborator_key] = (
            self.accepted_by_collaborator_trip.get(collaborator_key, 0) + 1
        )


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza datos personales, médicos o sensibles.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_transport_sync_context(
    country: str = "Argentina",
    network_demo_id: str = "demo-network-sube",
    route_demo_id: str = "demo-route-001",
    vehicle_demo_id: str = "demo-vehicle-001",
    trip_demo_id: str = "demo-trip-001",
    time_window_demo_id: str = "demo-window-001",
) -> TransportSyncContext:
    return TransportSyncContext(
        country=country,
        network_demo_id=network_demo_id,
        route_demo_id=route_demo_id,
        vehicle_demo_id=vehicle_demo_id,
        trip_demo_id=trip_demo_id,
        time_window_demo_id=time_window_demo_id,
    )


def create_demo_sync_request(
    sync_event_demo_id: str = "demo-sync-event-001",
    priority_user_token: str = "demo-priority-user-001",
    priority_attribute_token: str = "demo-priority-attribute-001",
    collaborator_token: str = "demo-collaborator-001",
    previously_accredited_need: bool = True,
    priority_user_confirms_sync: bool = True,
    voluntary_seat_yield: bool = True,
    collaborator_claims_reward: bool = False,
    seat_type: SeatType = SeatType.GENERAL_USE,
    actual_context: Optional[TransportSyncContext] = None,
    expected_context: Optional[TransportSyncContext] = None,
    issued_at_utc: Optional[datetime] = None,
    ttl_minutes: int = DEFAULT_SYNC_TTL_MINUTES,
) -> SolidarySyncRequest:
    """
    Crea una solicitud demostrativa de sincronización solidaria.
    """
    if not sync_event_demo_id or not sync_event_demo_id.strip():
        raise ValueError("El identificador demostrativo de sincronización no puede estar vacío.")

    if not priority_user_token or not priority_user_token.strip():
        raise ValueError("El token demostrativo del usuario SUBE Prioridad no puede estar vacío.")

    if not priority_attribute_token or not priority_attribute_token.strip():
        raise ValueError("El token demostrativo de prioridad no puede estar vacío.")

    if not collaborator_token or not collaborator_token.strip():
        raise ValueError("El token demostrativo del colaborador no puede estar vacío.")

    assert_no_prohibited_fields(
        {
            "sync_event_demo_id": sync_event_demo_id,
            "priority_user_token": priority_user_token,
            "priority_attribute_token": priority_attribute_token,
            "collaborator_token": collaborator_token,
        }
    )

    context = actual_context or create_demo_transport_sync_context()
    expected = expected_context or context

    issued_at = issued_at_utc or datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=ttl_minutes)

    return SolidarySyncRequest(
        sync_event_demo_id=sync_event_demo_id.strip(),
        priority_signal=PriorityUserSignal(
            priority_user_token=priority_user_token.strip(),
            priority_attribute_token=priority_attribute_token.strip(),
            previously_accredited_need=previously_accredited_need,
            priority_user_confirms_sync=priority_user_confirms_sync,
        ),
        collaborator_signal=CollaboratorSeatYieldSignal(
            collaborator_token=collaborator_token.strip(),
            voluntary_seat_yield=voluntary_seat_yield,
            collaborator_claims_reward=collaborator_claims_reward,
            seat_type=seat_type,
        ),
        actual_context=context,
        expected_context=expected,
        sync_window=SyncWindow(
            issued_at_utc=issued_at,
            expires_at_utc=expires_at,
        ),
    )


def simulate_solidary_sync_security(
    request: SolidarySyncRequest,
    ledger: Optional[SyncSecurityLedger] = None,
    now_utc: Optional[datetime] = None,
) -> SolidarySyncResult:
    """
    Simula el blindaje de sincronización entre usuario prioritario y colaborador.
    """
    assert_no_prohibited_fields(
        {
            "sync_event_demo_id": request.sync_event_demo_id,
            "priority_user_token": request.priority_signal.priority_user_token,
            "priority_attribute_token": request.priority_signal.priority_attribute_token,
            "collaborator_token": request.collaborator_signal.collaborator_token,
        }
    )

    ledger = ledger or SyncSecurityLedger()
    current_time = now_utc or datetime.now(timezone.utc)

    stages_completed: List[SyncStage] = [
        SyncStage.PRIORITY_SIGNAL_CREATED,
        SyncStage.COLLABORATOR_SIGNAL_CREATED,
    ]

    same_context = _same_context(request.actual_context, request.expected_context)

    if request.actual_context.country.strip().lower() != "argentina":
        return _rejected_result(
            reason="La sincronización solidaria demostrativa sólo aplica a transporte público de Argentina.",
            risk_flags=["outside_argentina_context"],
            stages_completed=stages_completed,
        )

    if _looks_like_free_text(request.priority_signal.priority_user_token):
        return _rejected_result(
            reason="El token del usuario SUBE Prioridad parece texto libre.",
            risk_flags=["priority_user_token_looks_like_free_text"],
            stages_completed=stages_completed,
        )

    if _looks_like_free_text(request.collaborator_signal.collaborator_token):
        return _rejected_result(
            reason="El token del colaborador parece texto libre.",
            risk_flags=["collaborator_token_looks_like_free_text"],
            stages_completed=stages_completed,
        )

    if (
        request.priority_signal.priority_user_token
        == request.collaborator_signal.collaborator_token
    ):
        return _rejected_result(
            reason="El usuario SUBE Prioridad y el colaborador no pueden ser el mismo token.",
            risk_flags=["self_sync_attempt"],
            stages_completed=stages_completed,
        )

    if request.sync_event_demo_id in ledger.used_sync_event_ids:
        return _rejected_result(
            reason="El evento de sincronización demostrativo ya fue utilizado.",
            risk_flags=["replay_sync_event_id"],
            stages_completed=stages_completed,
        )

    if current_time > request.sync_window.expires_at_utc:
        return _rejected_result(
            reason="La ventana temporal de sincronización demostrativa expiró.",
            risk_flags=["expired_sync_window"],
            stages_completed=stages_completed,
        )

    if not request.priority_signal.previously_accredited_need:
        return _rejected_result(
            reason="No existe necesidad previamente acreditada en la señal demostrativa.",
            risk_flags=["need_not_previously_accredited"],
            stages_completed=stages_completed,
        )

    if not request.collaborator_signal.voluntary_seat_yield:
        return _rejected_result(
            reason="No se registra cesión voluntaria de asiento.",
            risk_flags=["no_voluntary_seat_yield"],
            stages_completed=stages_completed,
        )

    if request.collaborator_signal.seat_type != SeatType.GENERAL_USE:
        return _rejected_result(
            reason="La sincronización solidaria no aplica a asientos prioritarios legales.",
            risk_flags=["legal_priority_seat_not_eligible"],
            stages_completed=stages_completed,
        )

    if request.collaborator_signal.collaborator_claims_reward:
        return _rejected_result(
            reason=(
                "El colaborador no puede reclamar reconocimiento por sí solo. "
                "La confirmación queda en manos del usuario SUBE Prioridad."
            ),
            risk_flags=["collaborator_unilateral_claim"],
            stages_completed=stages_completed,
        )

    if not request.priority_signal.priority_user_confirms_sync:
        return _rejected_result(
            reason=(
                "El usuario SUBE Prioridad no confirmó la sincronización. "
                "Sin confirmación voluntaria no hay reconocimiento."
            ),
            risk_flags=["priority_user_confirmation_required"],
            stages_completed=stages_completed,
        )

    stages_completed.append(SyncStage.USER_CONFIRMATION_RECEIVED)

    if not same_context:
        return _rejected_result(
            reason="No coincide el contexto demostrativo de transporte.",
            risk_flags=["different_transport_context"],
            stages_completed=stages_completed,
        )

    stages_completed.append(SyncStage.CONTEXT_MATCHED)

    priority_count = ledger.accepted_by_priority_user_trip.get(
        _priority_user_trip_key(request),
        0,
    )

    collaborator_count = ledger.accepted_by_collaborator_trip.get(
        _collaborator_trip_key(request),
        0,
    )

    if priority_count >= MAX_ACCEPTED_SYNC_EVENTS_PER_PRIORITY_USER_TRIP:
        return _needs_review_result(
            reason="El usuario SUBE Prioridad ya confirmó una sincronización en este viaje demostrativo.",
            risk_flags=["priority_user_trip_sync_limit_exceeded"],
            stages_completed=stages_completed,
        )

    if collaborator_count >= MAX_ACCEPTED_SYNC_EVENTS_PER_COLLABORATOR_TRIP:
        return _needs_review_result(
            reason="El colaborador acumula múltiples sincronizaciones en el mismo viaje demostrativo.",
            risk_flags=["collaborator_trip_sync_limit_exceeded"],
            stages_completed=stages_completed,
        )

    stages_completed.append(SyncStage.SECURITY_CHECKS_PASSED)
    stages_completed.append(SyncStage.DEMO_SYNC_READY)

    ledger.register_accepted_sync(request)

    return SolidarySyncResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=SyncStatus.ACCEPTED,
        accepted_demo_sync=True,
        solidary_point_demo=1,
        stages_completed=stages_completed,
        risk_flags=[],
        reason=(
            "Sincronización solidaria demostrativa aceptada. "
            "La confirmación fue realizada por el usuario SUBE Prioridad, "
            "sobre un asiento de uso general, dentro de un contexto coherente."
        ),
        priority_user_control=(
            "El usuario SUBE Prioridad conserva el control de la confirmación."
        ),
        collaborator_limit=(
            "El colaborador no puede reclamar reconocimiento unilateralmente."
        ),
        driver_burden=_driver_burden_notice(),
        privacy_notice=_privacy_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: SolidarySyncResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "accepted_demo_sync": result.accepted_demo_sync,
        "solidary_point_demo": result.solidary_point_demo,
        "stages_completed": [stage.value for stage in result.stages_completed],
        "risk_flags": result.risk_flags,
        "reason": result.reason,
        "priority_user_control": result.priority_user_control,
        "collaborator_limit": result.collaborator_limit,
        "driver_burden": result.driver_burden,
        "privacy_notice": result.privacy_notice,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    ledger = SyncSecurityLedger()
    request = create_demo_sync_request()

    result = simulate_solidary_sync_security(
        request=request,
        ledger=ledger,
    )

    return result_to_dict(result)


def _same_context(
    actual: TransportSyncContext,
    expected: TransportSyncContext,
) -> bool:
    return (
        actual.country == expected.country
        and actual.network_demo_id == expected.network_demo_id
        and actual.route_demo_id == expected.route_demo_id
        and actual.vehicle_demo_id == expected.vehicle_demo_id
        and actual.trip_demo_id == expected.trip_demo_id
        and actual.time_window_demo_id == expected.time_window_demo_id
    )


def _priority_user_trip_key(request: SolidarySyncRequest) -> str:
    return "|".join(
        [
            request.priority_signal.priority_user_token,
            request.actual_context.network_demo_id,
            request.actual_context.route_demo_id,
            request.actual_context.vehicle_demo_id,
            request.actual_context.trip_demo_id,
            request.actual_context.time_window_demo_id,
        ]
    )


def _collaborator_trip_key(request: SolidarySyncRequest) -> str:
    return "|".join(
        [
            request.collaborator_signal.collaborator_token,
            request.actual_context.network_demo_id,
            request.actual_context.route_demo_id,
            request.actual_context.vehicle_demo_id,
            request.actual_context.trip_demo_id,
            request.actual_context.time_window_demo_id,
        ]
    )


def _looks_like_free_text(token: str) -> bool:
    normalized = token.lower().strip()

    suspicious_terms = {
        "quiero",
        "gratis",
        "beneficio",
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
        "premio",
        "puntos",
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _rejected_result(
    reason: str,
    risk_flags: List[str],
    stages_completed: List[SyncStage],
) -> SolidarySyncResult:
    return SolidarySyncResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=SyncStatus.REJECTED,
        accepted_demo_sync=False,
        solidary_point_demo=0,
        stages_completed=stages_completed,
        risk_flags=risk_flags,
        reason=reason,
        priority_user_control=(
            "Sin confirmación del usuario SUBE Prioridad no hay sincronización aceptada."
        ),
        collaborator_limit=(
            "El colaborador no puede activar reconocimiento por sí solo."
        ),
        driver_burden=_driver_burden_notice(),
        privacy_notice=_privacy_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def _needs_review_result(
    reason: str,
    risk_flags: List[str],
    stages_completed: List[SyncStage],
) -> SolidarySyncResult:
    return SolidarySyncResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=SyncStatus.NEEDS_REVIEW,
        accepted_demo_sync=False,
        solidary_point_demo=0,
        stages_completed=stages_completed,
        risk_flags=risk_flags,
        reason=reason,
        priority_user_control=(
            "La confirmación del usuario existe, pero el patrón requiere revisión demostrativa."
        ),
        collaborator_limit=(
            "No se sanciona ni se rankea al colaborador; sólo se marca revisión conceptual."
        ),
        driver_burden=_driver_burden_notice(),
        privacy_notice=_privacy_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def _privacy_notice() -> str:
    return (
        "La sincronización no revela DNI, nombre, domicilio, diagnóstico, CUD, "
        "historia clínica ni certificado médico."
    )


def _driver_burden_notice() -> str:
    return (
        "El personal de conducción no verifica, no decide, no media y no administra "
        "la sincronización solidaria."
    )


def _common_warnings() -> List[str]:
    return [
        "Flujo conceptual y demostrativo.",
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
        "Sin vigilancia.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "El usuario SUBE Prioridad conserva el control de la confirmación.",
        "El colaborador no puede reclamar reconocimiento unilateralmente.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))

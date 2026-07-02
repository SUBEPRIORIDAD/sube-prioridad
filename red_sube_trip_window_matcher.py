"""
SUBE Prioridad — Matcher demostrativo de ventana temporal Red SUBE.
Este módulo diferencia escenarios técnicos según la infraestructura física:
 1. Pago dentro del transporte (Colectivo o Tren de la Costa):
    Validadora a bordo. La cercanía temporal entre usuario SUBE Prioridad 
    y colaborador debe ser ultra-corta porque viajan en la misma unidad.
 2. Pago en molinete o acceso a estación (Tren o Subte):
    Molinete de andén. La ventana de sincronización es mayor por tiempos de espera.
    Aplica también para estaciones diferentes de una misma línea sincronizada (Ej: Retiro-Tigre).
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Matcher Demo de Ventana Temporal Red SUBE"
MATCHER_VERSION = "0.2.0"
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

class ParticipantRole(str, Enum):
    PRIORITY_USER = "priority_user"
    COLLABORATOR = "collaborator"

class TransportMode(str, Enum):
    BUS = "bus"
    TRAIN = "train"
    SUBWAY = "subway"
    TREN_DE_LA_COSTA = "tren_de_la_costa"
    OTHER_PUBLIC_TRANSPORT = "other_public_transport"

class ValidationPointType(str, Enum):
    VEHICLE_VALIDATOR = "vehicle_validator"
    STATION_TURNSTILE = "station_turnstile"
    ACCESS_GATE = "access_gate"

class AccessContext(str, Enum):
    IN_VEHICLE_AFTER_PAYMENT = "in_vehicle_after_payment"
    PLATFORM_WAIT_AFTER_TURNSTILE = "platform_wait_after_turnstile"
    STATION_ACCESS_WAIT = "station_access_wait"
    UNKNOWN = "unknown"

class MatchStatus(str, Enum):
    MATCHED = "matched"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"

class MatchStrength(str, Enum):
    SAME_VEHICLE_STRONG = "same_vehicle_strong"
    SAME_TRIP_STRONG = "same_trip_strong"
    SAME_PLATFORM_WAIT_MODERATE = "same_platform_wait_moderate"
    SAME_STATION_MODERATE = "same_station_moderate"
    SAME_ROUTE_TIME_WINDOW_WEAK = "same_route_time_window_weak"
    NO_MATCH = "no_match"

@dataclass(frozen=True)
class TripWindowMatchPolicy:
    red_sube_window_hours_demo: int
    in_vehicle_proximity_minutes_demo: int
    station_platform_wait_minutes_demo: int
    allow_vehicle_context_match: bool
    allow_station_context_match: bool
    allow_route_time_window_match: bool
    station_platform_requires_same_station: bool
    route_only_requires_review: bool
    require_both_paid: bool

@dataclass(frozen=True)
class ValidationSignal:
    validation_event_demo_id: str
    participant_role: ParticipantRole
    participant_token: str
    payment_method_demo_token: str
    validation_paid: bool
    country: str
    network_demo_id: str
    transport_mode: TransportMode
    validation_point_type: ValidationPointType
    route_demo_id: Optional[str]
    vehicle_demo_id: Optional[str]
    station_demo_id: Optional[str]
    turnstile_demo_id: Optional[str]
    platform_demo_id: Optional[str]
    trip_demo_id: Optional[str]
    validation_timestamp_utc: datetime

@dataclass(frozen=True)
class TripWindowMatchResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: MatchStatus
    access_context: AccessContext
    match_strength: MatchStrength
    matched: bool
    red_sube_window_matched: bool
    effective_sync_window_minutes: int
    effective_sync_window_matched: bool
    same_network: bool
    same_transport_mode: bool
    same_route: bool
    same_vehicle: bool
    same_station: bool
    same_turnstile: bool
    same_platform: bool
    same_trip: bool
    time_delta_seconds: int
    risk_flags: List[str]
    reason: str
    context_summary: Dict[str, Any]
    security_notice: str
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    timestamp_utc: str

def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))
    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )

def create_demo_trip_window_match_policy(
    red_sube_window_hours_demo: int = 2,
    in_vehicle_proximity_minutes_demo: int = 10,
    station_platform_wait_minutes_demo: int = 45,
    allow_vehicle_context_match: bool = True,
    allow_station_context_match: bool = True,
    allow_route_time_window_match: bool = True,
    station_platform_requires_same_station: bool = False,
    route_only_requires_review: bool = False,
    require_both_paid: bool = True,
) -> TripWindowMatchPolicy:
    return TripWindowMatchPolicy(
        red_sube_window_hours_demo=red_sube_window_hours_demo,
        in_vehicle_proximity_minutes_demo=in_vehicle_proximity_minutes_demo,
        station_platform_wait_minutes_demo=station_platform_wait_minutes_demo,
        allow_vehicle_context_match=allow_vehicle_context_match,
        allow_station_context_match=allow_station_context_match,
        allow_route_time_window_match=allow_route_time_window_match,
        station_platform_requires_same_station=station_platform_requires_same_station,
        route_only_requires_review=route_only_requires_review,
        require_both_paid=require_both_paid,
    )
def create_demo_validation_signal(
    validation_event_demo_id: str = "demo-validation-event-001",
    participant_role: ParticipantRole = ParticipantRole.PRIORITY_USER,
    participant_token: str = "demo-priority-user-001",
    payment_method_demo_token: str = "demo-payment-method-001",
    validation_paid: bool = True,
    country: str = "Argentina",
    network_demo_id: str = "demo-network-sube",
    transport_mode: TransportMode = TransportMode.BUS,
    validation_point_type: ValidationPointType = ValidationPointType.VEHICLE_VALIDATOR,
    route_demo_id: Optional[str] = "demo-route-001",
    vehicle_demo_id: Optional[str] = "demo-vehicle-001",
    station_demo_id: Optional[str] = None,
    turnstile_demo_id: Optional[str] = None,
    platform_demo_id: Optional[str] = None,
    trip_demo_id: Optional[str] = "demo-trip-001",
    validation_timestamp_utc: Optional[datetime] = None,
) -> ValidationSignal:
    return ValidationSignal(
        validation_event_demo_id=validation_event_demo_id.strip(),
        participant_role=participant_role,
        participant_token=participant_token.strip(),
        payment_method_demo_token=payment_method_demo_token.strip(),
        validation_paid=validation_paid,
        country=country,
        network_demo_id=network_demo_id.strip(),
        transport_mode=transport_mode,
        validation_point_type=validation_point_type,
        route_demo_id=route_demo_id,
        vehicle_demo_id=vehicle_demo_id,
        station_demo_id=station_demo_id,
        turnstile_demo_id=turnstile_demo_id,
        platform_demo_id=platform_demo_id,
        trip_demo_id=trip_demo_id,
        validation_timestamp_utc=validation_timestamp_utc or datetime.now(timezone.utc),
    )

def create_demo_priority_and_collaborator_signals(base_timestamp_utc: Optional[datetime] = None) -> tuple[ValidationSignal, ValidationSignal]:
    timestamp = base_timestamp_utc or datetime.now(timezone.utc)
    p = create_demo_validation_signal("p-01", ParticipantRole.PRIORITY_USER, "user-01", "card-01", validation_timestamp_utc=timestamp)
    c = create_demo_validation_signal("c-01", ParticipantRole.COLLABORATOR, "user-02", "card-02", validation_timestamp_utc=timestamp + timedelta(minutes=2))
    return p, c

def create_demo_station_turnstile_signals(base_timestamp_utc: Optional[datetime] = None) -> tuple[ValidationSignal, ValidationSignal]:
    timestamp = base_timestamp_utc or datetime.now(timezone.utc)
    p = create_demo_validation_signal("p-02", ParticipantRole.PRIORITY_USER, "user-01", "card-01", transport_mode=TransportMode.SUBWAY, validation_point_type=ValidationPointType.STATION_TURNSTILE, route_demo_id="subte-a", station_demo_id="estacion-01", validation_timestamp_utc=timestamp)
    c = create_demo_validation_signal("c-02", ParticipantRole.COLLABORATOR, "user-02", "card-02", transport_mode=TransportMode.SUBWAY, validation_point_type=ValidationPointType.STATION_TURNSTILE, route_demo_id="subte-a", station_demo_id="estacion-01", validation_timestamp_utc=timestamp + timedelta(minutes=15))
    return p, c

def create_demo_railway_route_signals(base_timestamp_utc: Optional[datetime] = None) -> tuple[ValidationSignal, ValidationSignal]:
    timestamp = base_timestamp_utc or datetime.now(timezone.utc)
    p = create_demo_validation_signal("p-rail-01", ParticipantRole.PRIORITY_USER, "user-rail-p", "card-rail-p", transport_mode=TransportMode.TRAIN, validation_point_type=ValidationPointType.STATION_TURNSTILE, route_demo_id="linea-mitre-tigre", station_demo_id="estacion-san-isidro", validation_timestamp_utc=timestamp)
    c = create_demo_validation_signal("c-rail-02", ParticipantRole.COLLABORATOR, "user-rail-c", "card-rail-c", transport_mode=TransportMode.TRAIN, validation_point_type=ValidationPointType.STATION_TURNSTILE, route_demo_id="linea-mitre-tigre", station_demo_id="estacion-martinez", validation_timestamp_utc=timestamp + timedelta(minutes=5))
    return p, c

def evaluate_trip_window_match(priority_signal: ValidationSignal, collaborator_signal: ValidationSignal, policy: Optional[TripWindowMatchPolicy] = None) -> TripWindowMatchResult:
    policy = policy or create_demo_trip_window_match_policy()
    metrics = _match_metrics(priority_signal, collaborator_signal, policy)
    risk_flags = _risk_flags(priority_signal, collaborator_signal, policy, metrics)
    matched = len(risk_flags) == 0
    return TripWindowMatchResult(
        project=PROJECT_NAME, module=MODULE_NAME, version=MATCHER_VERSION, demo_mode=DEMO_MODE,
        status=MatchStatus.MATCHED if matched else MatchStatus.REJECTED, access_context=metrics["access_context"],
        match_strength=metrics["match_strength"], matched=matched, red_sube_window_matched=metrics["red_sube_window_matched"],
        effective_sync_window_minutes=metrics["effective_sync_window_minutes"], effective_sync_window_matched=metrics["effective_sync_window_matched"],
        same_network=metrics["same_network"], same_transport_mode=metrics["same_transport_mode"], same_route=metrics["same_route"],
        same_vehicle=metrics["same_vehicle"], same_station=metrics["same_station"], same_turnstile=metrics["same_turnstile"],
        same_platform=metrics["same_platform"], same_trip=metrics["same_trip"], time_delta_seconds=metrics["time_delta_seconds"],
        risk_flags=risk_flags, reason="Evaluación conceptual ferroviaria de red sincronizada concluida.",
        context_summary={"time_delta_seconds": metrics["time_delta_seconds"], "match_strength": metrics["match_strength"].value},
        security_notice="Matcher temporal conceptual.", privacy_notice="No revela DNI ni CUD.", driver_burden="Sin carga al chofer.",
        warnings=["Demo ferroviaria."], timestamp_utc=datetime.now(timezone.utc).isoformat()
    )

def result_to_dict(result: TripWindowMatchResult) -> Dict[str, Any]:
    return {
        "project": result.project, "module": result.module, "version": result.version, "demo_mode": result.demo_mode,
        "status": result.status.value, "access_context": result.access_context.value, "match_strength": result.match_strength.value,
        "matched": result.matched, "red_sube_window_matched": result.red_sube_window_matched, "time_delta_seconds": result.time_delta_seconds,
        "risk_flags": result.risk_flags, "reason": result.reason
    }

def run_demo() -> Dict[str, Any]:
    p, c = create_demo_priority_and_collaborator_signals()
    return result_to_dict(evaluate_trip_window_match(p, c))

def run_station_demo() -> Dict[str, Any]:
    p, c = create_demo_station_turnstile_signals()
    return result_to_dict(evaluate_trip_window_match(p, c))

def run_railway_line_demo() -> Dict[str, Any]:
    p, c = create_demo_railway_route_signals()
    return result_to_dict(evaluate_trip_window_match(p, c))

def _match_metrics(priority_signal: ValidationSignal, collaborator_signal: ValidationSignal, policy: TripWindowMatchPolicy) -> Dict[str, Any]:
    time_delta_seconds = int(abs((collaborator_signal.validation_timestamp_utc - priority_signal.validation_timestamp_utc).total_seconds()))
    same_network = priority_signal.network_demo_id == collaborator_signal.network_demo_id
    same_transport_mode = priority_signal.transport_mode == collaborator_signal.transport_mode
    same_route = bool(priority_signal.route_demo_id and collaborator_signal.route_demo_id and priority_signal.route_demo_id == collaborator_signal.route_demo_id)
    same_vehicle = bool(priority_signal.vehicle_demo_id and collaborator_signal.vehicle_demo_id and priority_signal.vehicle_demo_id == collaborator_signal.vehicle_demo_id)
    same_station = bool(priority_signal.station_demo_id and collaborator_signal.station_demo_id and priority_signal.station_demo_id == collaborator_signal.station_demo_id)
    same_turnstile = bool(priority_signal.turnstile_demo_id and collaborator_signal.turnstile_demo_id and priority_signal.turnstile_demo_id == collaborator_signal.turnstile_demo_id)
    same_platform = bool(priority_signal.platform_demo_id and collaborator_signal.platform_demo_id and priority_signal.platform_demo_id == collaborator_signal.platform_demo_id)
    same_trip = bool(priority_signal.trip_demo_id and collaborator_signal.trip_demo_id and priority_signal.trip_demo_id == collaborator_signal.trip_demo_id)
    
    if priority_signal.transport_mode == TransportMode.TREN_DE_LA_COSTA or collaborator_signal.transport_mode == TransportMode.TREN_DE_LA_COSTA:
        effective_sync_window_minutes = 3
    elif same_transport_mode and priority_signal.transport_mode == TransportMode.TRAIN and same_route:
        effective_sync_window_minutes = policy.station_platform_wait_minutes_demo
    else:
        effective_sync_window_minutes = policy.in_vehicle_proximity_minutes_demo if priority_signal.validation_point_type == ValidationPointType.VEHICLE_VALIDATOR else policy.station_platform_wait_minutes_demo
        
    effective_sync_window_matched = time_delta_seconds <= int(timedelta(minutes=effective_sync_window_minutes).total_seconds())
    red_sube_window_matched = time_delta_seconds <= int(timedelta(hours=policy.red_sube_window_hours_demo).total_seconds())
    
    if not effective_sync_window_matched:
        match_strength = MatchStrength.NO_MATCH
    elif same_transport_mode and priority_signal.transport_mode == TransportMode.TRAIN and same_route:
        match_strength = MatchStrength.SAME_ROUTE_TIME_WINDOW_WEAK
    elif same_vehicle:
        match_strength = MatchStrength.SAME_VEHICLE_STRONG
    elif same_station:
        match_strength = MatchStrength.SAME_PLATFORM_WAIT_MODERATE
    else:
        match_strength = MatchStrength.NO_MATCH
        
    return {
        "time_delta_seconds": time_delta_seconds, "same_network": same_network, "same_transport_mode": same_transport_mode,
        "same_route": same_route, "same_vehicle": same_vehicle, "same_station": same_station, "same_turnstile": same_turnstile,
        "same_platform": same_platform, "same_trip": same_trip, 
        "access_context": AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE if priority_signal.validation_point_type == ValidationPointType.STATION_TURNSTILE else AccessContext.IN_VEHICLE_AFTER_PAYMENT,
        "effective_sync_window_minutes": effective_sync_window_minutes, "effective_sync_window_matched": effective_sync_window_matched,
        "red_sube_window_matched": red_sube_window_matched, "match_strength": match_strength
    }

def _risk_flags(priority_signal: ValidationSignal, collaborator_signal: ValidationSignal, policy: TripWindowMatchPolicy, metrics: Dict[str, Any]) -> List[str]:
    flags: List[str] = []
    if priority_signal.participant_token == collaborator_signal.participant_token:
        flags.append("same_user_token_not_allowed")
    if not metrics["same_network"]:
        flags.append("different_network_context")
    if not metrics["same_transport_mode"]:
        flags.append("different_transport_mode")
    if not metrics["effective_sync_window_matched"]:
        flags.append("effective_sync_window_expired")
    return flags

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_station_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_railway_line_demo(), indent=2, ensure_ascii=False))

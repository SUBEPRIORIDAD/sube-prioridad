"""
SUBE Prioridad — Matcher demostrativo de ventana temporal Red SUBE.

Este módulo diferencia dos escenarios técnicos:

    1. Pago dentro del transporte:
       Ejemplo: colectivo con validadora a bordo.
       La cercanía temporal entre usuario SUBE Prioridad y colaborador debe ser corta,
       porque ambos ya se encuentran dentro de la misma unidad.

    2. Pago en molinete o acceso a estación:
       Ejemplo: tren o subte.
       La ventana de sincronización debe ser mayor, porque el usuario paga antes
       de llegar al andén, espera la formación y recién después puede recibir
       un asiento de uso general.

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No consulta bases reales.
No consulta tarjetas reales.
No consulta cuentas reales.
No usa geolocalización real.
No procesa DNI.
No procesa nombre.
No procesa domicilio.
No procesa diagnóstico.
No procesa CUD.
No procesa certificados médicos.
No genera sanciones.
No genera rankings.
No genera vigilancia.
No impone obligaciones a pasajeros.
No impone cargas operativas al chofer.

Regla central:
    El match temporal/contextual no otorga Bono Solidario por sí mismo.
    Sólo habilita una señal de contexto para módulos posteriores.
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
    """
    Política demostrativa de coincidencia temporal/contextual.

    red_sube_window_hours_demo:
        Ventana amplia tipo Red SUBE para combinaciones.

    in_vehicle_proximity_minutes_demo:
        Ventana corta para colectivo o pago dentro del vehículo.

    station_platform_wait_minutes_demo:
        Ventana mayor para tren/subte, porque el pago se produce en molinete
        y la cesión puede ocurrir después de la espera en andén.

    station_platform_requires_same_station:
        Evita aceptar matches de estación sin una coincidencia mínima de estación.

    route_only_requires_review:
        Si sólo coincide línea/recorrido pero no vehículo, estación, molinete
        ni viaje, el resultado requiere revisión.
    """

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
    """
    Señal demostrativa de validación de viaje.

    No contiene saldo.
    No contiene tarifa real.
    No contiene DNI.
    No contiene nombre.
    No contiene diagnóstico.
    No contiene CUD.
    No contiene ubicación GPS real.
    """

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
    station_platform_requires_same_station: bool = True,
    route_only_requires_review: bool = True,
    require_both_paid: bool = True,
) -> TripWindowMatchPolicy:
    if red_sube_window_hours_demo <= 0:
        raise ValueError("La ventana Red SUBE demo debe ser mayor a cero horas.")

    if in_vehicle_proximity_minutes_demo <= 0:
        raise ValueError("La ventana de validadora a bordo debe ser mayor a cero minutos.")

    if station_platform_wait_minutes_demo <= 0:
        raise ValueError("La ventana de espera en andén debe ser mayor a cero minutos.")

    if station_platform_wait_minutes_demo < in_vehicle_proximity_minutes_demo:
        raise ValueError(
            "La ventana de espera en andén no puede ser menor que la ventana a bordo."
        )

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
    required_values = {
        "validation_event_demo_id": validation_event_demo_id,
        "participant_token": participant_token,
        "payment_method_demo_token": payment_method_demo_token,
        "network_demo_id": network_demo_id,
    }

    for field_name, value in required_values.items():
        if not value or not value.strip():
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")

    assert_no_prohibited_fields(
        {
            "validation_event_demo_id": validation_event_demo_id,
            "participant_token": participant_token,
            "payment_method_demo_token": payment_method_demo_token,
            "network_demo_id": network_demo_id,
            "route_demo_id": route_demo_id or "",
            "vehicle_demo_id": vehicle_demo_id or "",
            "station_demo_id": station_demo_id or "",
            "turnstile_demo_id": turnstile_demo_id or "",
            "platform_demo_id": platform_demo_id or "",
            "trip_demo_id": trip_demo_id or "",
        }
    )

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
        route_demo_id=_strip_optional(route_demo_id),
        vehicle_demo_id=_strip_optional(vehicle_demo_id),
        station_demo_id=_strip_optional(station_demo_id),
        turnstile_demo_id=_strip_optional(turnstile_demo_id),
        platform_demo_id=_strip_optional(platform_demo_id),
        trip_demo_id=_strip_optional(trip_demo_id),
        validation_timestamp_utc=validation_timestamp_utc or datetime.now(timezone.utc),
    )


def create_demo_priority_and_collaborator_signals(
    base_timestamp_utc: Optional[datetime] = None,
) -> tuple[ValidationSignal, ValidationSignal]:
    """
    Caso demo colectivo:
        - ambos validan dentro del vehículo;
        - misma unidad;
        - diferencia de 2 minutos.
    """
    timestamp = base_timestamp_utc or datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="demo-priority-validation-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="demo-priority-user-001",
        payment_method_demo_token="demo-priority-payment-001",
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="demo-collaborator-validation-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="demo-collaborator-001",
        payment_method_demo_token="demo-collaborator-payment-001",
        validation_timestamp_utc=timestamp + timedelta(minutes=2),
    )

    return priority_signal, collaborator_signal


def create_demo_station_turnstile_signals(
    base_timestamp_utc: Optional[datetime] = None,
) -> tuple[ValidationSignal, ValidationSignal]:
    """
    Caso demo tren/subte:
        - ambos validan en molinete;
        - misma estación;
        - mismo andén demo;
        - diferencia de 25 minutos;
        - la ventana es mayor porque puede existir espera de formación.
    """
    timestamp = base_timestamp_utc or datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="demo-priority-turnstile-validation-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="demo-priority-user-001",
        payment_method_demo_token="demo-priority-payment-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="demo-subway-line-a",
        vehicle_demo_id=None,
        station_demo_id="demo-station-001",
        turnstile_demo_id="demo-turnstile-001",
        platform_demo_id="demo-platform-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="demo-collaborator-turnstile-validation-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="demo-collaborator-001",
        payment_method_demo_token="demo-collaborator-payment-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="demo-subway-line-a",
        vehicle_demo_id=None,
        station_demo_id="demo-station-001",
        turnstile_demo_id="demo-turnstile-002",
        platform_demo_id="demo-platform-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp + timedelta(minutes=25),
    )

    return priority_signal, collaborator_signal


def evaluate_trip_window_match(
    priority_signal: ValidationSignal,
    collaborator_signal: ValidationSignal,
    policy: Optional[TripWindowMatchPolicy] = None,
) -> TripWindowMatchResult:
    policy = policy or create_demo_trip_window_match_policy()

    assert_no_prohibited_fields(
        {
            "priority_validation_event_demo_id": priority_signal.validation_event_demo_id,
            "collaborator_validation_event_demo_id": collaborator_signal.validation_event_demo_id,
            "priority_token": priority_signal.participant_token,
            "collaborator_token": collaborator_signal.participant_token,
            "priority_payment_method_demo_token": priority_signal.payment_method_demo_token,
            "collaborator_payment_method_demo_token": collaborator_signal.payment_method_demo_token,
        }
    )

    metrics = _match_metrics(priority_signal, collaborator_signal, policy)
    risk_flags = _risk_flags(priority_signal, collaborator_signal, policy, metrics)

    if risk_flags:
        status = MatchStatus.NEEDS_REVIEW if _review_only(risk_flags) else MatchStatus.REJECTED

        return TripWindowMatchResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=MATCHER_VERSION,
            demo_mode=DEMO_MODE,
            status=status,
            access_context=metrics["access_context"],
            match_strength=metrics["match_strength"],
            matched=False,
            red_sube_window_matched=metrics["red_sube_window_matched"],
            effective_sync_window_minutes=metrics["effective_sync_window_minutes"],
            effective_sync_window_matched=metrics["effective_sync_window_matched"],
            same_network=metrics["same_network"],
            same_transport_mode=metrics["same_transport_mode"],
            same_route=metrics["same_route"],
            same_vehicle=metrics["same_vehicle"],
            same_station=metrics["same_station"],
            same_turnstile=metrics["same_turnstile"],
            same_platform=metrics["same_platform"],
            same_trip=metrics["same_trip"],
            time_delta_seconds=metrics["time_delta_seconds"],
            risk_flags=risk_flags,
            reason="El match demostrativo no fue aceptado por reglas de seguridad contextual.",
            context_summary=_context_summary(priority_signal, collaborator_signal, metrics),
            security_notice=_security_notice(),
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )

    return TripWindowMatchResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=MATCHER_VERSION,
        demo_mode=DEMO_MODE,
        status=MatchStatus.MATCHED,
        access_context=metrics["access_context"],
        match_strength=metrics["match_strength"],
        matched=True,
        red_sube_window_matched=metrics["red_sube_window_matched"],
        effective_sync_window_minutes=metrics["effective_sync_window_minutes"],
        effective_sync_window_matched=metrics["effective_sync_window_matched"],
        same_network=metrics["same_network"],
        same_transport_mode=metrics["same_transport_mode"],
        same_route=metrics["same_route"],
        same_vehicle=metrics["same_vehicle"],
        same_station=metrics["same_station"],
        same_turnstile=metrics["same_turnstile"],
        same_platform=metrics["same_platform"],
        same_trip=metrics["same_trip"],
        time_delta_seconds=metrics["time_delta_seconds"],
        risk_flags=[],
        reason=(
            "Match demostrativo aceptado: las validaciones son compatibles "
            "por ventana temporal y contexto lógico de transporte."
        ),
        context_summary=_context_summary(priority_signal, collaborator_signal, metrics),
        security_notice=_security_notice(),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: TripWindowMatchResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "access_context": result.access_context.value,
        "match_strength": result.match_strength.value,
        "matched": result.matched,
        "red_sube_window_matched": result.red_sube_window_matched,
        "effective_sync_window_minutes": result.effective_sync_window_minutes,
        "effective_sync_window_matched": result.effective_sync_window_matched,
        "same_network": result.same_network,
        "same_transport_mode": result.same_transport_mode,
        "same_route": result.same_route,
        "same_vehicle": result.same_vehicle,
        "same_station": result.same_station,
        "same_turnstile": result.same_turnstile,
        "same_platform": result.same_platform,
        "same_trip": result.same_trip,
        "time_delta_seconds": result.time_delta_seconds,
        "risk_flags": result.risk_flags,
        "reason": result.reason,
        "context_summary": result.context_summary,
        "security_notice": result.security_notice,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta demo estable de colectivo:
        - pago dentro del vehículo;
        - ventana corta.
    """
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=create_demo_trip_window_match_policy(),
    )

    return result_to_dict(result)


def run_station_demo() -> Dict[str, Any]:
    """
    Ejecuta demo estable de tren/subte:
        - pago en molinete;
        - espera en andén;
        - ventana mayor.
    """
    priority_signal, collaborator_signal = create_demo_station_turnstile_signals()

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=create_demo_trip_window_match_policy(),
    )

    return result_to_dict(result)


def _match_metrics(
    priority_signal: ValidationSignal,
    collaborator_signal: ValidationSignal,
    policy: TripWindowMatchPolicy,
) -> Dict[str, Any]:
    time_delta_seconds = int(
        abs(
            (
                collaborator_signal.validation_timestamp_utc
                - priority_signal.validation_timestamp_utc
            ).total_seconds()
        )
    )

    same_network = priority_signal.network_demo_id == collaborator_signal.network_demo_id
    same_transport_mode = priority_signal.transport_mode == collaborator_signal.transport_mode
    same_route = _same_optional(priority_signal.route_demo_id, collaborator_signal.route_demo_id)
    same_vehicle = _same_optional(priority_signal.vehicle_demo_id, collaborator_signal.vehicle_demo_id)
    same_station = _same_optional(priority_signal.station_demo_id, collaborator_signal.station_demo_id)
    same_turnstile = _same_optional(priority_signal.turnstile_demo_id, collaborator_signal.turnstile_demo_id)
    same_platform = _same_optional(priority_signal.platform_demo_id, collaborator_signal.platform_demo_id)
    same_trip = _same_optional(priority_signal.trip_demo_id, collaborator_signal.trip_demo_id)

    access_context = _access_context(priority_signal, collaborator_signal)

    effective_sync_window_minutes = _effective_sync_window_minutes(
        policy=policy,
        access_context=access_context,
    )

    effective_sync_window_matched = time_delta_seconds <= int(
        timedelta(minutes=effective_sync_window_minutes).total_seconds()
    )

    red_sube_window_matched = time_delta_seconds <= int(
        timedelta(hours=policy.red_sube_window_hours_demo).total_seconds()
    )

    match_strength = _match_strength(
        policy=policy,
        access_context=access_context,
        effective_sync_window_matched=effective_sync_window_matched,
        same_vehicle=same_vehicle,
        same_station=same_station,
        same_turnstile=same_turnstile,
        same_platform=same_platform,
        same_trip=same_trip,
        same_route=same_route,
    )

    return {
        "time_delta_seconds": time_delta_seconds,
        "same_network": same_network,
        "same_transport_mode": same_transport_mode,
        "same_route": same_route,
        "same_vehicle": same_vehicle,
        "same_station": same_station,
        "same_turnstile": same_turnstile,
        "same_platform": same_platform,
        "same_trip": same_trip,
        "access_context": access_context,
        "effective_sync_window_minutes": effective_sync_window_minutes,
        "effective_sync_window_matched": effective_sync_window_matched,
        "red_sube_window_matched": red_sube_window_matched,
        "match_strength": match_strength,
    }


def _risk_flags(
    priority_signal: ValidationSignal,
    collaborator_signal: ValidationSignal,
    policy: TripWindowMatchPolicy,
    metrics: Dict[str, Any],
) -> List[str]:
    flags: List[str] = []

    if priority_signal.participant_role != ParticipantRole.PRIORITY_USER:
        flags.append("priority_signal_role_mismatch")

    if collaborator_signal.participant_role != ParticipantRole.COLLABORATOR:
        flags.append("collaborator_signal_role_mismatch")

    if priority_signal.country.strip().lower() != "argentina":
        flags.append("priority_signal_outside_argentina_context")

    if collaborator_signal.country.strip().lower() != "argentina":
        flags.append("collaborator_signal_outside_argentina_context")

    if policy.require_both_paid:
        if not priority_signal.validation_paid:
            flags.append("priority_validation_payment_not_confirmed")

        if not collaborator_signal.validation_paid:
            flags.append("collaborator_validation_payment_not_confirmed")

    if priority_signal.participant_token == collaborator_signal.participant_token:
        flags.append("same_user_token_not_allowed")

    if priority_signal.payment_method_demo_token == collaborator_signal.payment_method_demo_token:
        flags.append("same_payment_method_token_not_allowed")

    if _looks_like_free_text(priority_signal.participant_token):
        flags.append("priority_token_looks_like_free_text")

    if _looks_like_free_text(collaborator_signal.participant_token):
        flags.append("collaborator_token_looks_like_free_text")

    if not metrics["same_network"]:
        flags.append("different_network_context")

    if not metrics["same_transport_mode"]:
        flags.append("different_transport_mode")

    if not metrics["red_sube_window_matched"]:
        flags.append("red_sube_demo_window_expired")

    if not metrics["effective_sync_window_matched"]:
        if metrics["access_context"] == AccessContext.IN_VEHICLE_AFTER_PAYMENT:
            flags.append("in_vehicle_sync_window_expired")
        elif metrics["access_context"] in {
            AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
            AccessContext.STATION_ACCESS_WAIT,
        }:
            flags.append("station_platform_sync_window_expired")
        else:
            flags.append("effective_sync_window_expired")

    if metrics["match_strength"] == MatchStrength.NO_MATCH:
        flags.append("no_shared_transport_context")

    if (
        metrics["match_strength"] == MatchStrength.SAME_ROUTE_TIME_WINDOW_WEAK
        and policy.route_only_requires_review
    ):
        flags.append("route_only_match_requires_review")

    if (
        metrics["access_context"] == AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE
        and policy.station_platform_requires_same_station
        and not metrics["same_station"]
    ):
        flags.append("station_platform_requires_same_station")

    if (
        priority_signal.validation_point_type == ValidationPointType.VEHICLE_VALIDATOR
        and not priority_signal.vehicle_demo_id
    ):
        flags.append("priority_vehicle_context_missing")

    if (
        collaborator_signal.validation_point_type == ValidationPointType.VEHICLE_VALIDATOR
        and not collaborator_signal.vehicle_demo_id
    ):
        flags.append("collaborator_vehicle_context_missing")

    if (
        priority_signal.validation_point_type == ValidationPointType.STATION_TURNSTILE
        and not priority_signal.station_demo_id
    ):
        flags.append("priority_station_context_missing")

    if (
        collaborator_signal.validation_point_type == ValidationPointType.STATION_TURNSTILE
        and not collaborator_signal.station_demo_id
    ):
        flags.append("collaborator_station_context_missing")

    return flags


def _review_only(risk_flags: List[str]) -> bool:
    review_only_flags = {
        "route_only_match_requires_review",
    }

    return bool(risk_flags) and set(risk_flags).issubset(review_only_flags)


def _access_context(
    priority_signal: ValidationSignal,
    collaborator_signal: ValidationSignal,
) -> AccessContext:
    vehicle_points = {
        priority_signal.validation_point_type,
        collaborator_signal.validation_point_type,
    }

    if vehicle_points == {ValidationPointType.VEHICLE_VALIDATOR}:
        return AccessContext.IN_VEHICLE_AFTER_PAYMENT

    station_points = {
        ValidationPointType.STATION_TURNSTILE,
        ValidationPointType.ACCESS_GATE,
    }

    if (
        priority_signal.validation_point_type in station_points
        and collaborator_signal.validation_point_type in station_points
    ):
        if priority_signal.validation_point_type == ValidationPointType.STATION_TURNSTILE:
            return AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE

        return AccessContext.STATION_ACCESS_WAIT

    return AccessContext.UNKNOWN


def _effective_sync_window_minutes(
    policy: TripWindowMatchPolicy,
    access_context: AccessContext,
) -> int:
    if access_context == AccessContext.IN_VEHICLE_AFTER_PAYMENT:
        return policy.in_vehicle_proximity_minutes_demo

    if access_context in {
        AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        AccessContext.STATION_ACCESS_WAIT,
    }:
        return policy.station_platform_wait_minutes_demo

    return policy.in_vehicle_proximity_minutes_demo


def _match_strength(
    policy: TripWindowMatchPolicy,
    access_context: AccessContext,
    effective_sync_window_matched: bool,
    same_vehicle: bool,
    same_station: bool,
    same_turnstile: bool,
    same_platform: bool,
    same_trip: bool,
    same_route: bool,
) -> MatchStrength:
    if not effective_sync_window_matched:
        return MatchStrength.NO_MATCH

    if policy.allow_vehicle_context_match:
        if access_context == AccessContext.IN_VEHICLE_AFTER_PAYMENT and same_vehicle:
            return MatchStrength.SAME_VEHICLE_STRONG

        if same_trip:
            return MatchStrength.SAME_TRIP_STRONG

    if policy.allow_station_context_match:
        if access_context in {
            AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
            AccessContext.STATION_ACCESS_WAIT,
        }:
            if same_station and same_platform:
                return MatchStrength.SAME_PLATFORM_WAIT_MODERATE

            if same_station or same_turnstile:
                return MatchStrength.SAME_STATION_MODERATE

    if policy.allow_route_time_window_match and same_route:
        return MatchStrength.SAME_ROUTE_TIME_WINDOW_WEAK

    return MatchStrength.NO_MATCH


def _context_summary(
    priority_signal: ValidationSignal,
    collaborator_signal: ValidationSignal,
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "priority_validation_event_demo_id": priority_signal.validation_event_demo_id,
        "collaborator_validation_event_demo_id": collaborator_signal.validation_event_demo_id,
        "priority_role": priority_signal.participant_role.value,
        "collaborator_role": collaborator_signal.participant_role.value,
        "transport_mode": priority_signal.transport_mode.value,
        "validation_point_type_priority": priority_signal.validation_point_type.value,
        "validation_point_type_collaborator": collaborator_signal.validation_point_type.value,
        "access_context": metrics["access_context"].value,
        "effective_sync_window_minutes": metrics["effective_sync_window_minutes"],
        "same_network": metrics["same_network"],
        "same_transport_mode": metrics["same_transport_mode"],
        "same_route": metrics["same_route"],
        "same_vehicle": metrics["same_vehicle"],
        "same_station": metrics["same_station"],
        "same_turnstile": metrics["same_turnstile"],
        "same_platform": metrics["same_platform"],
        "same_trip": metrics["same_trip"],
        "time_delta_seconds": metrics["time_delta_seconds"],
        "match_strength": metrics["match_strength"].value,
    }


def _same_optional(first: Optional[str], second: Optional[str]) -> bool:
    return bool(first and second and first == second)


def _strip_optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    stripped = value.strip()
    return stripped if stripped else None


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
        "vigilancia",
        "premio",
        "puntos",
        "bono solidario",
        "red sube",
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _security_notice() -> str:
    return (
        "El matcher sólo evalúa coincidencia temporal/contextual demostrativa. "
        "Diferencia pago a bordo y pago en molinete porque la espera de tren/subte "
        "puede justificar una ventana mayor. No acredita beneficios por sí solo."
    )


def _privacy_notice() -> str:
    return (
        "El matcher no revela DNI, nombre, domicilio, diagnóstico, CUD, historia clínica "
        "ni certificado médico. Tampoco utiliza geolocalización real."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no verifica coincidencias, no decide matches, no administra beneficios "
        "y no interviene en la sincronización."
    )


def _common_warnings() -> List[str]:
    return [
        "Matcher conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin consulta a cuentas reales.",
        "Sin consulta a tarjetas reales.",
        "Sin geolocalización real.",
        "Sin datos sensibles.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
        "Sin certificados médicos reales.",
        "Sin sanciones.",
        "Sin ranking.",
        "Sin vigilancia.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "La coincidencia temporal no otorga beneficios por sí sola.",
        "La ventana a bordo es más corta que la ventana de espera en andén.",
        "La ventana de molinete contempla espera razonable de tren o subte.",
        "El resultado debe combinarse con confirmación del usuario SUBE Prioridad.",
        "El resultado debe combinarse con flujo antifraude aceptado.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_station_demo(), indent=2, ensure_ascii=False))

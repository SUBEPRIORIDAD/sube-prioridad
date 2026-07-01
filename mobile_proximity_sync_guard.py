"""
SUBE Prioridad — Guardia demo de proximidad móvil no excluyente.

Este módulo evalúa señales móviles opcionales para reforzar la sincronización
solidaria del Bono Solidario.

Regla central:
    La proximidad móvil NO es excluyente.
    No tener celular, app, NFC, BLE, conectividad o tablet no bloquea por sí solo.
    Las señales móviles sirven como refuerzo antifraude y auditoría.

No integra SUBE real.
No integra Red SUBE real.
No consulta tarjetas reales.
No consulta cuentas reales.
No consulta validadoras reales.
No consulta molinetes reales.
No usa DNI.
No usa nombre.
No usa diagnóstico.
No usa CUD visible.
No usa GPS exacto.
No usa IMEI.
No usa MAC.
No genera ranking.
No genera sanciones.
No impone carga al chofer.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Guardia Demo de Proximidad Móvil No Excluyente"
GUARD_VERSION = "0.2.1"
DEMO_MODE = True


PROHIBITED_FIELDS = {
    "dni",
    "documento",
    "nombre",
    "apellido",
    "domicilio",
    "direccion",
    "dirección",
    "telefono",
    "teléfono",
    "phone",
    "email",
    "correo",
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
    "gps",
    "latitud",
    "longitud",
    "latitude",
    "longitude",
    "imei",
    "mac",
    "saldo",
    "dinero",
}


class ProximityGuardStatus(str, Enum):
    ACCEPTED_REINFORCED = "accepted_reinforced"
    ACCEPTED_WITHOUT_MOBILE_EVIDENCE = "accepted_without_mobile_evidence"
    REJECTED_HARD_RISK = "rejected_hard_risk"
    NEEDS_REVIEW = "needs_review"
    DEFERRED_OFFLINE_VALIDATION = "deferred_offline_validation"


class TransportAccessContext(str, Enum):
    IN_VEHICLE_AFTER_PAYMENT = "in_vehicle_after_payment"
    PLATFORM_WAIT_AFTER_TURNSTILE = "platform_wait_after_turnstile"
    STATION_ACCESS_WAIT = "station_access_wait"
    TERMINAL_WAIT = "terminal_wait"
    UNKNOWN = "unknown"


class ProximityMethod(str, Enum):
    NONE_AVAILABLE = "none_available"
    QR_TEMPORARY_DEMO = "qr_temporary_demo"
    NFC_TEMPORARY_DEMO = "nfc_temporary_demo"
    BLE_NEARBY_DEMO = "ble_nearby_demo"
    SAME_DEVICE_SESSION_DEMO = "same_device_session_demo"
    MANUAL_CODE_DEMO = "manual_code_demo"


class ProximityStrength(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NOT_AVAILABLE = "not_available"
    NONE = "none"


@dataclass(frozen=True)
class ProximityGuardPolicy:
    in_vehicle_max_minutes: int
    station_platform_max_minutes: int
    terminal_max_minutes: int
    offline_deferred_validation_window_minutes: int
    mobile_required_for_bonus: bool
    require_mobile_for_extended_context: bool
    allow_offline_deferred_validation: bool
    enable_audit_trail: bool


@dataclass(frozen=True)
class MobileDeviceBindingDemo:
    user_token: str
    device_session_demo_token: str
    payment_method_demo_token: str
    active_binding: bool
    voluntarily_linked_to_payment: bool


@dataclass(frozen=True)
class ProximitySignal:
    sync_event_demo_id: str
    priority_user_token: str
    collaborator_user_token: str
    priority_payment_method_demo_token: str
    collaborator_payment_method_demo_token: str
    transport_access_context: TransportAccessContext
    proximity_method: ProximityMethod
    proximity_attempt_timestamp_utc: datetime
    access_window_started_at_utc: datetime
    trip_window_started_at_utc: datetime
    priority_user_confirms_sync: bool
    collaborator_claims_unilaterally: bool
    same_transport_context: bool
    same_vehicle_demo_id: bool
    same_trainset_demo_id: bool
    same_station_demo_id: bool
    same_platform_demo_id: bool
    access_window_matched: bool
    trip_window_matched: bool
    priority_user_has_mobile_device: bool
    collaborator_has_mobile_device: bool
    qr_or_code_token_demo: Optional[str]
    nfc_handshake_token_demo: Optional[str]
    ble_ephemeral_token_demo: Optional[str]
    priority_device_binding: Optional[MobileDeviceBindingDemo]
    collaborator_device_binding: Optional[MobileDeviceBindingDemo]
    offline_mode_detected: bool
    offline_deferred_minutes_elapsed: int


@dataclass(frozen=True)
class ProximityGuardResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: ProximityGuardStatus
    proximity_strength: ProximityStrength
    mobile_filter_available: bool
    mobile_filter_used: bool
    proximity_reinforced: bool
    non_exclusive_filter: bool
    blocks_solidary_bonus_flow: bool
    requires_audit_review: bool
    hard_risk_flags: List[str]
    audit_flags: List[str]
    audit_record_demo: Dict[str, Any]
    reason: str
    privacy_notice: str
    legal_scope_notice: str
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


def create_demo_proximity_guard_policy(
    in_vehicle_max_minutes: int = 10,
    station_platform_max_minutes: int = 60,
    terminal_max_minutes: int = 60,
    offline_deferred_validation_window_minutes: int = 120,
    mobile_required_for_bonus: bool = False,
    require_mobile_for_extended_context: bool = False,
    allow_offline_deferred_validation: bool = True,
    enable_audit_trail: bool = True,
) -> ProximityGuardPolicy:
    _positive("in_vehicle_max_minutes", in_vehicle_max_minutes)
    _positive("station_platform_max_minutes", station_platform_max_minutes)
    _positive("terminal_max_minutes", terminal_max_minutes)
    _positive(
        "offline_deferred_validation_window_minutes",
        offline_deferred_validation_window_minutes,
    )

    return ProximityGuardPolicy(
        in_vehicle_max_minutes=in_vehicle_max_minutes,
        station_platform_max_minutes=station_platform_max_minutes,
        terminal_max_minutes=terminal_max_minutes,
        offline_deferred_validation_window_minutes=offline_deferred_validation_window_minutes,
        mobile_required_for_bonus=mobile_required_for_bonus,
        require_mobile_for_extended_context=require_mobile_for_extended_context,
        allow_offline_deferred_validation=allow_offline_deferred_validation,
        enable_audit_trail=enable_audit_trail,
    )


def create_demo_mobile_device_binding(
    user_token: str = "demo-user-001",
    device_session_demo_token: str = "demo-device-session-001",
    payment_method_demo_token: str = "demo-payment-method-001",
    active_binding: bool = True,
    voluntarily_linked_to_payment: bool = True,
) -> MobileDeviceBindingDemo:
    required_values = {
        "user_token": user_token,
        "device_session_demo_token": device_session_demo_token,
        "payment_method_demo_token": payment_method_demo_token,
    }

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    return MobileDeviceBindingDemo(
        user_token=user_token.strip(),
        device_session_demo_token=device_session_demo_token.strip(),
        payment_method_demo_token=payment_method_demo_token.strip(),
        active_binding=active_binding,
        voluntarily_linked_to_payment=voluntarily_linked_to_payment,
    )


def create_demo_proximity_signal(
    sync_event_demo_id: str = "demo-mobile-proximity-sync-001",
    priority_user_token: str = "demo-priority-user-001",
    collaborator_user_token: str = "demo-collaborator-user-001",
    priority_payment_method_demo_token: str = "demo-priority-payment-001",
    collaborator_payment_method_demo_token: str = "demo-collaborator-payment-001",
    transport_access_context: TransportAccessContext = TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT,
    proximity_method: ProximityMethod = ProximityMethod.QR_TEMPORARY_DEMO,
    proximity_attempt_timestamp_utc: Optional[datetime] = None,
    access_window_started_at_utc: Optional[datetime] = None,
    trip_window_started_at_utc: Optional[datetime] = None,
    priority_user_confirms_sync: bool = True,
    collaborator_claims_unilaterally: bool = False,
    same_transport_context: bool = True,
    same_vehicle_demo_id: bool = True,
    same_trainset_demo_id: bool = False,
    same_station_demo_id: bool = False,
    same_platform_demo_id: bool = False,
    access_window_matched: bool = True,
    trip_window_matched: bool = True,
    priority_user_has_mobile_device: bool = True,
    collaborator_has_mobile_device: bool = True,
    qr_or_code_token_demo: Optional[str] = "demo-qr-token-001",
    nfc_handshake_token_demo: Optional[str] = None,
    ble_ephemeral_token_demo: Optional[str] = None,
    priority_device_binding: Optional[MobileDeviceBindingDemo] = None,
    collaborator_device_binding: Optional[MobileDeviceBindingDemo] = None,
    offline_mode_detected: bool = False,
    offline_deferred_minutes_elapsed: int = 0,
) -> ProximitySignal:
    required_values = {
        "sync_event_demo_id": sync_event_demo_id,
        "priority_user_token": priority_user_token,
        "collaborator_user_token": collaborator_user_token,
        "priority_payment_method_demo_token": priority_payment_method_demo_token,
        "collaborator_payment_method_demo_token": collaborator_payment_method_demo_token,
    }

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    now = proximity_attempt_timestamp_utc or datetime.now(timezone.utc)
    started_at = access_window_started_at_utc or now - timedelta(minutes=2)
    trip_started_at = trip_window_started_at_utc or started_at

    if priority_device_binding is None and priority_user_has_mobile_device:
        priority_device_binding = create_demo_mobile_device_binding(
            user_token=priority_user_token,
            device_session_demo_token="demo-priority-device-001",
            payment_method_demo_token=priority_payment_method_demo_token,
        )

    if collaborator_device_binding is None and collaborator_user_has_mobile_device:
        collaborator_device_binding = create_demo_mobile_device_binding(
            user_token=collaborator_user_token,
            device_session_demo_token="demo-collaborator-device-001",
            payment_method_demo_token=collaborator_payment_method_demo_token,
        )

    return ProximitySignal(
        sync_event_demo_id=sync_event_demo_id.strip(),
        priority_user_token=priority_user_token.strip(),
        collaborator_user_token=collaborator_user_token.strip(),
        priority_payment_method_demo_token=priority_payment_method_demo_token.strip(),
        collaborator_payment_method_demo_token=collaborator_payment_method_demo_token.strip(),
        transport_access_context=transport_access_context,
        proximity_method=proximity_method,
        proximity_attempt_timestamp_utc=now,
        access_window_started_at_utc=started_at,
        trip_window_started_at_utc=trip_started_at,
        priority_user_confirms_sync=priority_user_confirms_sync,
        collaborator_claims_unilaterally=collaborator_claims_unilaterally,
        same_transport_context=same_transport_context,
        same_vehicle_demo_id=same_vehicle_demo_id,
        same_trainset_demo_id=same_trainset_demo_id,
        same_station_demo_id=same_station_demo_id,
        same_platform_demo_id=same_platform_demo_id,
        access_window_matched=access_window_matched,
        trip_window_matched=trip_window_matched,
        priority_user_has_mobile_device=priority_user_has_mobile_device,
        collaborator_has_mobile_device=collaborator_has_mobile_device,
        qr_or_code_token_demo=qr_or_code_token_demo,
        nfc_handshake_token_demo=nfc_handshake_token_demo,
        ble_ephemeral_token_demo=ble_ephemeral_token_demo,
        priority_device_binding=priority_device_binding,
        collaborator_device_binding=collaborator_device_binding,
        offline_mode_detected=offline_mode_detected,
        offline_deferred_minutes_elapsed=offline_deferred_minutes_elapsed,
    )


def create_demo_station_extended_proximity_signal(
    created_at_utc: Optional[datetime] = None,
) -> ProximitySignal:
    now = created_at_utc or datetime.now(timezone.utc)

    return create_demo_proximity_signal(
        sync_event_demo_id="demo-station-extended-proximity-001",
        transport_access_context=TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        proximity_method=ProximityMethod.BLE_NEARBY_DEMO,
        proximity_attempt_timestamp_utc=now,
        access_window_started_at_utc=now - timedelta(minutes=25),
        trip_window_started_at_utc=now - timedelta(minutes=25),
        same_vehicle_demo_id=False,
        same_station_demo_id=True,
        same_platform_demo_id=True,
        qr_or_code_token_demo=None,
        ble_ephemeral_token_demo="demo-ble-token-001",
    )


def create_demo_no_mobile_proximity_signal(
    created_at_utc: Optional[datetime] = None,
) -> ProximitySignal:
    now = created_at_utc or datetime.now(timezone.utc)

    return create_demo_proximity_signal(
        sync_event_demo_id="demo-no-mobile-proximity-001",
        proximity_method=ProximityMethod.NONE_AVAILABLE,
        proximity_attempt_timestamp_utc=now,
        access_window_started_at_utc=now - timedelta(minutes=2),
        trip_window_started_at_utc=now - timedelta(minutes=2),
        priority_user_has_mobile_device=False,
        collaborator_has_mobile_device=False,
        qr_or_code_token_demo=None,
        nfc_handshake_token_demo=None,
        ble_ephemeral_token_demo=None,
        priority_device_binding=None,
        collaborator_device_binding=None,
    )


def evaluate_mobile_proximity_sync_guard(
    signal: ProximitySignal,
    policy: Optional[ProximityGuardPolicy] = None,
) -> ProximityGuardResult:
    policy = policy or create_demo_proximity_guard_policy()

    assert_no_prohibited_fields(
        {
            "sync_event_demo_id": signal.sync_event_demo_id,
            "priority_user_token": signal.priority_user_token,
            "collaborator_user_token": signal.collaborator_user_token,
            "priority_payment_method_demo_token": signal.priority_payment_method_demo_token,
            "collaborator_payment_method_demo_token": signal.collaborator_payment_method_demo_token,
        }
    )

    metrics = _metrics(signal, policy)
    hard_risk_flags = _hard_risk_flags(signal, policy, metrics)
    audit_flags = _audit_flags(signal, policy, metrics)
    strength = _proximity_strength(signal, policy, metrics["mobile_filter_used"])

    if signal.offline_mode_detected and not hard_risk_flags:
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.DEFERRED_OFFLINE_VALIDATION,
            proximity_strength=strength,
            hard_risk_flags=[],
            audit_flags=audit_flags,
            blocks_solidary_bonus_flow=False,
            requires_audit_review=True,
            reason=(
                "La sincronización queda diferida por modo offline. La falta de "
                "conectividad no bloquea por sí sola, pero exige auditoría posterior."
            ),
        )

    if hard_risk_flags:
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.REJECTED_HARD_RISK,
            proximity_strength=strength,
            hard_risk_flags=hard_risk_flags,
            audit_flags=audit_flags,
            blocks_solidary_bonus_flow=True,
            requires_audit_review=True,
            reason=(
                "La guardia móvil rechazó el flujo por riesgo duro o condición mínima "
                "incumplida."
            ),
        )

    if metrics["proximity_reinforced"]:
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.ACCEPTED_REINFORCED,
            proximity_strength=strength,
            hard_risk_flags=[],
            audit_flags=audit_flags,
            blocks_solidary_bonus_flow=False,
            requires_audit_review=bool(audit_flags),
            reason=(
                "La sincronización fue aceptada con refuerzo móvil demo. El filtro "
                "móvil sigue siendo no excluyente."
            ),
        )

    return _result(
        signal=signal,
        policy=policy,
        metrics=metrics,
        status=ProximityGuardStatus.ACCEPTED_WITHOUT_MOBILE_EVIDENCE,
        proximity_strength=strength,
        hard_risk_flags=[],
        audit_flags=audit_flags,
        blocks_solidary_bonus_flow=False,
        requires_audit_review=True,
        reason=(
            "La sincronización fue aceptada sin evidencia móvil. La ausencia o no uso "
            "de móvil no bloquea por sí solo."
        ),
    )


def result_to_dict(result: ProximityGuardResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "proximity_strength": result.proximity_strength.value,
        "mobile_filter_available": result.mobile_filter_available,
        "mobile_filter_used": result.mobile_filter_used,
        "proximity_reinforced": result.proximity_reinforced,
        "non_exclusive_filter": result.non_exclusive_filter,
        "blocks_solidary_bonus_flow": result.blocks_solidary_bonus_flow,
        "requires_audit_review": result.requires_audit_review,
        "hard_risk_flags": result.hard_risk_flags,
        "audit_flags": result.audit_flags,
        "audit_record_demo": result.audit_record_demo,
        "reason": result.reason,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    result = evaluate_mobile_proximity_sync_guard(create_demo_proximity_signal())

    return result_to_dict(result)


def run_station_demo() -> Dict[str, Any]:
    result = evaluate_mobile_proximity_sync_guard(
        create_demo_station_extended_proximity_signal()
    )

    return result_to_dict(result)


def run_no_mobile_demo() -> Dict[str, Any]:
    result = evaluate_mobile_proximity_sync_guard(
        create_demo_no_mobile_proximity_signal()
    )

    return result_to_dict(result)


def _metrics(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
) -> Dict[str, Any]:
    mobile_filter_available = (
        signal.priority_user_has_mobile_device
        or signal.collaborator_has_mobile_device
        or signal.priority_device_binding is not None
        or signal.collaborator_device_binding is not None
    )

    handshake_signal_present = _handshake_signal_present(signal)
    device_binding_matched = _device_binding_matched(signal)

    mobile_filter_used = mobile_filter_available and (
        handshake_signal_present
        or (
            signal.proximity_method == ProximityMethod.SAME_DEVICE_SESSION_DEMO
            and device_binding_matched
        )
    )

    proximity_reinforced = mobile_filter_used and _proximity_strength(
        signal=signal,
        policy=policy,
        mobile_filter_used=mobile_filter_used,
    ) in {
        ProximityStrength.STRONG,
        ProximityStrength.MODERATE,
    }

    return {
        "mobile_filter_available": mobile_filter_available,
        "mobile_filter_used": mobile_filter_used,
        "mobile_filter_absent": not mobile_filter_available,
        "mobile_filter_available_but_not_used": (
            mobile_filter_available and not mobile_filter_used
        ),
        "handshake_signal_present": handshake_signal_present,
        "device_binding_matched": device_binding_matched,
        "proximity_reinforced": proximity_reinforced,
    }


def _hard_risk_flags(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
) -> List[str]:
    flags: List[str] = []

    if _looks_like_free_text(signal.sync_event_demo_id):
        flags.append("sync_event_id_looks_like_free_text")

    if _looks_like_free_text(signal.priority_user_token):
        flags.append("priority_user_token_looks_like_free_text")

    if _looks_like_free_text(signal.collaborator_user_token):
        flags.append("collaborator_user_token_looks_like_free_text")

    if signal.priority_user_token == signal.collaborator_user_token:
        flags.append("same_user_token_not_allowed")

    if signal.priority_payment_method_demo_token == signal.collaborator_payment_method_demo_token:
        flags.append("same_payment_method_not_allowed")

    if not signal.priority_user_confirms_sync:
        flags.append("priority_user_confirmation_required")

    if signal.collaborator_claims_unilaterally:
        flags.append("collaborator_unilateral_claim")

    if not signal.access_window_matched:
        flags.append("access_window_not_matched")

    if not signal.trip_window_matched:
        flags.append("trip_window_not_matched")

    if not signal.same_transport_context:
        flags.append("no_shared_transport_context")

    if signal.transport_access_context == TransportAccessContext.UNKNOWN:
        flags.append("unknown_transport_access_context")

    if _access_context_expired(signal, policy):
        flags.append("access_context_window_expired")

    if (
        signal.offline_mode_detected
        and not policy.allow_offline_deferred_validation
    ):
        flags.append("offline_deferred_validation_not_allowed")

    if (
        signal.offline_mode_detected
        and signal.offline_deferred_minutes_elapsed
        > policy.offline_deferred_validation_window_minutes
    ):
        flags.append("offline_deferred_validation_window_expired")

    if policy.mobile_required_for_bonus and not metrics["mobile_filter_used"]:
        flags.append("mobile_required_by_policy")

    if (
        policy.require_mobile_for_extended_context
        and signal.transport_access_context
        in {
            TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
            TransportAccessContext.STATION_ACCESS_WAIT,
            TransportAccessContext.TERMINAL_WAIT,
        }
        and not metrics["mobile_filter_used"]
    ):
        flags.append("mobile_required_for_extended_context_by_policy")

    return _deduplicate(flags)


def _audit_flags(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
) -> List[str]:
    flags: List[str] = []

    if not policy.enable_audit_trail:
        return flags

    flags.append("mobile_proximity_guard_audit")

    if metrics["mobile_filter_absent"]:
        flags.append("mobile_filter_absent_non_blocking")

    if metrics["mobile_filter_available_but_not_used"]:
        flags.append("mobile_filter_available_but_not_used")

    if not signal.priority_user_has_mobile_device:
        flags.append("priority_user_without_mobile_supported")

    if not signal.collaborator_has_mobile_device:
        flags.append("collaborator_without_mobile_supported")

    if signal.transport_access_context in {
        TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        TransportAccessContext.STATION_ACCESS_WAIT,
    }:
        flags.append("station_or_platform_context_audit")

        if not metrics["proximity_reinforced"]:
            flags.append("extended_context_without_mobile_reinforcement_audit")

    if signal.transport_access_context == TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT:
        flags.append("in_vehicle_context_audit")

    if signal.offline_mode_detected:
        flags.append("offline_deferred_validation_audit")

    if _has_inactive_binding(signal):
        flags.append("inactive_device_binding_audit")

    if _has_not_linked_to_payment_binding(signal):
        flags.append("device_not_linked_to_payment_audit")

    return _deduplicate(flags)


def _proximity_strength(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    mobile_filter_used: bool,
) -> ProximityStrength:
    if not mobile_filter_used:
        if (
            not signal.priority_user_has_mobile_device
            and not signal.collaborator_has_mobile_device
        ):
            return ProximityStrength.NOT_AVAILABLE

        return ProximityStrength.NONE

    if signal.proximity_method in {
        ProximityMethod.NFC_TEMPORARY_DEMO,
        ProximityMethod.QR_TEMPORARY_DEMO,
        ProximityMethod.SAME_DEVICE_SESSION_DEMO,
    }:
        return ProximityStrength.STRONG

    if signal.proximity_method in {
        ProximityMethod.BLE_NEARBY_DEMO,
        ProximityMethod.MANUAL_CODE_DEMO,
    }:
        return ProximityStrength.MODERATE

    return ProximityStrength.WEAK


def _handshake_signal_present(signal: ProximitySignal) -> bool:
    if signal.proximity_method == ProximityMethod.NONE_AVAILABLE:
        return False

    if signal.proximity_method == ProximityMethod.QR_TEMPORARY_DEMO:
        return bool(signal.qr_or_code_token_demo)

    if signal.proximity_method == ProximityMethod.MANUAL_CODE_DEMO:
        return bool(signal.qr_or_code_token_demo)

    if signal.proximity_method == ProximityMethod.NFC_TEMPORARY_DEMO:
        return bool(signal.nfc_handshake_token_demo)

    if signal.proximity_method == ProximityMethod.BLE_NEARBY_DEMO:
        return bool(signal.ble_ephemeral_token_demo)

    if signal.proximity_method == ProximityMethod.SAME_DEVICE_SESSION_DEMO:
        return True

    return False


def _device_binding_matched(signal: ProximitySignal) -> bool:
    bindings = [
        signal.priority_device_binding,
        signal.collaborator_device_binding,
    ]

    existing = [binding for binding in bindings if binding is not None]

    if not existing:
        return False

    return all(
        binding.active_binding and binding.voluntarily_linked_to_payment
        for binding in existing
    )


def _access_context_expired(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
) -> bool:
    elapsed_minutes = (
        signal.proximity_attempt_timestamp_utc - signal.access_window_started_at_utc
    ).total_seconds() / 60

    if signal.transport_access_context == TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT:
        return elapsed_minutes > policy.in_vehicle_max_minutes

    if signal.transport_access_context in {
        TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        TransportAccessContext.STATION_ACCESS_WAIT,
    }:
        return elapsed_minutes > policy.station_platform_max_minutes

    if signal.transport_access_context == TransportAccessContext.TERMINAL_WAIT:
        return elapsed_minutes > policy.terminal_max_minutes

    return False


def _has_inactive_binding(signal: ProximitySignal) -> bool:
    return any(
        binding is not None and not binding.active_binding
        for binding in [
            signal.priority_device_binding,
            signal.collaborator_device_binding,
        ]
    )


def _has_not_linked_to_payment_binding(signal: ProximitySignal) -> bool:
    return any(
        binding is not None and not binding.voluntarily_linked_to_payment
        for binding in [
            signal.priority_device_binding,
            signal.collaborator_device_binding,
        ]
    )


def _result(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
    status: ProximityGuardStatus,
    proximity_strength: ProximityStrength,
    hard_risk_flags: List[str],
    audit_flags: List[str],
    blocks_solidary_bonus_flow: bool,
    requires_audit_review: bool,
    reason: str,
) -> ProximityGuardResult:
    return ProximityGuardResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=GUARD_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        proximity_strength=proximity_strength,
        mobile_filter_available=metrics["mobile_filter_available"],
        mobile_filter_used=metrics["mobile_filter_used"],
        proximity_reinforced=metrics["proximity_reinforced"],
        non_exclusive_filter=True,
        blocks_solidary_bonus_flow=blocks_solidary_bonus_flow,
        requires_audit_review=requires_audit_review,
        hard_risk_flags=hard_risk_flags,
        audit_flags=audit_flags,
        audit_record_demo=_audit_record_demo(signal, policy, metrics),
        reason=reason,
        privacy_notice=_privacy_notice(),
        legal_scope_notice=_legal_scope_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )


def _audit_record_demo(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "sync_event_demo_id": signal.sync_event_demo_id,
        "transport_access_context": signal.transport_access_context.value,
        "proximity_method": signal.proximity_method.value,
        "mobile_filter_available": metrics["mobile_filter_available"],
        "mobile_filter_used": metrics["mobile_filter_used"],
        "proximity_reinforced": metrics["proximity_reinforced"],
        "same_transport_context": signal.same_transport_context,
        "same_vehicle_demo_id": signal.same_vehicle_demo_id,
        "same_trainset_demo_id": signal.same_trainset_demo_id,
        "same_station_demo_id": signal.same_station_demo_id,
        "same_platform_demo_id": signal.same_platform_demo_id,
        "access_window_matched": signal.access_window_matched,
        "trip_window_matched": signal.trip_window_matched,
        "offline_mode_detected": signal.offline_mode_detected,
        "offline_deferred_minutes_elapsed": signal.offline_deferred_minutes_elapsed,
        "mobile_required_for_bonus": policy.mobile_required_for_bonus,
        "require_mobile_for_extended_context": policy.require_mobile_for_extended_context,
    }


def _privacy_notice() -> str:
    return (
        "La guardia móvil no revela DNI, nombre, domicilio, diagnóstico, CUD, "
        "certificado médico, historia clínica, teléfono, email, IMEI, MAC, saldo "
        "ni GPS exacto."
    )


def _legal_scope_notice() -> str:
    return (
        "La proximidad móvil es una señal demo no excluyente. No integra SUBE real, "
        "no integra Red SUBE real, no aplica beneficios reales y no modifica saldo."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no verifica proximidad móvil, no decide beneficios, no controla "
        "datos personales y no recibe una obligación nueva."
    )


def _common_warnings() -> List[str]:
    return [
        "Filtro móvil no excluyente.",
        "Sin obligación de tener celular.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin consulta a cuentas reales.",
        "Sin consulta a tarjetas reales.",
        "Sin consulta a validadoras reales.",
        "Sin consulta a molinetes reales.",
        "Sin saldo real.",
        "Sin tarifa real.",
        "Sin DNI.",
        "Sin diagnóstico médico.",
        "Sin CUD visible.",
        "Sin teléfono real.",
        "Sin email real.",
        "Sin IMEI real.",
        "Sin MAC real.",
        "Sin GPS exacto.",
        "Sin vigilancia.",
        "Sin ranking.",
        "Sin sanciones.",
        "La ausencia de móvil no bloquea por sí sola.",
        "Tener móvil disponible no significa haber usado proximidad móvil.",
        "QR, NFC, BLE, código manual o sesión compartida pueden reforzar auditoría.",
    ]


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
        "gps",
        "telefono",
        "teléfono",
        "email",
        "saldo",
        "dinero",
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _positive(field_name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"El campo {field_name} debe ser mayor a cero.")


def _validate_required_values(required_values: Dict[str, str]) -> None:
    for field_name, value in required_values.items():
        if not value or not value.strip():
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")


def _deduplicate(flags: List[str]) -> List[str]:
    seen = set()
    result = []

    for flag in flags:
        if flag not in seen:
            seen.add(flag)
            result.append(flag)

    return result


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_station_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_no_mobile_demo(), indent=2, ensure_ascii=False))

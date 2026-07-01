"""
SUBE Prioridad — Guardia demostrativa de proximidad para sincronización solidaria.

Este módulo modela una segunda capa antifraude para el Bono Solidario.

Problema que resuelve:
    En trenes, subtes, estaciones, andenes o terminales, dos personas pueden haber
    validado su viaje dentro de una ventana amplia, pero eso no prueba por sí solo
    que hayan estado cerca al momento real de la cesión del asiento.

Por eso este módulo separa:

    1. Ventana de acceso o validación.
    2. Cercanía razonable al momento de sincronizar.
    3. Confirmación voluntaria del usuario SUBE Prioridad.
    4. Señales no sensibles y tokenizadas.

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No consulta bases reales.
No consulta tarjetas reales.
No consulta cuentas reales.
No usa geolocalización GPS exacta.
No procesa DNI.
No procesa nombre.
No procesa domicilio.
No procesa diagnóstico.
No procesa CUD.
No procesa certificados médicos.
No usa número de teléfono real.
No usa email real.
No genera sanciones.
No genera rankings.
No genera vigilancia.
No impone obligaciones a pasajeros.
No impone cargas operativas al chofer.

Señales admitidas en modo demo:
    - QR temporal.
    - NFC temporal.
    - BLE/Bluetooth Low Energy demostrativo.
    - token de dispositivo.
    - token de medio de pago.
    - token de tarjeta SUBE demo.
    - mismo contexto de estación, andén, unidad o formación.
    - validación diferida offline.
    - confirmación del usuario SUBE Prioridad.

Regla central:
    La validación de pago habilita una ventana.
    La sincronización digital genera una solicitud.
    La proximidad reforzada reduce riesgo de fraude.
    El Bono Solidario demo sólo puede avanzar si las capas mínimas coinciden.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Guardia Demo de Proximidad Móvil"
GUARD_VERSION = "0.1.0"
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
    "phone",
    "email",
    "correo",
    "gps",
    "latitud",
    "longitud",
    "latitude",
    "longitude",
}


class ProximityGuardStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"
    DEFERRED_OFFLINE_VALIDATION = "deferred_offline_validation"


class TransportAccessContext(str, Enum):
    IN_VEHICLE_AFTER_PAYMENT = "in_vehicle_after_payment"
    PLATFORM_WAIT_AFTER_TURNSTILE = "platform_wait_after_turnstile"
    STATION_ACCESS_WAIT = "station_access_wait"
    TERMINAL_WAIT = "terminal_wait"
    UNKNOWN = "unknown"


class ProximityMethod(str, Enum):
    QR_TEMPORARY_DEMO = "qr_temporary_demo"
    NFC_TEMPORARY_DEMO = "nfc_temporary_demo"
    BLE_NEARBY_DEMO = "ble_nearby_demo"
    SAME_DEVICE_SESSION_DEMO = "same_device_session_demo"
    MANUAL_CODE_DEMO = "manual_code_demo"


class ProximityStrength(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NONE = "none"


@dataclass(frozen=True)
class ProximityGuardPolicy:
    """
    Política demostrativa para evaluar cercanía al momento de sincronizar.

    in_vehicle_sync_window_minutes:
        Ventana corta para colectivo, tren con validadora a bordo o unidad donde
        ambos ya se encuentran físicamente dentro del transporte.

    station_extended_access_window_minutes:
        Ventana más amplia para molinetes, estaciones, andenes y espera de tren/subte.

    sync_moment_proximity_window_minutes:
        Ventana estricta para el momento real del agradecimiento o sincronización.

    require_device_or_handshake_for_extended_context:
        En estación/andén, una ventana amplia no alcanza sola. Se exige señal
        adicional: QR, NFC, BLE, token de dispositivo o código temporal.
    """

    in_vehicle_sync_window_minutes: int
    station_extended_access_window_minutes: int
    sync_moment_proximity_window_minutes: int
    require_user_confirmation: bool
    require_distinct_users: bool
    require_distinct_payment_methods: bool
    require_device_or_handshake_for_extended_context: bool
    allow_offline_deferred_validation: bool
    max_pending_offline_minutes: int


@dataclass(frozen=True)
class MobileDeviceBindingDemo:
    """
    Vinculación demostrativa de dispositivo.

    No contiene número de teléfono real.
    No contiene email real.
    No contiene IMEI real.
    No contiene identidad civil.
    """

    device_session_token: str
    account_demo_token: str
    payment_method_demo_token: str
    sube_card_demo_token: str
    mobile_account_linked_to_payment_demo: bool
    device_binding_active: bool


@dataclass(frozen=True)
class ProximitySignal:
    """
    Señal demostrativa de cercanía.

    No usa GPS exacto.
    No usa ubicación real.
    No identifica civilmente a las personas.
    """

    sync_event_demo_id: str
    priority_user_token: str
    collaborator_token: str
    access_context: TransportAccessContext
    proximity_method: ProximityMethod
    priority_device: Optional[MobileDeviceBindingDemo]
    collaborator_device: Optional[MobileDeviceBindingDemo]
    qr_or_code_token_demo: Optional[str]
    nfc_handshake_token_demo: Optional[str]
    ble_ephemeral_token_demo: Optional[str]
    same_network_demo_id: bool
    same_route_demo_id: bool
    same_station_demo_id: bool
    same_platform_demo_id: bool
    same_vehicle_demo_id: bool
    same_trainset_demo_id: bool
    same_service_window_demo_id: bool
    access_window_matched: bool
    trip_window_matched: bool
    priority_user_confirms_sync: bool
    collaborator_claims_unilaterally: bool
    offline_mode: bool
    created_at_utc: datetime
    sync_attempted_at_utc: datetime


@dataclass(frozen=True)
class ProximityGuardResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: ProximityGuardStatus
    proximity_strength: ProximityStrength
    proximity_accepted: bool
    requires_deferred_validation: bool
    access_context: str
    proximity_method: str
    access_window_matched: bool
    trip_window_matched: bool
    sync_moment_window_matched: bool
    device_binding_matched: bool
    handshake_signal_present: bool
    same_transport_context_score: int
    risk_flags: List[str]
    reason: str
    security_summary: Dict[str, Any]
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    timestamp_utc: str


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza campos personales, médicos, GPS exacto o sensibles.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_proximity_guard_policy(
    in_vehicle_sync_window_minutes: int = 10,
    station_extended_access_window_minutes: int = 60,
    sync_moment_proximity_window_minutes: int = 5,
    require_user_confirmation: bool = True,
    require_distinct_users: bool = True,
    require_distinct_payment_methods: bool = True,
    require_device_or_handshake_for_extended_context: bool = True,
    allow_offline_deferred_validation: bool = True,
    max_pending_offline_minutes: int = 120,
) -> ProximityGuardPolicy:
    """
    Crea política demostrativa para la guardia de proximidad.
    """
    if in_vehicle_sync_window_minutes <= 0:
        raise ValueError("La ventana a bordo debe ser mayor a cero minutos.")

    if station_extended_access_window_minutes <= 0:
        raise ValueError("La ventana extendida de estación debe ser mayor a cero minutos.")

    if sync_moment_proximity_window_minutes <= 0:
        raise ValueError("La ventana de proximidad al sincronizar debe ser mayor a cero minutos.")

    if max_pending_offline_minutes <= 0:
        raise ValueError("La ventana offline diferida debe ser mayor a cero minutos.")

    if station_extended_access_window_minutes < in_vehicle_sync_window_minutes:
        raise ValueError(
            "La ventana extendida de estación no puede ser menor que la ventana a bordo."
        )

    return ProximityGuardPolicy(
        in_vehicle_sync_window_minutes=in_vehicle_sync_window_minutes,
        station_extended_access_window_minutes=station_extended_access_window_minutes,
        sync_moment_proximity_window_minutes=sync_moment_proximity_window_minutes,
        require_user_confirmation=require_user_confirmation,
        require_distinct_users=require_distinct_users,
        require_distinct_payment_methods=require_distinct_payment_methods,
        require_device_or_handshake_for_extended_context=require_device_or_handshake_for_extended_context,
        allow_offline_deferred_validation=allow_offline_deferred_validation,
        max_pending_offline_minutes=max_pending_offline_minutes,
    )


def create_demo_mobile_device_binding(
    device_session_token: str = "demo-device-session-001",
    account_demo_token: str = "demo-account-001",
    payment_method_demo_token: str = "demo-payment-method-001",
    sube_card_demo_token: str = "demo-sube-card-001",
    mobile_account_linked_to_payment_demo: bool = True,
    device_binding_active: bool = True,
) -> MobileDeviceBindingDemo:
    """
    Crea vinculación demostrativa de dispositivo.
    """
    required_values = {
        "device_session_token": device_session_token,
        "account_demo_token": account_demo_token,
        "payment_method_demo_token": payment_method_demo_token,
        "sube_card_demo_token": sube_card_demo_token,
    }

    for field_name, value in required_values.items():
        if not value or not value.strip():
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")

    assert_no_prohibited_fields(required_values)

    return MobileDeviceBindingDemo(
        device_session_token=device_session_token.strip(),
        account_demo_token=account_demo_token.strip(),
        payment_method_demo_token=payment_method_demo_token.strip(),
        sube_card_demo_token=sube_card_demo_token.strip(),
        mobile_account_linked_to_payment_demo=mobile_account_linked_to_payment_demo,
        device_binding_active=device_binding_active,
    )


def create_demo_proximity_signal(
    sync_event_demo_id: str = "demo-proximity-sync-001",
    priority_user_token: str = "demo-priority-user-001",
    collaborator_token: str = "demo-collaborator-001",
    access_context: TransportAccessContext = TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT,
    proximity_method: ProximityMethod = ProximityMethod.QR_TEMPORARY_DEMO,
    priority_device: Optional[MobileDeviceBindingDemo] = None,
    collaborator_device: Optional[MobileDeviceBindingDemo] = None,
    qr_or_code_token_demo: Optional[str] = "demo-qr-token-001",
    nfc_handshake_token_demo: Optional[str] = None,
    ble_ephemeral_token_demo: Optional[str] = None,
    same_network_demo_id: bool = True,
    same_route_demo_id: bool = True,
    same_station_demo_id: bool = False,
    same_platform_demo_id: bool = False,
    same_vehicle_demo_id: bool = True,
    same_trainset_demo_id: bool = False,
    same_service_window_demo_id: bool = True,
    access_window_matched: bool = True,
    trip_window_matched: bool = True,
    priority_user_confirms_sync: bool = True,
    collaborator_claims_unilaterally: bool = False,
    offline_mode: bool = False,
    created_at_utc: Optional[datetime] = None,
    sync_attempted_at_utc: Optional[datetime] = None,
) -> ProximitySignal:
    """
    Crea señal demostrativa de proximidad.
    """
    required_values = {
        "sync_event_demo_id": sync_event_demo_id,
        "priority_user_token": priority_user_token,
        "collaborator_token": collaborator_token,
    }

    for field_name, value in required_values.items():
        if not value or not value.strip():
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")

    assert_no_prohibited_fields(required_values)

    now = created_at_utc or datetime.now(timezone.utc)

    return ProximitySignal(
        sync_event_demo_id=sync_event_demo_id.strip(),
        priority_user_token=priority_user_token.strip(),
        collaborator_token=collaborator_token.strip(),
        access_context=access_context,
        proximity_method=proximity_method,
        priority_device=priority_device
        or create_demo_mobile_device_binding(
            device_session_token="demo-priority-device-session-001",
            account_demo_token="demo-priority-account-001",
            payment_method_demo_token="demo-priority-payment-001",
            sube_card_demo_token="demo-priority-sube-card-001",
        ),
        collaborator_device=collaborator_device
        or create_demo_mobile_device_binding(
            device_session_token="demo-collaborator-device-session-001",
            account_demo_token="demo-collaborator-account-001",
            payment_method_demo_token="demo-collaborator-payment-001",
            sube_card_demo_token="demo-collaborator-sube-card-001",
        ),
        qr_or_code_token_demo=_strip_optional(qr_or_code_token_demo),
        nfc_handshake_token_demo=_strip_optional(nfc_handshake_token_demo),
        ble_ephemeral_token_demo=_strip_optional(ble_ephemeral_token_demo),
        same_network_demo_id=same_network_demo_id,
        same_route_demo_id=same_route_demo_id,
        same_station_demo_id=same_station_demo_id,
        same_platform_demo_id=same_platform_demo_id,
        same_vehicle_demo_id=same_vehicle_demo_id,
        same_trainset_demo_id=same_trainset_demo_id,
        same_service_window_demo_id=same_service_window_demo_id,
        access_window_matched=access_window_matched,
        trip_window_matched=trip_window_matched,
        priority_user_confirms_sync=priority_user_confirms_sync,
        collaborator_claims_unilaterally=collaborator_claims_unilaterally,
        offline_mode=offline_mode,
        created_at_utc=now,
        sync_attempted_at_utc=sync_attempted_at_utc or now + timedelta(minutes=2),
    )


def create_demo_station_extended_proximity_signal(
    created_at_utc: Optional[datetime] = None,
) -> ProximitySignal:
    """
    Crea caso demo de tren/subte:
        - validación previa en molinete;
        - espera en andén;
        - ventana extendida;
        - señal BLE/QR al momento de sincronizar;
        - mismo andén o misma estación.
    """
    timestamp = created_at_utc or datetime.now(timezone.utc)

    return create_demo_proximity_signal(
        sync_event_demo_id="demo-station-proximity-sync-001",
        access_context=TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        proximity_method=ProximityMethod.BLE_NEARBY_DEMO,
        qr_or_code_token_demo=None,
        ble_ephemeral_token_demo="demo-ble-token-001",
        same_network_demo_id=True,
        same_route_demo_id=True,
        same_station_demo_id=True,
        same_platform_demo_id=True,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_service_window_demo_id=True,
        access_window_matched=True,
        trip_window_matched=True,
        created_at_utc=timestamp,
        sync_attempted_at_utc=timestamp + timedelta(minutes=45),
    )


def evaluate_mobile_proximity_sync_guard(
    signal: ProximitySignal,
    policy: Optional[ProximityGuardPolicy] = None,
) -> ProximityGuardResult:
    """
    Evalúa la proximidad demostrativa al momento de sincronizar.

    La aceptación no acredita el Bono Solidario por sí sola.
    Sólo habilita una capa técnica para módulos posteriores.
    """
    policy = policy or create_demo_proximity_guard_policy()

    assert_no_prohibited_fields(
        {
            "sync_event_demo_id": signal.sync_event_demo_id,
            "priority_user_token": signal.priority_user_token,
            "collaborator_token": signal.collaborator_token,
        }
    )

    metrics = _metrics(signal, policy)
    risk_flags = _risk_flags(signal, policy, metrics)
    strength = _proximity_strength(signal, metrics)

    if signal.offline_mode and _offline_can_be_deferred(policy, metrics, risk_flags):
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.DEFERRED_OFFLINE_VALIDATION,
            proximity_strength=strength,
            proximity_accepted=False,
            requires_deferred_validation=True,
            risk_flags=["offline_validation_pending"],
            reason=(
                "La sincronización se registró en modo offline. "
                "Debe validarse en diferido cuando exista conectividad."
            ),
        )

    if risk_flags:
        status = (
            ProximityGuardStatus.NEEDS_REVIEW
            if _review_only(risk_flags)
            else ProximityGuardStatus.REJECTED
        )

        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=status,
            proximity_strength=strength,
            proximity_accepted=False,
            requires_deferred_validation=False,
            risk_flags=risk_flags,
            reason=(
                "La guardia de proximidad no aceptó la sincronización porque "
                "la solicitud no supera las reglas mínimas antifraude."
            ),
        )

    return _result(
        signal=signal,
        policy=policy,
        metrics=metrics,
        status=ProximityGuardStatus.ACCEPTED,
        proximity_strength=strength,
        proximity_accepted=True,
        requires_deferred_validation=False,
        risk_flags=[],
        reason=(
            "Guardia de proximidad aceptada: existe señal voluntaria, no sensible "
            "y razonable de cercanía al momento de sincronizar."
        ),
    )


def result_to_dict(result: ProximityGuardResult) -> Dict[str, Any]:
    """
    Convierte el resultado a diccionario serializable.
    """
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "proximity_strength": result.proximity_strength.value,
        "proximity_accepted": result.proximity_accepted,
        "requires_deferred_validation": result.requires_deferred_validation,
        "access_context": result.access_context,
        "proximity_method": result.proximity_method,
        "access_window_matched": result.access_window_matched,
        "trip_window_matched": result.trip_window_matched,
        "sync_moment_window_matched": result.sync_moment_window_matched,
        "device_binding_matched": result.device_binding_matched,
        "handshake_signal_present": result.handshake_signal_present,
        "same_transport_context_score": result.same_transport_context_score,
        "risk_flags": result.risk_flags,
        "reason": result.reason,
        "security_summary": result.security_summary,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta demo estable de validadora a bordo.
    """
    signal = create_demo_proximity_signal()

    result = evaluate_mobile_proximity_sync_guard(signal)

    return result_to_dict(result)


def run_station_demo() -> Dict[str, Any]:
    """
    Ejecuta demo estable de estación/andén con ventana extendida.
    """
    signal = create_demo_station_extended_proximity_signal()

    result = evaluate_mobile_proximity_sync_guard(signal)

    return result_to_dict(result)


def _metrics(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
) -> Dict[str, Any]:
    elapsed_seconds = int(
        abs((signal.sync_attempted_at_utc - signal.created_at_utc).total_seconds())
    )

    access_window_minutes = _access_window_minutes(signal.access_context, policy)

    access_context_window_matched = elapsed_seconds <= int(
        timedelta(minutes=access_window_minutes).total_seconds()
    )

    sync_moment_window_matched = elapsed_seconds <= int(
        timedelta(minutes=policy.sync_moment_proximity_window_minutes).total_seconds()
    )

    offline_pending_window_matched = elapsed_seconds <= int(
        timedelta(minutes=policy.max_pending_offline_minutes).total_seconds()
    )

    device_binding_matched = _device_binding_matched(signal)

    handshake_signal_present = _handshake_signal_present(signal)

    same_transport_context_score = _same_transport_context_score(signal)

    extended_context = signal.access_context in {
        TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        TransportAccessContext.STATION_ACCESS_WAIT,
        TransportAccessContext.TERMINAL_WAIT,
    }

    return {
        "elapsed_seconds": elapsed_seconds,
        "access_window_minutes": access_window_minutes,
        "access_context_window_matched": access_context_window_matched,
        "sync_moment_window_matched": sync_moment_window_matched,
        "offline_pending_window_matched": offline_pending_window_matched,
        "device_binding_matched": device_binding_matched,
        "handshake_signal_present": handshake_signal_present,
        "same_transport_context_score": same_transport_context_score,
        "extended_context": extended_context,
    }


def _risk_flags(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
) -> List[str]:
    flags: List[str] = []

    if policy.require_distinct_users and signal.priority_user_token == signal.collaborator_token:
        flags.append("same_user_token_not_allowed")

    if _looks_like_free_text(signal.priority_user_token):
        flags.append("priority_user_token_looks_like_free_text")

    if _looks_like_free_text(signal.collaborator_token):
        flags.append("collaborator_token_looks_like_free_text")

    if policy.require_user_confirmation and not signal.priority_user_confirms_sync:
        flags.append("priority_user_confirmation_required")

    if signal.collaborator_claims_unilaterally:
        flags.append("collaborator_unilateral_claim")

    if not signal.access_window_matched:
        flags.append("access_window_not_matched")

    if not signal.trip_window_matched:
        flags.append("trip_window_not_matched")

    if not metrics["access_context_window_matched"]:
        flags.append("access_context_window_expired")

    if (
        signal.access_context == TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT
        and not metrics["sync_moment_window_matched"]
    ):
        flags.append("in_vehicle_sync_moment_window_expired")

    if metrics["extended_context"]:
        if not metrics["access_context_window_matched"]:
            flags.append("extended_station_access_window_expired")

        if (
            policy.require_device_or_handshake_for_extended_context
            and not metrics["handshake_signal_present"]
            and not metrics["device_binding_matched"]
        ):
            flags.append("extended_context_requires_handshake_or_device_signal")

    if metrics["same_transport_context_score"] <= 0:
        flags.append("no_shared_transport_context")

    if signal.access_context == TransportAccessContext.UNKNOWN:
        flags.append("unknown_access_context")

    if policy.require_distinct_payment_methods:
        if (
            signal.priority_device
            and signal.collaborator_device
            and signal.priority_device.payment_method_demo_token
            == signal.collaborator_device.payment_method_demo_token
        ):
            flags.append("same_payment_method_token_not_allowed")

        if (
            signal.priority_device
            and signal.collaborator_device
            and signal.priority_device.sube_card_demo_token
            == signal.collaborator_device.sube_card_demo_token
        ):
            flags.append("same_sube_card_token_not_allowed")

    if signal.priority_device and not signal.priority_device.device_binding_active:
        flags.append("priority_device_binding_inactive")

    if signal.collaborator_device and not signal.collaborator_device.device_binding_active:
        flags.append("collaborator_device_binding_inactive")

    if signal.priority_device and not signal.priority_device.mobile_account_linked_to_payment_demo:
        flags.append("priority_mobile_not_linked_to_payment_demo")

    if signal.collaborator_device and not signal.collaborator_device.mobile_account_linked_to_payment_demo:
        flags.append("collaborator_mobile_not_linked_to_payment_demo")

    if signal.offline_mode and not policy.allow_offline_deferred_validation:
        flags.append("offline_validation_not_allowed")

    if signal.offline_mode and not metrics["offline_pending_window_matched"]:
        flags.append("offline_pending_window_expired")

    return _deduplicate(flags)


def _review_only(risk_flags: List[str]) -> bool:
    review_only_flags = {
        "extended_context_requires_handshake_or_device_signal",
        "unknown_access_context",
    }

    return bool(risk_flags) and set(risk_flags).issubset(review_only_flags)


def _offline_can_be_deferred(
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
    risk_flags: List[str],
) -> bool:
    if not policy.allow_offline_deferred_validation:
        return False

    if not metrics["offline_pending_window_matched"]:
        return False

    blocking_flags = set(risk_flags) - {
        "extended_context_requires_handshake_or_device_signal",
    }

    return not blocking_flags


def _proximity_strength(
    signal: ProximitySignal,
    metrics: Dict[str, Any],
) -> ProximityStrength:
    if not metrics["access_context_window_matched"]:
        return ProximityStrength.NONE

    if signal.access_context == TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT:
        if signal.same_vehicle_demo_id or signal.same_trainset_demo_id:
            if metrics["handshake_signal_present"] or metrics["device_binding_matched"]:
                return ProximityStrength.STRONG

    if signal.access_context in {
        TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        TransportAccessContext.STATION_ACCESS_WAIT,
        TransportAccessContext.TERMINAL_WAIT,
    }:
        if signal.same_platform_demo_id and metrics["handshake_signal_present"]:
            return ProximityStrength.STRONG

        if signal.same_station_demo_id and (
            metrics["handshake_signal_present"] or metrics["device_binding_matched"]
        ):
            return ProximityStrength.MODERATE

        if signal.same_service_window_demo_id and metrics["handshake_signal_present"]:
            return ProximityStrength.MODERATE

    if metrics["same_transport_context_score"] > 0:
        return ProximityStrength.WEAK

    return ProximityStrength.NONE


def _result(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
    status: ProximityGuardStatus,
    proximity_strength: ProximityStrength,
    proximity_accepted: bool,
    requires_deferred_validation: bool,
    risk_flags: List[str],
    reason: str,
) -> ProximityGuardResult:
    return ProximityGuardResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=GUARD_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        proximity_strength=proximity_strength,
        proximity_accepted=proximity_accepted,
        requires_deferred_validation=requires_deferred_validation,
        access_context=signal.access_context.value,
        proximity_method=signal.proximity_method.value,
        access_window_matched=signal.access_window_matched,
        trip_window_matched=signal.trip_window_matched,
        sync_moment_window_matched=metrics["sync_moment_window_matched"],
        device_binding_matched=metrics["device_binding_matched"],
        handshake_signal_present=metrics["handshake_signal_present"],
        same_transport_context_score=metrics["same_transport_context_score"],
        risk_flags=risk_flags,
        reason=reason,
        security_summary=_security_summary(signal, policy, metrics),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def _security_summary(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "sync_event_demo_id": signal.sync_event_demo_id,
        "access_context": signal.access_context.value,
        "proximity_method": signal.proximity_method.value,
        "elapsed_seconds": metrics["elapsed_seconds"],
        "access_window_minutes": metrics["access_window_minutes"],
        "sync_moment_proximity_window_minutes": policy.sync_moment_proximity_window_minutes,
        "in_vehicle_sync_window_minutes": policy.in_vehicle_sync_window_minutes,
        "station_extended_access_window_minutes": policy.station_extended_access_window_minutes,
        "same_network_demo_id": signal.same_network_demo_id,
        "same_route_demo_id": signal.same_route_demo_id,
        "same_station_demo_id": signal.same_station_demo_id,
        "same_platform_demo_id": signal.same_platform_demo_id,
        "same_vehicle_demo_id": signal.same_vehicle_demo_id,
        "same_trainset_demo_id": signal.same_trainset_demo_id,
        "same_service_window_demo_id": signal.same_service_window_demo_id,
        "offline_mode": signal.offline_mode,
    }


def _device_binding_matched(signal: ProximitySignal) -> bool:
    if signal.priority_device is None or signal.collaborator_device is None:
        return False

    if not signal.priority_device.device_binding_active:
        return False

    if not signal.collaborator_device.device_binding_active:
        return False

    if not signal.priority_device.mobile_account_linked_to_payment_demo:
        return False

    if not signal.collaborator_device.mobile_account_linked_to_payment_demo:
        return False

    if signal.priority_device.device_session_token == signal.collaborator_device.device_session_token:
        return False

    if signal.priority_device.payment_method_demo_token == signal.collaborator_device.payment_method_demo_token:
        return False

    if signal.priority_device.sube_card_demo_token == signal.collaborator_device.sube_card_demo_token:
        return False

    return True


def _handshake_signal_present(signal: ProximitySignal) -> bool:
    if signal.proximity_method == ProximityMethod.QR_TEMPORARY_DEMO:
        return bool(signal.qr_or_code_token_demo)

    if signal.proximity_method == ProximityMethod.MANUAL_CODE_DEMO:
        return bool(signal.qr_or_code_token_demo)

    if signal.proximity_method == ProximityMethod.NFC_TEMPORARY_DEMO:
        return bool(signal.nfc_handshake_token_demo)

    if signal.proximity_method == ProximityMethod.BLE_NEARBY_DEMO:
        return bool(signal.ble_ephemeral_token_demo)

    if signal.proximity_method == ProximityMethod.SAME_DEVICE_SESSION_DEMO:
        return _device_binding_matched(signal)

    return False


def _same_transport_context_score(signal: ProximitySignal) -> int:
    score = 0

    if signal.same_network_demo_id:
        score += 1

    if signal.same_route_demo_id:
        score += 1

    if signal.same_service_window_demo_id:
        score += 1

    if signal.same_vehicle_demo_id:
        score += 2

    if signal.same_trainset_demo_id:
        score += 2

    if signal.same_station_demo_id:
        score += 1

    if signal.same_platform_demo_id:
        score += 2

    return score


def _access_window_minutes(
    access_context: TransportAccessContext,
    policy: ProximityGuardPolicy,
) -> int:
    if access_context == TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT:
        return policy.in_vehicle_sync_window_minutes

    if access_context in {
        TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        TransportAccessContext.STATION_ACCESS_WAIT,
        TransportAccessContext.TERMINAL_WAIT,
    }:
        return policy.station_extended_access_window_minutes

    return policy.in_vehicle_sync_window_minutes


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
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _deduplicate(flags: List[str]) -> List[str]:
    seen = set()
    result = []

    for flag in flags:
        if flag not in seen:
            seen.add(flag)
            result.append(flag)

    return result


def _strip_optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    stripped = value.strip()
    return stripped if stripped else None


def _privacy_notice() -> str:
    return (
        "La guardia de proximidad no revela DNI, nombre, domicilio, diagnóstico, CUD, "
        "historia clínica, certificado médico, teléfono, email ni GPS exacto. "
        "Sólo utiliza tokens demostrativos, voluntarios y temporales."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no verifica proximidad, no decide sincronizaciones, no administra "
        "beneficios y no interviene en el Bono Solidario."
    )


def _common_warnings() -> List[str]:
    return [
        "Guardia de proximidad conceptual y demostrativa.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin consulta a cuentas reales.",
        "Sin consulta a tarjetas reales.",
        "Sin datos sensibles.",
        "Sin DNI.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
        "Sin certificados médicos reales.",
        "Sin teléfono real.",
        "Sin email real.",
        "Sin geolocalización GPS exacta.",
        "Sin vigilancia.",
        "Sin ranking.",
        "Sin sanciones.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "La ventana amplia de estación no alcanza por sí sola.",
        "La proximidad debe reforzarse al momento de sincronizar.",
        "La aceptación de proximidad no acredita beneficios por sí sola.",
        "El resultado debe combinarse con handoff, antifraude y política demo de descuento.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_station_demo(), indent=2, ensure_ascii=False))

"""
SUBE Prioridad — Guardia demostrativa de proximidad móvil no excluyente.

Este módulo modela una capa de refuerzo antifraude para el Bono Solidario.

Regla central:
    La proximidad móvil NO es requisito excluyente.
    La ausencia de celular, smartphone, tablet, conectividad o app no debe impedir
    por sí sola la sincronización solidaria ni la eventual evaluación del Bono Solidario.

Finalidad:
    - reforzar la validación cuando existen señales móviles voluntarias;
    - generar registros de auditoría ante sospechas de fraude;
    - aportar contexto probatorio adicional;
    - permitir validación diferida en entornos sin conectividad;
    - evitar que la tecnología se transforme en una nueva barrera de acceso.

Este módulo NO acredita el Bono Solidario.
Este módulo NO calcula descuentos.
Este módulo NO decide beneficios tarifarios.
Este módulo NO reemplaza el handoff antifraude.
Este módulo NO reemplaza el matcher temporal Red SUBE demo.
Este módulo NO exige celular como condición prioritaria.

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

Uso esperado dentro del ecosistema:
    handoff aceptado
    + ventana temporal / contexto de viaje válido
    + confirmación del usuario SUBE Prioridad
    + asiento de uso general
    + filtros antifraude mínimos
    + proximidad móvil, si existe
    =
    evaluación posterior del Bono Solidario demo.

Si no existe proximidad móvil:
    el resultado queda registrado como "sin señal móvil disponible",
    pero no bloquea automáticamente el flujo.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Guardia Demo de Proximidad Móvil No Excluyente"
GUARD_VERSION = "0.2.0"
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
    "imei",
    "mac",
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
    """
    Política demostrativa de proximidad.

    mobile_required_for_bonus:
        Debe permanecer en False para evitar que el celular sea requisito excluyente.

    require_mobile_for_extended_context:
        Si es False, la ausencia de señal móvil en estación/andén no bloquea por sí sola.
        Sólo reduce la fuerza probatoria y deja registro de auditoría.

    enable_audit_trail:
        Permite registrar señales ausentes, débiles o reforzadas para revisión posterior.
    """

    in_vehicle_sync_window_minutes: int
    station_extended_access_window_minutes: int
    sync_moment_proximity_window_minutes: int
    mobile_required_for_bonus: bool
    require_user_confirmation: bool
    require_distinct_users: bool
    require_distinct_payment_methods: bool
    require_mobile_for_extended_context: bool
    allow_offline_deferred_validation: bool
    max_pending_offline_minutes: int
    enable_audit_trail: bool


@dataclass(frozen=True)
class MobileDeviceBindingDemo:
    """
    Vinculación demostrativa de dispositivo.

    Puede no existir.
    No contiene número de teléfono real.
    No contiene email real.
    No contiene IMEI real.
    No contiene MAC real.
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
    Señal demostrativa de proximidad.

    La señal móvil puede estar ausente sin bloquear automáticamente el flujo.
    """

    sync_event_demo_id: str
    priority_user_token: str
    collaborator_token: str
    access_context: TransportAccessContext
    proximity_method: ProximityMethod
    priority_device: Optional[MobileDeviceBindingDemo]
    collaborator_device: Optional[MobileDeviceBindingDemo]
    priority_user_has_mobile_device: bool
    collaborator_has_mobile_device: bool
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
    mobile_filter_available: bool
    mobile_filter_used: bool
    proximity_reinforced: bool
    non_exclusive_filter: bool
    blocks_solidary_bonus_flow: bool
    requires_deferred_validation: bool
    requires_audit_review: bool
    access_context: str
    proximity_method: str
    access_window_matched: bool
    trip_window_matched: bool
    sync_moment_window_matched: bool
    device_binding_matched: bool
    handshake_signal_present: bool
    same_transport_context_score: int
    hard_risk_flags: List[str]
    audit_flags: List[str]
    reason: str
    security_summary: Dict[str, Any]
    audit_record_demo: Dict[str, Any]
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
    mobile_required_for_bonus: bool = False,
    require_user_confirmation: bool = True,
    require_distinct_users: bool = True,
    require_distinct_payment_methods: bool = True,
    require_mobile_for_extended_context: bool = False,
    allow_offline_deferred_validation: bool = True,
    max_pending_offline_minutes: int = 120,
    enable_audit_trail: bool = True,
) -> ProximityGuardPolicy:
    """
    Crea una política demostrativa donde el celular no es requisito excluyente.
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
        mobile_required_for_bonus=mobile_required_for_bonus,
        require_user_confirmation=require_user_confirmation,
        require_distinct_users=require_distinct_users,
        require_distinct_payment_methods=require_distinct_payment_methods,
        require_mobile_for_extended_context=require_mobile_for_extended_context,
        allow_offline_deferred_validation=allow_offline_deferred_validation,
        max_pending_offline_minutes=max_pending_offline_minutes,
        enable_audit_trail=enable_audit_trail,
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
    priority_user_has_mobile_device: bool = True,
    collaborator_has_mobile_device: bool = True,
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

    Si alguna de las partes no tiene dispositivo móvil, no se crea binding móvil
    para esa parte y el resultado se tratará como señal no disponible, no como
    fraude automático.
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

    default_priority_device = (
        create_demo_mobile_device_binding(
            device_session_token="demo-priority-device-session-001",
            account_demo_token="demo-priority-account-001",
            payment_method_demo_token="demo-priority-payment-001",
            sube_card_demo_token="demo-priority-sube-card-001",
        )
        if priority_user_has_mobile_device
        else None
    )

    default_collaborator_device = (
        create_demo_mobile_device_binding(
            device_session_token="demo-collaborator-device-session-001",
            account_demo_token="demo-collaborator-account-001",
            payment_method_demo_token="demo-collaborator-payment-001",
            sube_card_demo_token="demo-collaborator-sube-card-001",
        )
        if collaborator_has_mobile_device
        else None
    )

    normalized_method = proximity_method

    if not priority_user_has_mobile_device or not collaborator_has_mobile_device:
        normalized_method = ProximityMethod.NONE_AVAILABLE

    return ProximitySignal(
        sync_event_demo_id=sync_event_demo_id.strip(),
        priority_user_token=priority_user_token.strip(),
        collaborator_token=collaborator_token.strip(),
        access_context=access_context,
        proximity_method=normalized_method,
        priority_device=priority_device if priority_device is not None else default_priority_device,
        collaborator_device=collaborator_device
        if collaborator_device is not None
        else default_collaborator_device,
        priority_user_has_mobile_device=priority_user_has_mobile_device,
        collaborator_has_mobile_device=collaborator_has_mobile_device,
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
    Caso demo de tren/subte con señal móvil disponible.
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


def create_demo_no_mobile_proximity_signal(
    created_at_utc: Optional[datetime] = None,
) -> ProximitySignal:
    """
    Caso demo donde una o ambas personas no cuentan con teléfono móvil.

    Debe quedar registrado para auditoría, pero no bloquear automáticamente
    la evaluación del Bono Solidario.
    """
    timestamp = created_at_utc or datetime.now(timezone.utc)

    return create_demo_proximity_signal(
        sync_event_demo_id="demo-no-mobile-proximity-sync-001",
        access_context=TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        proximity_method=ProximityMethod.NONE_AVAILABLE,
        priority_user_has_mobile_device=False,
        collaborator_has_mobile_device=True,
        qr_or_code_token_demo=None,
        nfc_handshake_token_demo=None,
        ble_ephemeral_token_demo=None,
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
        sync_attempted_at_utc=timestamp + timedelta(minutes=40),
    )


def evaluate_mobile_proximity_sync_guard(
    signal: ProximitySignal,
    policy: Optional[ProximityGuardPolicy] = None,
) -> ProximityGuardResult:
    """
    Evalúa la señal móvil como refuerzo no excluyente.

    Sólo bloquea cuando aparecen riesgos duros:
        - mismo usuario;
        - mismo medio de pago cuando debe ser distinto;
        - reclamo unilateral del colaborador;
        - falta de confirmación del usuario SUBE Prioridad;
        - ausencia de ventana temporal mínima;
        - ausencia total de contexto compartido.

    La falta de celular no bloquea automáticamente.
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
    hard_risk_flags = _hard_risk_flags(signal, policy, metrics)
    audit_flags = _audit_flags(signal, policy, metrics)
    strength = _proximity_strength(signal, metrics)

    if signal.offline_mode and _offline_can_be_deferred(policy, metrics, hard_risk_flags):
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.DEFERRED_OFFLINE_VALIDATION,
            proximity_strength=strength,
            proximity_reinforced=False,
            blocks_solidary_bonus_flow=False,
            requires_deferred_validation=True,
            requires_audit_review=True,
            hard_risk_flags=[],
            audit_flags=_deduplicate(audit_flags + ["offline_validation_pending"]),
            reason=(
                "La señal móvil se registró en modo offline. No bloquea por sí sola, "
                "pero requiere validación diferida y queda registrada para auditoría."
            ),
        )

    if hard_risk_flags:
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.REJECTED_HARD_RISK,
            proximity_strength=strength,
            proximity_reinforced=False,
            blocks_solidary_bonus_flow=True,
            requires_deferred_validation=False,
            requires_audit_review=True,
            hard_risk_flags=hard_risk_flags,
            audit_flags=audit_flags,
            reason=(
                "La guardia detectó riesgos duros. En este caso el filtro sí bloquea "
                "el avance porque no se trata de simple ausencia de celular."
            ),
        )

    if metrics["mobile_filter_available"] and metrics["mobile_filter_used"]:
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.ACCEPTED_REINFORCED,
            proximity_strength=strength,
            proximity_reinforced=True,
            blocks_solidary_bonus_flow=False,
            requires_deferred_validation=False,
            requires_audit_review=bool(audit_flags),
            hard_risk_flags=[],
            audit_flags=audit_flags,
            reason=(
                "La proximidad móvil actúa como refuerzo positivo no excluyente. "
                "Aporta evidencia adicional, pero no acredita el Bono Solidario por sí sola."
            ),
        )

    if audit_flags:
        return _result(
            signal=signal,
            policy=policy,
            metrics=metrics,
            status=ProximityGuardStatus.ACCEPTED_WITHOUT_MOBILE_EVIDENCE,
            proximity_strength=ProximityStrength.NOT_AVAILABLE,
            proximity_reinforced=False,
            blocks_solidary_bonus_flow=False,
            requires_deferred_validation=False,
            requires_audit_review=True,
            hard_risk_flags=[],
            audit_flags=audit_flags,
            reason=(
                "No existe señal móvil suficiente. La ausencia de celular o app no bloquea "
                "automáticamente la sincronización, pero queda registrada como menor fuerza "
                "probatoria para auditoría antifraude."
            ),
        )

    return _result(
        signal=signal,
        policy=policy,
        metrics=metrics,
        status=ProximityGuardStatus.ACCEPTED_WITHOUT_MOBILE_EVIDENCE,
        proximity_strength=ProximityStrength.NOT_AVAILABLE,
        proximity_reinforced=False,
        blocks_solidary_bonus_flow=False,
        requires_deferred_validation=False,
        requires_audit_review=False,
        hard_risk_flags=[],
        audit_flags=[],
        reason=(
            "No se usó proximidad móvil. El filtro es no excluyente y no bloquea "
            "el flujo del Bono Solidario demo."
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
        "mobile_filter_available": result.mobile_filter_available,
        "mobile_filter_used": result.mobile_filter_used,
        "proximity_reinforced": result.proximity_reinforced,
        "non_exclusive_filter": result.non_exclusive_filter,
        "blocks_solidary_bonus_flow": result.blocks_solidary_bonus_flow,
        "requires_deferred_validation": result.requires_deferred_validation,
        "requires_audit_review": result.requires_audit_review,
        "access_context": result.access_context,
        "proximity_method": result.proximity_method,
        "access_window_matched": result.access_window_matched,
        "trip_window_matched": result.trip_window_matched,
        "sync_moment_window_matched": result.sync_moment_window_matched,
        "device_binding_matched": result.device_binding_matched,
        "handshake_signal_present": result.handshake_signal_present,
        "same_transport_context_score": result.same_transport_context_score,
        "hard_risk_flags": result.hard_risk_flags,
        "audit_flags": result.audit_flags,
        "reason": result.reason,
        "security_summary": result.security_summary,
        "audit_record_demo": result.audit_record_demo,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Demo estable con señal móvil disponible.
    """
    signal = create_demo_proximity_signal()

    result = evaluate_mobile_proximity_sync_guard(signal)

    return result_to_dict(result)


def run_station_demo() -> Dict[str, Any]:
    """
    Demo estable de estación/andén con BLE.
    """
    signal = create_demo_station_extended_proximity_signal()

    result = evaluate_mobile_proximity_sync_guard(signal)

    return result_to_dict(result)


def run_no_mobile_demo() -> Dict[str, Any]:
    """
    Demo estable sin celular disponible para una de las partes.

    Debe aceptar sin refuerzo móvil y registrar auditoría.
    """
    signal = create_demo_no_mobile_proximity_signal()

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

    mobile_filter_available = (
        signal.priority_user_has_mobile_device
        and signal.collaborator_has_mobile_device
    )

    mobile_filter_used = mobile_filter_available and (
        device_binding_matched or handshake_signal_present
    )

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
        "mobile_filter_available": mobile_filter_available,
        "mobile_filter_used": mobile_filter_used,
        "extended_context": extended_context,
    }


def _hard_risk_flags(
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

    if signal.offline_mode and not policy.allow_offline_deferred_validation:
        flags.append("offline_validation_not_allowed")

    if signal.offline_mode and not metrics["offline_pending_window_matched"]:
        flags.append("offline_pending_window_expired")

    if policy.mobile_required_for_bonus and not metrics["mobile_filter_used"]:
        flags.append("mobile_required_by_policy_but_not_available")

    if (
        policy.require_mobile_for_extended_context
        and metrics["extended_context"]
        and not metrics["mobile_filter_used"]
    ):
        flags.append("extended_context_mobile_required_by_policy")

    return _deduplicate(flags)


def _audit_flags(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
) -> List[str]:
    if not policy.enable_audit_trail:
        return []

    flags: List[str] = []

    if not signal.priority_user_has_mobile_device:
        flags.append("priority_user_mobile_not_available_non_blocking")

    if not signal.collaborator_has_mobile_device:
        flags.append("collaborator_mobile_not_available_non_blocking")

    if not metrics["mobile_filter_available"]:
        flags.append("mobile_filter_not_available_non_blocking")

    if metrics["mobile_filter_available"] and not metrics["mobile_filter_used"]:
        flags.append("mobile_filter_available_but_not_used")

    if metrics["extended_context"] and not metrics["mobile_filter_used"]:
        flags.append("extended_context_without_mobile_reinforcement")

    if signal.access_context == TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE:
        flags.append("station_or_platform_context_audit")

    if signal.access_context == TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT:
        flags.append("in_vehicle_context_audit")

    if signal.offline_mode:
        flags.append("offline_mode_audit")

    if signal.priority_device and not signal.priority_device.device_binding_active:
        flags.append("priority_device_binding_inactive_audit")

    if signal.collaborator_device and not signal.collaborator_device.device_binding_active:
        flags.append("collaborator_device_binding_inactive_audit")

    if signal.priority_device and not signal.priority_device.mobile_account_linked_to_payment_demo:
        flags.append("priority_mobile_not_linked_to_payment_demo_audit")

    if signal.collaborator_device and not signal.collaborator_device.mobile_account_linked_to_payment_demo:
        flags.append("collaborator_mobile_not_linked_to_payment_demo_audit")

    return _deduplicate(flags)


def _offline_can_be_deferred(
    policy: ProximityGuardPolicy,
    metrics: Dict[str, Any],
    hard_risk_flags: List[str],
) -> bool:
    if not policy.allow_offline_deferred_validation:
        return False

    if not metrics["offline_pending_window_matched"]:
        return False

    return not hard_risk_flags


def _proximity_strength(
    signal: ProximitySignal,
    metrics: Dict[str, Any],
) -> ProximityStrength:
    if not metrics["mobile_filter_available"]:
        return ProximityStrength.NOT_AVAILABLE

    if not metrics["mobile_filter_used"]:
        return ProximityStrength.NONE

    if signal.access_context == TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT:
        if signal.same_vehicle_demo_id or signal.same_trainset_demo_id:
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
    proximity_reinforced: bool,
    blocks_solidary_bonus_flow: bool,
    requires_deferred_validation: bool,
    requires_audit_review: bool,
    hard_risk_flags: List[str],
    audit_flags: List[str],
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
        proximity_reinforced=proximity_reinforced,
        non_exclusive_filter=True,
        blocks_solidary_bonus_flow=blocks_solidary_bonus_flow,
        requires_deferred_validation=requires_deferred_validation,
        requires_audit_review=requires_audit_review,
        access_context=signal.access_context.value,
        proximity_method=signal.proximity_method.value,
        access_window_matched=signal.access_window_matched,
        trip_window_matched=signal.trip_window_matched,
        sync_moment_window_matched=metrics["sync_moment_window_matched"],
        device_binding_matched=metrics["device_binding_matched"],
        handshake_signal_present=metrics["handshake_signal_present"],
        same_transport_context_score=metrics["same_transport_context_score"],
        hard_risk_flags=hard_risk_flags,
        audit_flags=audit_flags,
        reason=reason,
        security_summary=_security_summary(signal, policy, metrics),
        audit_record_demo=_audit_record_demo(signal, metrics, hard_risk_flags, audit_flags),
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
        "mobile_required_for_bonus": policy.mobile_required_for_bonus,
        "require_mobile_for_extended_context": policy.require_mobile_for_extended_context,
        "mobile_filter_available": metrics["mobile_filter_available"],
        "mobile_filter_used": metrics["mobile_filter_used"],
        "same_network_demo_id": signal.same_network_demo_id,
        "same_route_demo_id": signal.same_route_demo_id,
        "same_station_demo_id": signal.same_station_demo_id,
        "same_platform_demo_id": signal.same_platform_demo_id,
        "same_vehicle_demo_id": signal.same_vehicle_demo_id,
        "same_trainset_demo_id": signal.same_trainset_demo_id,
        "same_service_window_demo_id": signal.same_service_window_demo_id,
        "offline_mode": signal.offline_mode,
    }


def _audit_record_demo(
    signal: ProximitySignal,
    metrics: Dict[str, Any],
    hard_risk_flags: List[str],
    audit_flags: List[str],
) -> Dict[str, Any]:
    """
    Registro demostrativo de auditoría.

    No contiene datos personales.
    No contiene diagnóstico.
    No contiene GPS.
    No contiene teléfono.
    """
    return {
        "sync_event_demo_id": signal.sync_event_demo_id,
        "mobile_filter_available": metrics["mobile_filter_available"],
        "mobile_filter_used": metrics["mobile_filter_used"],
        "proximity_method": signal.proximity_method.value,
        "access_context": signal.access_context.value,
        "same_transport_context_score": metrics["same_transport_context_score"],
        "hard_risk_flags": hard_risk_flags,
        "audit_flags": audit_flags,
        "audit_purpose": (
            "Registro no sensible para revisión antifraude ante patrones anómalos "
            "o sospechas posteriores."
        ),
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
        "historia clínica, certificado médico, teléfono, email, IMEI, MAC ni GPS exacto. "
        "La ausencia de celular no bloquea automáticamente el flujo."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no verifica proximidad, no decide sincronizaciones, no administra "
        "beneficios y no interviene en el Bono Solidario."
    )


def _common_warnings() -> List[str]:
    return [
        "Guardia de proximidad conceptual y demostrativa.",
        "Filtro móvil no excluyente.",
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
        "Sin IMEI real.",
        "Sin MAC real.",
        "Sin geolocalización GPS exacta.",
        "Sin vigilancia.",
        "Sin ranking.",
        "Sin sanciones.",
        "Sin obligación de tener celular.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "La proximidad móvil refuerza, pero no reemplaza los demás filtros.",
        "La ausencia de señal móvil puede registrarse para auditoría sin bloquear automáticamente.",
        "La aceptación de proximidad no acredita beneficios por sí sola.",
        "El resultado debe combinarse con handoff, matcher temporal, antifraude y política demo de descuento.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_station_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_no_mobile_demo(), indent=2, ensure_ascii=False))

"""
SUBE Prioridad — Selector demo de canales de sincronización solidaria.
Este módulo resuelve un punto central del ecosistema:
 Ni el usuario SUBE Prioridad ni el colaborador deben estar obligados
 a tener celular, NFC, Android, iOS, tablet, app o conectividad propia.

No representa implementación oficial.
No integra SUBE real. No integra Red SUBE real.
No procesa DNI, nombre, domicilio, diagnóstico ni CUD de pasajeros.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Selector Demo de Canales de Sincronización Solidaria"
MODULE_VERSION = "0.1.0"
DEMO_MODE = True

PROHIBITED_FIELDS = {
    "dni", "documento", "nombre", "apellido", "domicilio", "direccion", "dirección",
    "telefono", "teléfono", "phone", "email", "correo", "diagnostico", "diagnóstico",
    "historia_clinica", "historia_clínica", "certificado_medico", "certificado_médico",
    "cud", "discapacidad", "patologia", "patología", "medico", "médico", "obra_social",
    "gps", "latitud", "longitud", "latitude", "longitude", "imei", "mac", "saldo", "dinero"
}

class SyncChannelStatus(str, Enum):
    READY_REINFORCED = "ready_reinforced"
    READY_WITHOUT_MOBILE = "ready_without_mobile"
    READY_DEFERRED_CONFIRMATION = "ready_deferred_confirmation"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"

class SyncChannel(str, Enum):
    NOTE_MOBILE_NFC_CARD_TAP = "priority_mobile_nfc_card_tap"
    PRIORITY_MOBILE_NFC_CARD_TAP = "priority_mobile_nfc_card_tap"
    COLLABORATOR_MOBILE_QR_OR_CODE = "collaborator_mobile_qr_or_code"
    VALIDATOR_CONTEXT_WINDOW = "validator_context_window"
    TURNSTILE_OR_STATION_WINDOW = "turnstile_or_station_window"
    ASSISTED_STATION_OR_TERMINAL_CHANNEL = "assisted_station_or_terminal_channel"
    ACCOUNT_DEFERRED_CONFIRMATION = "account_deferred_confirmation"
    NO_CHANNEL_AVAILABLE = "no_channel_available"

class TransportMode(str, Enum):
    BUS = "bus"
    TRAIN = "train"
    SUBWAY = "subway"
    COASTAL_TRAIN_OR_ONBOARD_VALIDATOR = "coastal_train_or_onboard_validator"
    OTHER_PUBLIC_TRANSPORT = "other_public_transport"

class ValidationPointType(str, Enum):
    VEHICLE_VALIDATOR = "vehicle_validator"
    ONBOARD_TRAIN_VALIDATOR = "onboard_train_validator"
    STATION_TURNSTILE = "station_turnstile"
    STATION_ACCESS_GATE = "station_access_gate"
    TERMINAL_VALIDATOR = "terminal_validator"
    UNKNOWN = "unknown"

class ConfirmationMode(str, Enum):
    IMMEDIATE_PRIORITY_CONFIRMATION = "immediate_priority_confirmation"
    ASSISTED_CONFIRMATION = "assisted_confirmation"
    DEFERRED_ACCOUNT_CONFIRMATION = "deferred_account_confirmation"
    VALIDATOR_WINDOW_PENDING_CONFIRMATION = "validator_window_pending_confirmation"
    MISSING = "missing"

class WindowKind(str, Enum):
    IN_VEHICLE_SHORT_WINDOW = "in_vehicle_short_window"
    ONBOARD_TRAIN_SHORT_WINDOW = "onboard_train_short_window"
    STATION_EXTENDED_WINDOW = "station_extended_window"
    TERMINAL_EXTENDED_WINDOW = "terminal_extended_window"
    DEFERRED_ACCOUNT_WINDOW = "deferred_account_window"
    UNKNOWN_WINDOW = "unknown_window"

@dataclass(frozen=True)
class SyncChannelPolicy:
    in_vehicle_window_minutes: int
    onboard_train_window_minutes: int
    station_window_minutes: int
    terminal_window_minutes: int
    deferred_confirmation_window_hours: int
    require_priority_attribute_active: bool
    require_priority_need_previously_accredited: bool
    require_priority_paid_validation: bool
    require_collaborator_paid_validation: bool
    require_priority_confirmation: bool
    allow_no_mobile_channels: bool
    allow_assisted_channel: bool
    allow_deferred_account_confirmation: bool
    max_context_score_for_ready_without_mobile: int

@dataclass(frozen=True)
class UserDeviceAvailability:
    has_mobile_device: bool
    has_nfc_capable_device: bool
    has_app_or_account_access_now: bool
    has_connectivity_now: bool
    has_physical_sube_card: bool

@dataclass(frozen=True)
class RedSubeValidationContext:
    network_demo_id: str
    route_demo_id: str
    service_window_demo_id: str
    validator_or_turnstile_demo_id: str
    vehicle_demo_id: Optional[str]
    trainset_demo_id: Optional[str]
    station_demo_id: Optional[str]
    platform_demo_id: Optional[str]
    transport_mode: TransportMode
    validation_point_type: ValidationPointType
    priority_paid_validation_confirmed: bool
    collaborator_paid_validation_confirmed: bool
    priority_validation_timestamp_utc: datetime
    collaborator_validation_timestamp_utc: datetime
    sync_attempt_timestamp_utc: datetime
@dataclass(frozen=True)
class SolidarySyncChannelRequest:
    sync_channel_event_demo_id: str
    priority_user_token: str
    priority_attribute_token: str
    collaborator_user_token: str
    priority_user_has_active_attribute: bool
    priority_need_previously_accredited: bool
    priority_device_availability: UserDeviceAvailability
    collaborator_device_availability: UserDeviceAvailability
    red_sube_context: RedSubeValidationContext
    confirmation_mode: ConfirmationMode
    priority_user_confirms_or_can_confirm: bool
    voluntary_seat_yield_declared: bool
    collaborator_claims_unilaterally: bool
    same_network_demo_id: bool
    same_route_demo_id: bool
    same_service_window_demo_id: bool
    same_validator_or_turnstile_demo_id: bool
    same_vehicle_demo_id: bool
    same_trainset_demo_id: bool
    same_station_demo_id: bool
    same_platform_demo_id: bool
    previous_handoff_security_accepted: bool
    previous_proximity_guard_blocks_flow: bool

@dataclass(frozen=True)
class SolidarySyncChannelResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: SyncChannelStatus
    selected_channel: SyncChannel
    window_kind: WindowKind
    window_minutes: int
    window_matched: bool
    mobile_required: bool
    priority_mobile_available: bool
    collaborator_mobile_available: bool
    no_mobile_path_supported: bool
    context_score: int
    opens_bonus_evaluation_window: bool
    blocks_solidary_bonus_flow: bool
    requires_audit_review: bool
    hard_risk_flags: List[str]
    audit_flags: List[str]
    reason: str
    security_summary: Dict[str, Any]
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

def create_demo_sync_channel_policy(
    in_vehicle_window_minutes: int = 10,
    onboard_train_window_minutes: int = 10,
    station_window_minutes: int = 60,
    terminal_window_minutes: int = 60,
    deferred_confirmation_window_hours: int = 24,
    require_priority_attribute_active: bool = True,
    require_priority_need_previously_accredited: bool = True,
    require_priority_paid_validation: bool = True,
    require_collaborator_paid_validation: bool = True,
    require_priority_confirmation: bool = True,
    allow_no_mobile_channels: bool = True,
    allow_assisted_channel: bool = True,
    allow_deferred_account_confirmation: bool = True,
    max_context_score_for_ready_without_mobile: int = 4,
) -> SyncChannelPolicy:
    if in_vehicle_window_minutes <= 0: raise ValueError("La ventana a bordo debe ser mayor a cero.")
    if onboard_train_window_minutes <= 0: raise ValueError("La ventana de tren con validadora a bordo debe ser mayor a cero.")
    if station_window_minutes <= 0: raise ValueError("La ventana de estación debe ser mayor a cero.")
    if terminal_window_minutes <= 0: raise ValueError("La ventana de terminal debe ser mayor a cero.")
    if deferred_confirmation_window_hours <= 0: raise ValueError("La ventana diferida debe ser mayor a cero.")
    if max_context_score_for_ready_without_mobile <= 0: raise ValueError("El puntaje mínimo contextual debe ser mayor a cero.")
    return SyncChannelPolicy(
        in_vehicle_window_minutes=in_vehicle_window_minutes, onboard_train_window_minutes=onboard_train_window_minutes,
        station_window_minutes=station_window_minutes, terminal_window_minutes=terminal_window_minutes,
        deferred_confirmation_window_hours=deferred_confirmation_window_hours, require_priority_attribute_active=require_priority_attribute_active,
        require_priority_need_previously_accredited=require_priority_need_previously_accredited, require_priority_paid_validation=require_priority_paid_validation,
        require_collaborator_paid_validation=require_collaborator_paid_validation, require_priority_confirmation=require_priority_confirmation,
        allow_no_mobile_channels=allow_no_mobile_channels, allow_assisted_channel=allow_assisted_channel,
        allow_deferred_account_confirmation=allow_deferred_account_confirmation, max_context_score_for_ready_without_mobile=max_context_score_for_ready_without_mobile,
    )

def create_demo_user_device_availability(has_mobile_device: bool = True, has_nfc_capable_device: bool = True, has_app_or_account_access_now: bool = True, has_connectivity_now: bool = True, has_physical_sube_card: bool = True) -> UserDeviceAvailability:
    return UserDeviceAvailability(has_mobile_device=has_mobile_device, has_nfc_capable_device=has_nfc_capable_device, has_app_or_account_access_now=has_app_or_account_access_now, has_connectivity_now=has_connectivity_now, has_physical_sube_card=has_physical_sube_card)

def create_demo_red_sube_validation_context(network_demo_id: str = "demo-red-sube-network-001", route_demo_id: str = "demo-route-001", service_window_demo_id: str = "demo-service-window-001", validator_or_turnstile_demo_id: str = "demo-validator-001", vehicle_demo_id: Optional[str] = "demo-vehicle-001", trainset_demo_id: Optional[str] = None, station_demo_id: Optional[str] = None, platform_demo_id: Optional[str] = None, transport_mode: TransportMode = TransportMode.BUS, validation_point_type: ValidationPointType = ValidationPointType.VEHICLE_VALIDATOR, priority_paid_validation_confirmed: bool = True, collaborator_paid_validation_confirmed: bool = True, priority_validation_timestamp_utc: Optional[datetime] = None, collaborator_validation_timestamp_utc: Optional[datetime] = None, sync_attempt_timestamp_utc: Optional[datetime] = None) -> RedSubeValidationContext:
    required_values = {"network_demo_id": network_demo_id, "route_demo_id": route_demo_id, "service_window_demo_id": service_window_demo_id, "validator_or_turnstile_demo_id": validator_or_turnstile_demo_id}
    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)
    now = priority_validation_timestamp_utc or datetime.now(timezone.utc)
    return RedSubeValidationContext(
        network_demo_id=network_demo_id.strip(), route_demo_id=route_demo_id.strip(), service_window_demo_id=service_window_demo_id.strip(), validator_or_turnstile_demo_id=validator_or_turnstile_demo_id.strip(),
        vehicle_demo_id=_strip_optional(vehicle_demo_id), trainset_demo_id=_strip_optional(trainset_demo_id), station_demo_id=_strip_optional(station_demo_id), platform_demo_id=_strip_optional(platform_demo_id),
        transport_mode=transport_mode, validation_point_type=validation_point_type, priority_paid_validation_confirmed=priority_paid_validation_confirmed, collaborator_paid_validation_confirmed=collaborator_paid_validation_confirmed, priority_validation_timestamp_utc=now,
        collaborator_validation_timestamp_utc=collaborator_validation_timestamp_utc or now + timedelta(minutes=1), sync_attempt_timestamp_utc=sync_attempt_timestamp_utc or now + timedelta(minutes=3),
    )

def create_demo_solidary_sync_channel_request(sync_channel_event_demo_id: str = "demo-sync-channel-001", priority_user_token: str = "demo-priority-user-001", priority_attribute_token: str = "demo-priority-attribute-001", collaborator_user_token: str = "demo-collaborator-user-001", priority_user_has_active_attribute: bool = True, priority_need_previously_accredited: bool = True, priority_device_availability: Optional[UserDeviceAvailability] = None, collaborator_device_availability: Optional[UserDeviceAvailability] = None, red_sube_context: Optional[RedSubeValidationContext] = None, confirmation_mode: ConfirmationMode = ConfirmationMode.IMMEDIATE_PRIORITY_CONFIRMATION, priority_user_confirms_or_can_confirm: bool = True, voluntary_seat_yield_declared: bool = True, collaborator_claims_unilaterally: bool = False, same_network_demo_id: bool = True, same_route_demo_id: bool = True, same_service_window_demo_id: bool = True, same_validator_or_turnstile_demo_id: bool = True, same_vehicle_demo_id: bool = True, same_trainset_demo_id: bool = False, same_station_demo_id: bool = False, same_platform_demo_id: bool = False, previous_handoff_security_accepted: bool = True, previous_proximity_guard_blocks_flow: bool = False) -> SolidarySyncChannelRequest:
    required_values = {"sync_channel_event_demo_id": sync_channel_event_demo_id, "priority_user_token": priority_user_token, "priority_attribute_token": priority_attribute_token, "collaborator_user_token": collaborator_user_token}
    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)
    return SolidarySyncChannelRequest(
        sync_channel_event_demo_id=sync_channel_event_demo_id.strip(), priority_user_token=priority_user_token.strip(), priority_attribute_token=priority_attribute_token.strip(), collaborator_user_token=collaborator_user_token.strip(),
        priority_user_has_active_attribute=priority_user_has_active_attribute, priority_need_previously_accredited=priority_need_previously_accredited,
        priority_device_availability=priority_device_availability or create_demo_user_device_availability(), collaborator_device_availability=collaborator_device_availability or create_demo_user_device_availability(has_mobile_device=False, has_nfc_capable_device=False),
        red_sube_context=red_sube_context or create_demo_red_sube_validation_context(), confirmation_mode=confirmation_mode, priority_user_confirms_or_can_confirm=priority_user_confirms_or_can_confirm,
        voluntary_seat_yield_declared=voluntary_seat_yield_declared,
        collaborator_claims_unilaterally=collaborator_claims_unilaterally,
        same_network_demo_id=same_network_demo_id,
        same_route_demo_id=same_route_demo_id,
        same_service_window_demo_id=same_service_window_demo_id,
        same_validator_or_turnstile_demo_id=same_validator_or_turnstile_demo_id,
        same_vehicle_demo_id=same_vehicle_demo_id,
        same_trainset_demo_id=same_trainset_demo_id,
        same_station_demo_id=same_station_demo_id,
        same_platform_demo_id=same_platform_demo_id,
        previous_handoff_security_accepted=previous_handoff_security_accepted,
        previous_proximity_guard_blocks_flow=previous_proximity_guard_blocks_flow,
    )

def create_demo_no_mobile_validator_based_request(created_at_utc: Optional[datetime] = None) -> SolidarySyncChannelRequest:
    timestamp = created_at_utc or datetime.now(timezone.utc)
    context = create_demo_red_sube_validation_context(transport_mode=TransportMode.BUS, validation_point_type=ValidationPointType.VEHICLE_VALIDATOR, vehicle_demo_id="demo-bus-vehicle-001", priority_validation_timestamp_utc=timestamp, collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1), sync_attempt_timestamp_utc=timestamp + timedelta(minutes=5))
    return create_demo_solidary_sync_channel_request(sync_channel_event_demo_id="demo-no-mobile-validator-sync-001", priority_device_availability=create_demo_user_device_availability(has_mobile_device=False, has_nfc_capable_device=False, has_app_or_account_access_now=False, has_connectivity_now=False, has_physical_sube_card=True), collaborator_device_availability=create_demo_user_device_availability(has_mobile_device=False, has_nfc_capable_device=False, has_app_or_account_access_now=False, has_connectivity_now=False, has_physical_sube_card=True), red_sube_context=context, confirmation_mode=ConfirmationMode.VALIDATOR_WINDOW_PENDING_CONFIRMATION, priority_user_confirms_or_can_confirm=True, same_vehicle_demo_id=True, same_validator_or_turnstile_demo_id=True)

def create_demo_station_no_mobile_deferred_request(created_at_utc: Optional[datetime] = None) -> SolidarySyncChannelRequest:
    timestamp = created_at_utc or datetime.now(timezone.utc)
    context = create_demo_red_sube_validation_context(transport_mode=TransportMode.SUBWAY, validation_point_type=ValidationPointType.STATION_TURNSTILE, validator_or_turnstile_demo_id="demo-turnstile-001", vehicle_demo_id=None, trainset_demo_id=None, station_demo_id="demo-station-001", platform_demo_id="demo-platform-001", priority_validation_timestamp_utc=timestamp, collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=8), sync_attempt_timestamp_utc=timestamp + timedelta(minutes=45))
    return create_demo_solidary_sync_channel_request(sync_channel_event_demo_id="demo-station-no-mobile-deferred-sync-001", priority_device_availability=create_demo_user_device_availability(has_mobile_device=False, has_nfc_capable_device=False, has_app_or_account_access_now=False, has_connectivity_now=False, has_physical_sube_card=True), collaborator_device_availability=create_demo_user_device_availability(has_mobile_device=False, has_nfc_capable_device=False, has_app_or_account_access_now=False, has_connectivity_now=False, has_physical_sube_card=True), red_sube_context=context, confirmation_mode=ConfirmationMode.DEFERRED_ACCOUNT_CONFIRMATION, priority_user_confirms_or_can_confirm=True, same_vehicle_demo_id=False, same_validator_or_turnstile_demo_id=True, same_station_demo_id=True, same_platform_demo_id=True)

def evaluate_solidary_sync_channel(request: SolidarySyncChannelRequest, policy: Optional[SyncChannelPolicy] = None) -> SolidarySyncChannelResult:
    policy = policy or create_demo_sync_channel_policy()
    assert_no_prohibited_fields({"sync_channel_event_demo_id": request.sync_channel_event_demo_id, "priority_user_token": request.priority_user_token, "priority_attribute_token": request.priority_attribute_token, "collaborator_user_token": request.collaborator_user_token})
    window_kind = _window_kind(request.red_sube_context)
    window_minutes = _window_minutes(window_kind, policy)
    window_matched = _window_matched(request.red_sube_context, window_minutes)
    context_score = _context_score(request)
    selected_channel = _select_channel(request, policy, window_matched, context_score)
    hard_risk_flags = _hard_risk_flags(request, policy, window_matched, context_score)
    audit_flags = _audit_flags(request, policy, selected_channel, window_kind, context_score)
    if hard_risk_flags:
        return _result(request=request, policy=policy, status=SyncChannelStatus.REJECTED, selected_channel=selected_channel, window_kind=window_kind, window_minutes=window_minutes, window_matched=window_matched, context_score=context_score, opens_bonus_evaluation_window=False, blocks_solidary_bonus_flow=True, requires_audit_review=True, hard_risk_flags=hard_risk_flags, audit_flags=audit_flags, reason="No se abre ventana de evaluación porque existen riesgos duros o faltan condiciones mínimas de validación Red SUBE demo.")
    if selected_channel in {SyncChannel.ACCOUNT_DEFERRED_CONFIRMATION, SyncChannel.ASSISTED_STATION_OR_TERMINAL_CHANNEL}:
        return _result(request=request, policy=policy, status=SyncChannelStatus.READY_DEFERRED_CONFIRMATION, selected_channel=selected_channel, window_kind=window_kind, window_minutes=window_minutes, window_matched=window_matched, context_score=context_score, opens_bonus_evaluation_window=True, blocks_solidary_bonus_flow=False, requires_audit_review=True, hard_risk_flags=[], audit_flags=audit_flags, reason="Se abre una ventana de evaluación con confirmación diferida o asistida. La ausencia de celular no bloquea, pero aumenta la necesidad de auditoría.")
    if selected_channel in {SyncChannel.VALIDATOR_CONTEXT_WINDOW, SyncChannel.TURNSTILE_OR_STATION_WINDOW}:
        return _result(request=request, policy=policy, status=SyncChannelStatus.READY_WITHOUT_MOBILE, selected_channel=selected_channel, window_kind=window_kind, window_minutes=window_minutes, window_matched=window_matched, context_score=context_score, opens_bonus_evaluation_window=True, blocks_solidary_bonus_flow=False, requires_audit_review=True, hard_risk_flags=[], audit_flags=audit_flags, reason="Se abre una ventana contextual desde validadora o molinete. No se exige celular; el canal queda registrado para auditoría antifraude.")
    return _result(request=request, policy=policy, status=SyncChannelStatus.READY_REINFORCED, selected_channel=selected_channel, window_kind=window_kind, window_minutes=window_minutes, window_matched=window_matched, context_score=context_score, opens_bonus_evaluation_window=True, blocks_solidary_bonus_flow=False, requires_audit_review=bool(audit_flags), hard_risk_flags=[], audit_flags=audit_flags, reason="Se seleccionó un canal de sincronización reforzado por dispositivo, sin excluir las alternativas Red SUBE.")

def result_to_dict(result: SolidarySyncChannelResult) -> Dict[str, Any]:
    return {"project": result.project, "module": result.module, "version": result.version, "demo_mode": result.demo_mode, "status": result.status.value, "selected_channel": result.selected_channel.value, "window_kind": result.window_kind.value, "window_minutes": result.window_minutes, "window_matched": result.window_matched, "mobile_required": result.mobile_required, "priority_mobile_available": result.priority_mobile_available, "collaborator_mobile_available": result.collaborator_mobile_available, "no_mobile_path_supported": result.no_mobile_path_supported, "context_score": result.context_score, "opens_bonus_evaluation_window": result.opens_bonus_evaluation_window, "blocks_solidary_bonus_flow": result.blocks_solidary_bonus_flow, "requires_audit_review": result.requires_audit_review, "hard_risk_flags": result.hard_risk_flags, "audit_flags": result.audit_flags, "reason": result.reason, "privacy_notice": result.privacy_notice, "legal_scope_notice": result.legal_scope_notice, "driver_burden": result.driver_burden, "warnings": result.warnings, "timestamp_utc": result.timestamp_utc}

def run_demo() -> Dict[str, Any]: return result_to_dict(evaluate_solidary_sync_channel(create_demo_solidary_sync_channel_request()))
def run_no_mobile_validator_demo() -> Dict[str, Any]: return result_to_dict(evaluate_solidary_sync_channel(create_demo_no_mobile_validator_based_request()))
def run_station_no_mobile_deferred_demo() -> Dict[str, Any]: return result_to_dict(evaluate_solidary_sync_channel(create_demo_station_no_mobile_deferred_request()))

def _select_channel(request: SolidarySyncChannelRequest, policy: SyncChannelPolicy, window_matched: bool, context_score: int) -> SyncChannel:
    priority_device = request.priority_device_availability; collaborator_device = request.collaborator_device_availability; validation_point = request.red_sube_context.validation_point_type
    if not window_matched: return SyncChannel.NO_CHANNEL_AVAILABLE
    if priority_device.has_mobile_device and priority_device.has_nfc_capable_device and collaborator_device.has_physical_sube_card: return SyncChannel.PRIORITY_MOBILE_NFC_CARD_TAP
    if collaborator_device.has_mobile_device and collaborator_device.has_app_or_account_access_now and collaborator_device.has_connectivity_now: return SyncChannel.COLLABORATOR_MOBILE_QR_OR_CODE
    if policy.allow_no_mobile_channels and validation_point in {ValidationPointType.VEHICLE_VALIDATOR, ValidationPointType.ONBOARD_TRAIN_VALIDATOR}: return SyncChannel.VALIDATOR_CONTEXT_WINDOW
    if policy.allow_no_mobile_channels and validation_point in {ValidationPointType.STATION_TURNSTILE, ValidationPointType.STATION_ACCESS_GATE}: return SyncChannel.TURNSTILE_OR_STATION_WINDOW
    if policy.allow_assisted_channel and validation_point == ValidationPointType.TERMINAL_VALIDATOR: return SyncChannel.ASSISTED_STATION_OR_TERMINAL_CHANNEL
def _hard_risk_flags(request: SolidarySyncChannelRequest, policy: SyncChannelPolicy, window_matched: bool, context_score: int) -> List[str]:
    flags: List[str] = []
    if _looks_like_free_text(request.priority_user_token): flags.append("priority_user_token_looks_like_free_text")
    if _looks_like_free_text(request.collaborator_user_token): flags.append("collaborator_user_token_looks_like_free_text")
    if request.priority_user_token == request.collaborator_user_token: flags.append("same_user_token_not_allowed")
    if policy.require_priority_attribute_active and not request.priority_user_has_active_attribute: flags.append("priority_attribute_not_active")
    if policy.require_priority_need_previously_accredited and not request.priority_need_previously_accredited: flags.append("priority_need_not_previously_accredited")
    if policy.require_priority_paid_validation and not request.red_sube_context.priority_paid_validation_confirmed: flags.append("priority_paid_validation_required")
    if policy.require_collaborator_paid_validation and not request.red_sube_context.collaborator_paid_validation_confirmed: flags.append("collaborator_paid_validation_required")
    if policy.require_priority_confirmation:
        if request.confirmation_mode == ConfirmationMode.MISSING: flags.append("priority_confirmation_missing")
        if not request.priority_user_confirms_or_can_confirm: flags.append("priority_user_cannot_confirm")
    if request.collaborator_claims_unilaterally: flags.append("collaborator_unilateral_claim")
    if not request.voluntary_seat_yield_declared: flags.append("voluntary_seat_yield_required")
    if not request.previous_handoff_security_accepted: flags.append("previous_handoff_security_not_accepted")
    if request.previous_proximity_guard_blocks_flow: flags.append("previous_proximity_guard_blocks_flow")
    if not window_matched: flags.append("sync_window_expired")
    if context_score <= 0: flags.append("no_shared_transport_context")
    return _deduplicate(flags)

def _audit_flags(request: SolidarySyncChannelRequest, policy: SyncChannelPolicy, selected_channel: SyncChannel, window_kind: WindowKind, context_score: int) -> List[str]:
    flags: List[str] = []
    p_dev = request.priority_device_availability
    c_dev = request.collaborator_device_availability
    if not p_dev.has_mobile_device: flags.append("priority_user_without_mobile_supported")
    if not c_dev.has_mobile_device: flags.append("collaborator_without_mobile_supported")
    if not p_dev.has_mobile_device and not c_dev.has_mobile_device: flags.append("no_mobile_both_users_non_blocking")
    if selected_channel in {SyncChannel.VALIDATOR_CONTEXT_WINDOW, SyncChannel.TURNSTILE_OR_STATION_WINDOW, SyncChannel.ASSISTED_STATION_OR_TERMINAL_CHANNEL, SyncChannel.ACCOUNT_DEFERRED_CONFIRMATION}: flags.append("red_sube_contextual_channel_audit")
    if selected_channel == SyncChannel.VALIDATOR_CONTEXT_WINDOW: flags.append("validator_window_opened_demo")
    if selected_channel == SyncChannel.TURNSTILE_OR_STATION_WINDOW: flags.append("turnstile_or_station_window_opened_demo")
    if selected_channel == SyncChannel.ACCOUNT_DEFERRED_CONFIRMATION: flags.append("deferred_account_confirmation_audit")
    if request.confirmation_mode in {ConfirmationMode.DEFERRED_ACCOUNT_CONFIRMATION, ConfirmationMode.VALIDATOR_WINDOW_PENDING_CONFIRMATION, ConfirmationMode.ASSISTED_CONFIRMATION}: flags.append("non_immediate_confirmation_audit")
    if window_kind in {WindowKind.STATION_EXTENDED_WINDOW, WindowKind.TERMINAL_EXTENDED_WINDOW, WindowKind.DEFERRED_ACCOUNT_WINDOW}: flags.append("extended_window_audit")
    if context_score < policy.max_context_score_for_ready_without_mobile: flags.append("low_context_score_audit")
    return _deduplicate(flags)

def _window_kind(context: RedSubeValidationContext) -> WindowKind:
    if context.validation_point_type == ValidationPointType.VEHICLE_VALIDATOR: return WindowKind.IN_VEHICLE_SHORT_WINDOW
    if context.validation_point_type == ValidationPointType.ONBOARD_TRAIN_VALIDATOR: return WindowKind.ONBOARD_TRAIN_SHORT_WINDOW
    if context.validation_point_type in {ValidationPointType.STATION_TURNSTILE, ValidationPointType.STATION_ACCESS_GATE}: return WindowKind.STATION_EXTENDED_WINDOW
    if context.validation_point_type == ValidationPointType.TERMINAL_VALIDATOR: return WindowKind.TERMINAL_EXTENDED_WINDOW
    return WindowKind.UNKNOWN_WINDOW

def _window_minutes(window_kind: WindowKind, policy: SyncChannelPolicy) -> int:
    if window_kind == WindowKind.IN_VEHICLE_SHORT_WINDOW: return policy.in_vehicle_window_minutes
    if window_kind == WindowKind.ONBOARD_TRAIN_SHORT_WINDOW: return policy.onboard_train_window_minutes
    if window_kind == WindowKind.STATION_EXTENDED_WINDOW: return policy.station_window_minutes
    if window_kind == WindowKind.TERMINAL_EXTENDED_WINDOW: return policy.terminal_window_minutes
    if window_kind == WindowKind.DEFERRED_ACCOUNT_WINDOW: return policy.deferred_confirmation_window_hours * 60
    return policy.in_vehicle_window_minutes

def _window_matched(context: RedSubeValidationContext, window_minutes: int) -> bool:
    earliest = min(context.priority_validation_timestamp_utc, context.collaborator_validation_timestamp_utc)
    elapsed_seconds = abs((context.sync_attempt_timestamp_utc - earliest).total_seconds())
    return elapsed_seconds <= timedelta(minutes=window_minutes).total_seconds()

def _context_score(request: SolidarySyncChannelRequest) -> int:
    score = 0
    if request.same_network_demo_id: score += 1
    if request.same_route_demo_id: score += 1
    if request.same_service_window_demo_id: score += 1
    if request.same_validator_or_turnstile_demo_id: score += 2
    if request.same_vehicle_demo_id: score += 2
    if request.same_trainset_demo_id: score += 2
    if request.same_station_demo_id: score += 1
    if request.same_platform_demo_id: score += 2
    return score
def _result(request: SolidarySyncChannelRequest, policy: SyncChannelPolicy, status: SyncChannelStatus, selected_channel: SyncChannel, window_kind: WindowKind, window_minutes: int, window_matched: bool, context_score: int, opens_bonus_evaluation_window: bool, blocks_solidary_bonus_flow: bool, requires_audit_review: bool, hard_risk_flags: List[str], audit_flags: List[str], reason: str) -> SolidarySyncChannelResult:
    return SolidarySyncChannelResult(
        project=PROJECT_NAME, module=MODULE_NAME, version=MODULE_VERSION, demo_mode=DEMO_MODE, status=status, selected_channel=selected_channel, window_kind=window_kind, window_minutes=window_minutes, window_matched=window_matched, mobile_required=False,
        priority_mobile_available=request.priority_device_availability.has_mobile_device, collaborator_mobile_available=request.collaborator_device_availability.has_mobile_device, no_mobile_path_supported=policy.allow_no_mobile_channels, context_score=context_score, opens_bonus_evaluation_window=opens_bonus_evaluation_window, blocks_solidary_bonus_flow=blocks_solidary_bonus_flow, requires_audit_review=requires_audit_review, hard_risk_flags=hard_risk_flags, audit_flags=audit_flags, reason=reason,
        security_summary=_security_summary(request=request, policy=policy, selected_channel=selected_channel, window_kind=window_kind, window_minutes=window_minutes, window_matched=window_matched, context_score=context_score),
        privacy_notice=_privacy_notice(), legal_scope_notice=_legal_scope_notice(), driver_burden=_driver_burden_notice(), warnings=_common_warnings(), timestamp_utc=_now_utc()
    )

def _security_summary(request: SolidarySyncChannelRequest, policy: SyncChannelPolicy, selected_channel: SyncChannel, window_kind: WindowKind, window_minutes: int, window_matched: bool, context_score: int) -> Dict[str, Any]:
    context = request.red_sube_context
    return {
        "sync_channel_event_demo_id": request.sync_channel_event_demo_id,
        "selected_channel": selected_channel.value,
        "window_kind": window_kind.value,
        "window_minutes": window_minutes,
        "window_matched": window_matched,
        "context_score": context_score,
        "transport_mode": context.transport_mode.value,
        "validation_point_type": context.validation_point_type.value,
        "priority_mobile_available": request.priority_device_availability.has_mobile_device,
        "priority_nfc_available": request.priority_device_availability.has_nfc_capable_device,
        "collaborator_mobile_available": request.collaborator_device_availability.has_mobile_device,
        "collaborator_physical_sube_card_available": request.collaborator_device_availability.has_physical_sube_card,
        "priority_paid_validation_confirmed": context.priority_paid_validation_confirmed,
        "collaborator_paid_validation_confirmed": context.collaborator_paid_validation_confirmed,
        "confirmation_mode": request.confirmation_mode.value,
        "priority_user_confirms_or_can_confirm": request.priority_user_confirms_or_can_confirm,
        "same_network_demo_id": request.same_network_demo_id,
        "same_route_demo_id": request.same_route_demo_id,
        "same_service_window_demo_id": request.same_service_window_demo_id,
        "same_validator_or_turnstile_demo_id": request.same_validator_or_turnstile_demo_id,
        "same_vehicle_demo_id": request.same_vehicle_demo_id,
        "same_trainset_demo_id": request.same_trainset_demo_id,
        "same_station_demo_id": request.same_station_demo_id,
        "same_platform_demo_id": request.same_platform_demo_id,
        "allow_no_mobile_channels": policy.allow_no_mobile_channels,
        "allow_assisted_channel": policy.allow_assisted_channel,
        "allow_deferred_account_confirmation": policy.allow_deferred_account_confirmation
    }

def _privacy_notice() -> str: 
    return "El selector de canales no revela DNI, nombre, domicilio, diagnóstico, CUD, historia clínica, certificado médico, teléfono, email, IMEI, MAC, saldo ni GPS exacto. La ausencia de celular no bloquea automáticamente."

def _legal_scope_notice() -> str: 
    return "La apertura de ventanas y canales es conceptual. No aplica descuentos reales, no actualiza tarjetas reales y no integra Red SUBE real. Una implementación requeriría autorización, integración oficial, auditoría y normativa competente."

def _driver_burden_notice() -> str: 
    return "El chofer no selecciona canales, no verifica sincronizaciones, no decide beneficios y no administra el Bono Solidario."

def _common_warnings() -> List[str]:
    return [
        "Selector conceptual y demostrativo.", "Sin implementación oficial vigente.", "Sin integración real con SUBE.", 
        "Sin integración real con Red SUBE.", "Sin consulta a cuentas reales.", "Sin consulta a tarjetas reales.", 
        "Sin consulta a validadoras reales.", "Sin consulta a molinetes reales.", "Sin saldo real.", "Sin tarifa real.", 
        "Sin escritura real sobre chip SUBE.", "Sin DNI.", "Sin diagnóstico médico.", "Sin CUD visible.", 
        "Sin teléfono real.", "Sin email real.", "Sin IMEI real.", "Sin MAC real.", "Sin GPS exacto.", "Sin vigilancia.", 
        "Sin ranking.", "Sin sanciones.", "Sin obligación de tener celular.", "El usuario SUBE Prioridad puede no tener celular.", 
        "El colaborador puede no tener celular.", "La Red SUBE demo puede abrir ventanas lógicas desde validadoras o molinetes.", 
        "Cada tipo de validadora o molinete puede tener una ventana temporal distinta.", "La ausencia de móvil reduce refuerzo probatorio, pero no bloquea por sí sola.", 
        "Las ventanas más amplias requieren mayor auditoría antifraude."
    ]

def _validate_required_values(required_values: Dict[str, str]) -> None:
    for field_name, value in required_values.items():
        if not value or not value.strip(): 
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")

def _looks_like_free_text(token: str) -> bool:
    normalized = token.lower().strip()
    suspicious_terms = {"quiero", "gratis", "beneficio", "tarifa", "social", "diagnostico", "diagnóstico", "cud", "certificado", "medico", "médico", "andis", "sancion", "sanción", "ranking", "vigilancia", "premio", "puntos", "bono solidario", "red sube", "gps", "telefono", "teléfono", "email", "saldo", "dinero"}
    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1

def _strip_optional(value: Optional[str]) -> Optional[str]:
    if value is None: return None
    stripped = value.strip()
    return stripped if stripped else None

def _deduplicate(flags: List[str]) -> List[str]:
    seen = set()
    result = []
    for flag in flags:
        if flag not in seen: 
            seen.add(flag)
            result.append(flag)
    return result

def _now_utc() -> str: 
    return datetime.now(timezone.utc).isoformat()

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))

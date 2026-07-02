"""
SUBE Prioridad — Alerta posterior a validación demo.
Este módulo modela qué puede ocurrir después de que una persona con atributo
SUBE Prioridad valida/paga su viaje en una validadora, molinete o punto de
acceso compatible.

Regla central:
 La alerta se dispara después de una validación paga.
 No revela diagnóstico. No revela CUD. No revela DNI.
 No revela identidad civil. No obliga al chofer.
 No reemplaza derechos vigentes. No integra SUBE real.
 No integra Red SUBE real.

Objetivo:
 Convertir la preferencia elegida por el usuario en una señal preventiva,
 pasiva, discreta, visible o lumínica, según corresponda al contexto.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Alerta Posterior a Validación"
MODULE_VERSION = "0.1.0"
DEMO_MODE = True

PROHIBITED_FIELDS = {
    "dni", "documento", "nombre", "apellido", "domicilio", "direccion", "dirección",
    "telefono", "teléfono", "phone", "email", "correo", "diagnostico", "diagnóstico",
    "historia_clinica", "historia_clínica", "certificado_medico", "certificado_médico",
    "cud", "discapacidad", "patologia", "patología", "medico", "médico", "obra_social",
    "gps", "latitud", "longitud", "latitude", "longitude", "imei", "mac", "saldo", "dinero"
}

class AlertChannel(str, Enum):
    PASSIVE_INTERNAL = "passive_internal"
    DISCREET_VISUAL = "discreet_visual"
    VISIBLE_LIGHT = "visible_light"
    LUMINOUS_SIGNAL = "luminous_signal"
    SILENT_LOG = "silent_log"
    STATION_OPERATOR_DEVICE = "station_operator_device"
    TRANSPORT_OPERATOR_DEVICE = "transport_operator_device"

class AlertPreferenceMode(str, Enum):
    SILENT = "silent"
    PASSIVE = "passive"
    DISCREET = "discreet"
    VISIBLE = "visible"
    LUMINOUS = "luminous"

class ValidationPointType(str, Enum):
    VEHICLE_VALIDATOR = "vehicle_validator"
    STATION_TURNSTILE = "station_turnstile"
    STATION_ACCESS_GATE = "station_access_gate"
    TERMINAL_VALIDATOR = "terminal_validator"
    UNKNOWN = "unknown"

class TransportMode(str, Enum):
    BUS = "bus"
    TRAIN = "train"
    SUBWAY = "subway"
    COASTAL_TRAIN_OR_ONBOARD_VALIDATOR = "coastal_train_or_onboard_validator"
    OTHER_PUBLIC_TRANSPORT = "other_public_transport"

class TriggerStatus(str, Enum):
    TRIGGERED = "triggered"
    NOT_TRIGGERED = "not_triggered"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"

@dataclass(frozen=True)
class PriorityAttributeDemo:
    priority_user_token: str
    priority_attribute_token: str
    active: bool
    previously_accredited_need: bool

@dataclass(frozen=True)
class UserAlertPreferences:
    preference_mode: AlertPreferenceMode
    allow_passive_internal_alert: bool
    allow_discreet_visual_alert: bool
    allow_visible_light_alert: bool
    allow_luminous_signal: bool
    allow_station_operator_notification: bool
    allow_transport_operator_notification: bool
    allow_silent_log: bool

@dataclass(frozen=True)
class ValidationEventDemo:
    validation_event_demo_id: str
    validation_paid: bool
    country: str
    network_demo_id: str
    route_demo_id: str
    vehicle_demo_id: Optional[str]
    station_demo_id: Optional[str]
    platform_demo_id: Optional[str]
    validation_point_type: ValidationPointType
    transport_mode: TransportMode
    timestamp_utc: datetime

@dataclass(frozen=True)
class ValidatorTriggerAlertRequest:
    priority_attribute: PriorityAttributeDemo
    preferences: UserAlertPreferences
    validation_event: ValidationEventDemo

@dataclass(frozen=True)
class ValidatorTriggerAlertResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: TriggerStatus
    selected_channels: List[AlertChannel]
    alert_triggered: bool
    station_or_operator_notification_requested: bool
    exposes_sensitive_data: bool
    driver_burden: str
    hard_risk_flags: List[str]
    audit_flags: List[str]
    reason: str
    privacy_notice: str
    legal_scope_notice: str
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

def create_demo_priority_attribute(
    priority_user_token: str = "demo-priority-user-001",
    priority_attribute_token: str = "demo-priority-attribute-001",
    active: bool = True,
    previously_accredited_need: bool = True,
) -> PriorityAttributeDemo:
    required_values = {"priority_user_token": priority_user_token, "priority_attribute_token": priority_attribute_token}
    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)
    return PriorityAttributeDemo(
        priority_user_token=priority_user_token.strip(),
        priority_attribute_token=priority_attribute_token.strip(),
        active=active, previously_accredited_need=previously_accredited_need,
    )

def create_demo_user_alert_preferences(
    preference_mode: AlertPreferenceMode = AlertPreferenceMode.DISCREET,
    allow_passive_internal_alert: bool = True,
    allow_discreet_visual_alert: bool = True,
    allow_visible_light_alert: bool = False,
    allow_luminous_signal: bool = False,
    allow_station_operator_notification: bool = False,
    allow_transport_operator_notification: bool = False,
    allow_silent_log: bool = True,
) -> UserAlertPreferences:
    return UserAlertPreferences(
        preference_mode=preference_mode, allow_passive_internal_alert=allow_passive_internal_alert,
        allow_discreet_visual_alert=allow_discreet_visual_alert, allow_visible_light_alert=allow_visible_light_alert,
        allow_luminous_signal=allow_luminous_signal, allow_station_operator_notification=allow_station_operator_notification,
        allow_transport_operator_notification=allow_transport_operator_notification, allow_silent_log=allow_silent_log,
    )

def create_demo_validation_event(
    validation_event_demo_id: str = "demo-validation-event-001",
    validation_paid: bool = True,
    country: str = "AR",
    network_demo_id: str = "demo-red-sube-network-001",
    route_demo_id: str = "demo-route-001",
    vehicle_demo_id: Optional[str] = "demo-vehicle-001",
    station_demo_id: Optional[str] = None,
    platform_demo_id: Optional[str] = None,
    validation_point_type: ValidationPointType = ValidationPointType.VEHICLE_VALIDATOR,
    transport_mode: TransportMode = TransportMode.BUS,
    timestamp_utc: Optional[datetime] = None,
) -> ValidationEventDemo:
    required_values = {"validation_event_demo_id": validation_event_demo_id, "country": country, "network_demo_id": network_demo_id, "route_demo_id": route_demo_id}
    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)
    return ValidationEventDemo(
        validation_event_demo_id=validation_event_demo_id.strip(), validation_paid=validation_paid,
        country=country.strip().upper(), network_demo_id=network_demo_id.strip(), route_demo_id=route_demo_id.strip(),
        vehicle_demo_id=_strip_optional(vehicle_demo_id), station_demo_id=_strip_optional(station_demo_id),
        platform_demo_id=_strip_optional(platform_demo_id), validation_point_type=validation_point_type,
        transport_mode=transport_mode, timestamp_utc=timestamp_utc or datetime.now(timezone.utc),
    )

def create_demo_validator_trigger_alert_request(
    priority_attribute: Optional[PriorityAttributeDemo] = None,
    preferences: Optional[UserAlertPreferences] = None,
    validation_event: Optional[ValidationEventDemo] = None,
) -> ValidatorTriggerAlertRequest:
    return ValidatorTriggerAlertRequest(
        priority_attribute=priority_attribute or create_demo_priority_attribute(),
        preferences=preferences or create_demo_user_alert_preferences(),
        validation_event=validation_event or create_demo_validation_event(),
    )

def evaluate_validator_trigger_alert(request: ValidatorTriggerAlertRequest) -> ValidatorTriggerAlertResult:
    assert_no_prohibited_fields({
        "priority_user_token": request.priority_attribute.priority_user_token,
        "priority_attribute_token": request.priority_attribute.priority_attribute_token,
        "validation_event_demo_id": request.validation_event.validation_event_demo_id,
    })
    hard_risk_flags = _hard_risk_flags(request)
    audit_flags = _audit_flags(request)
    if hard_risk_flags:
        return _result(status=TriggerStatus.REJECTED, selected_channels=[], hard_risk_flags=hard_risk_flags, audit_flags=audit_flags, reason="No se disparó alerta porque faltan condiciones mínimas: atributo activo, necesidad previamente acreditada, validación paga o contexto compatible.")
    selected_channels = _select_channels(request)
    if not selected_channels:
        return _result(status=TriggerStatus.NOT_TRIGGERED, selected_channels=[], hard_risk_flags=[], audit_flags=audit_flags, reason="No se disparó alerta porque las preferencias del usuario no habilitan canales activos para este contexto.")
    return _result(status=TriggerStatus.TRIGGERED, selected_channels=selected_channels, hard_risk_flags=[], audit_flags=audit_flags, reason="Alerta demo posterior a validación generada según preferencias del usuario y sin exponer datos sensibles.")

def simulate_validator_trigger_alert(request: Optional[ValidatorTriggerAlertRequest] = None) -> ValidatorTriggerAlertResult:
    return evaluate_validator_trigger_alert(request or create_demo_validator_trigger_alert_request())

def result_to_dict(result: ValidatorTriggerAlertResult) -> Dict[str, Any]:
    return {"project": result.project, "module": result.module, "version": result.version, "demo_mode": result.demo_mode, "status": result.status.value, "selected_channels": [channel.value for channel in result.selected_channels], "alert_triggered": result.alert_triggered, "station_or_operator_notification_requested": result.station_or_operator_notification_requested, "exposes_sensitive_data": result.exposes_sensitive_data, "driver_burden": result.driver_burden, "hard_risk_flags": result.hard_risk_flags, "audit_flags": result.audit_flags, "reason": result.reason, "privacy_notice": result.privacy_notice, "legal_scope_notice": result.legal_scope_notice, "warnings": result.warnings, "timestamp_utc": result.timestamp_utc}

def run_demo() -> Dict[str, Any]:
    result = simulate_validator_trigger_alert()
    return result_to_dict(result)

def _hard_risk_flags(request: ValidatorTriggerAlertRequest) -> List[str]:
    flags: List[str] = []; priority = request.priority_attribute; event = request.validation_event
    if _looks_like_free_text(priority.priority_user_token): flags.append("priority_user_token_looks_like_free_text")
    if _looks_like_free_text(priority.priority_attribute_token): flags.append("priority_attribute_token_looks_like_free_text")
    if _looks_like_free_text(event.validation_event_demo_id): flags.append("validation_event_id_looks_like_free_text")
    if not priority.active: flags.append("priority_attribute_not_active")
    if not priority.previously_accredited_need: flags.append("priority_need_not_previously_accredited")
    if not event.validation_paid: flags.append("validation_payment_not_confirmed")
    if event.country != "AR": flags.append("outside_argentina_context")
    if event.validation_point_type == ValidationPointType.UNKNOWN: flags.append("unknown_validation_point_type")
    return _deduplicate(flags)

def _audit_flags(request: ValidatorTriggerAlertRequest) -> List[str]:
    flags: List[str] = []; event = request.validation_event
    flags.append("validator_trigger_alert_audit")
    if event.validation_point_type == ValidationPointType.VEHICLE_VALIDATOR: flags.append("vehicle_validator_context")
    if event.validation_point_type in {ValidationPointType.STATION_TURNSTILE, ValidationPointType.STATION_ACCESS_GATE}: flags.append("station_or_turnstile_context")
    if event.transport_mode in {TransportMode.TRAIN, TransportMode.SUBWAY, TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR}: flags.append("rail_or_subway_context")
    return _deduplicate(flags)

def _select_channels(request: ValidatorTriggerAlertRequest) -> List[AlertChannel]:
    preferences = request.preferences; event = request.validation_event; channels: List[AlertChannel] = []
    if preferences.allow_silent_log: channels.append(AlertChannel.SILENT_LOG)
    if preferences.allow_passive_internal_alert and preferences.preference_mode in {AlertPreferenceMode.PASSIVE, AlertPreferenceMode.DISCREET, AlertPreferenceMode.VISIBLE, AlertPreferenceMode.LUMINOUS}: channels.append(AlertChannel.PASSIVE_INTERNAL)
    if preferences.allow_discreet_visual_alert and preferences.preference_mode in {AlertPreferenceMode.DISCREET, AlertPreferenceMode.VISIBLE, AlertPreferenceMode.LUMINOUS}: channels.append(AlertChannel.DISCREET_VISUAL)
    if preferences.allow_visible_light_alert and preferences.preference_mode in {AlertPreferenceMode.VISIBLE, AlertPreferenceMode.LUMINOUS}: channels.append(AlertChannel.VISIBLE_LIGHT)
    if preferences.allow_luminous_signal and preferences.preference_mode == AlertPreferenceMode.LUMINOUS: channels.append(AlertChannel.LUMINOUS_SIGNAL)
    if preferences.allow_station_operator_notification and event.validation_point_type in {ValidationPointType.STATION_TURNSTILE, ValidationPointType.STATION_ACCESS_GATE, ValidationPointType.TERMINAL_VALIDATOR}: channels.append(AlertChannel.STATION_OPERATOR_DEVICE)
    if preferences.allow_transport_operator_notification: channels.append(AlertChannel.TRANSPORT_OPERATOR_DEVICE)
    if preferences.preference_mode == AlertPreferenceMode.SILENT: return [AlertChannel.SILENT_LOG] if preferences.allow_silent_log else []
    return _deduplicate_channels(channels)

def _result(status: TriggerStatus, selected_channels: List[AlertChannel], hard_risk_flags: List[str], audit_flags: List[str], reason: str) -> ValidatorTriggerAlertResult:
    station_or_operator_notification_requested = any(channel in {AlertChannel.STATION_OPERATOR_DEVICE, AlertChannel.TRANSPORT_OPERATOR_DEVICE} for channel in selected_channels)
    return ValidatorTriggerAlertResult(
        project=PROJECT_NAME, module=MODULE_NAME, version=MODULE_VERSION, demo_mode=DEMO_MODE, status=status, selected_channels=selected_channels, alert_triggered=status == TriggerStatus.TRIGGERED, station_or_operator_notification_requested=station_or_operator_notification_requested, exposes_sensitive_data=False,
        driver_burden="El chofer no recibe diagnóstico, no verifica datos personales, no decide prioridad y no asume una obligación nueva.",
        hard_risk_flags=hard_risk_flags, audit_flags=audit_flags, reason=reason,
        privacy_notice="La alerta demo sólo indica una preferencia de asistencia previamente configurada. No expone DNI, nombre, diagnóstico, CUD, certificado médico ni historia clínica.",
        legal_scope_notice="La alerta es conceptual y complementaria. No reemplaza derechos vigentes, no crea privilegios, no modifica obligaciones legales y no integra sistemas reales de SUBE o Red SUBE.",
        warnings=["Alerta posterior a validación conceptual y demostrativa.", "Sin integración real con SUBE.", "Sin integración real con Red SUBE.", "Sin consulta a validadoras reales.", "Sin consulta a molinetes reales.", "Sin DNI.", "Sin diagnóstico médico.", "Sin CUD visible.", "Sin exposición de datos sensibles.", "Sin obligación nueva para el chofer.", "La preferencia del usuario controla el modo de alerta."],
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )

def _validate_required_values(required_values: Dict[str, str]) -> None:
    for field_name, value in required_values.items():
        if not value or not value.strip(): raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")

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
        if flag not in seen: seen.add(flag); result.append(flag)
    return result

def _deduplicate_channels(channels: List[AlertChannel]) -> List[AlertChannel]:
    seen = set()
    result = []
    for channel in channels:
        if channel.value not in seen: seen.add(channel.value); result.append(channel)
    return result

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))

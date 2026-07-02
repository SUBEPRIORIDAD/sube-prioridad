"""
SUBE Prioridad — Política demo de activación por viaje.
Este módulo modela una regla central del proyecto:
 Tener el atributo SUBE Prioridad activo NO significa que el usuario
 quiera activar asistencia, alerta o comunicación en todos sus viajes.

El atributo puede estar activo como respaldo general, pero cada viaje puede
tener distintos niveles de activación según preferencias del usuario,
contexto del transporte y consentimiento.

Regla general de calle:
 El entorno operativo sólo ve "Usuario SUBE Prioridad".

Excepción:
 En trenes, subtes, estaciones, andenes o plataformas puede compartirse
 un indicio operativo respetuoso con personal autorizado, sólo si el usuario
 prestó consentimiento.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Política Demo de Activación por Viaje"
MODULE_VERSION = "0.1.0"
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
    "email",
    "correo",
    "diagnostico",
    "diagnóstico",
    "patologia",
    "patología",
    "historia_clinica",
    "historia_clínica",
    "certificado_medico",
    "certificado_médico",
    "cud",
    "discapacidad",
    "embarazo",
    "lesion",
    "lesión",
    "fractura",
    "tratamiento",
    "medicacion",
    "medicación",
    "obra_social",
    "saldo",
    "dinero",
    "tarifa",
    "gps",
    "latitud",
    "longitud",
}

class TripAssistanceMode(str, Enum):
    SILENT = "silent"
    INTERNAL_PASSIVE = "internal_passive"
    DISCREET = "discreet"
    VISIBLE = "visible"
    LUMINOUS = "luminous"
    STATION_AUTHORIZED_STAFF = "station_authorized_staff"

class TripActivationStatus(str, Enum):
    NOT_ACTIVE = "not_active"
    ACTIVE_SILENT_BACKUP = "active_silent_backup"
    ACTIVE_PASSIVE_NOTICE = "active_passive_notice"
    ACTIVE_DISCREET_NOTICE = "active_discreet_notice"
    ACTIVE_VISIBLE_NOTICE = "active_visible_notice"
    ACTIVE_STATION_AUTHORIZED_NOTICE = "active_station_authorized_notice"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"

class TransportContext(str, Enum):
    BUS = "bus"
    TRAIN_ONBOARD = "train_onboard"
    TRAIN_STATION = "train_station"
    SUBWAY_ONBOARD = "subway_onboard"
    SUBWAY_STATION = "subway_station"
    TURNSTILE = "turnstile"
    PLATFORM = "platform"
    TERMINAL = "terminal"
    OTHER_PUBLIC_TRANSPORT = "other_public_transport"

class VisibilityScope(str, Enum):
    NONE = "none"
    SYSTEM_ONLY = "system_only"
    AUTHORIZED_STAFF_ONLY = "authorized_staff_only"
    PUBLIC_GENERIC = "public_generic"

class ConsentedOperationalHint(str, Enum):
    NONE = "none"
    MAY_NEED_STATION_ASSISTANCE = "may_need_station_assistance"
    MAY_NEED_PLATFORM_ASSISTANCE = "may_need_platform_assistance"
    MAY_NEED_DESCENT_SUPPORT = "may_need_descent_support"
    MAY_NEED_DISCREET_SECURITY_NOTICE = "may_need_discreet_security_notice"
    MAY_NEED_NON_SPECIFIC_DECOMPENSATION_SUPPORT = "may_need_non_specific_decompensation_support"
@dataclass(frozen=True)
class PriorityAttributeForTripDemo:
    priority_attribute_token: str
    active: bool
    valid_for_trip: bool
    generic_visibility_label: str
    consented_operational_hint: ConsentedOperationalHint
    consented_operational_hint_enabled: bool

@dataclass(frozen=True)
class TripActivationPreferenceDemo:
    assistance_mode: TripAssistanceMode
    user_requests_assistance_this_trip: bool
    user_allows_public_generic_notice: bool
    user_allows_authorized_staff_notice: bool
    user_allows_luminous_signal: bool
    user_allows_station_hint: bool

@dataclass(frozen=True)
class TripValidationContextDemo:
    trip_event_demo_id: str
    transport_context: TransportContext
    validation_paid: bool
    validation_timestamp_utc: datetime
    validator_or_turnstile_demo_token: str
    operator_context_demo_token: Optional[str]

@dataclass(frozen=True)
class TripActivationRequestDemo:
    priority_attribute: PriorityAttributeForTripDemo
    preference: TripActivationPreferenceDemo
    validation_context: TripValidationContextDemo

@dataclass(frozen=True)
class TripActivationResultDemo:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: TripActivationStatus
    priority_attribute_active: bool
    visible_as: str
    visibility_scope: VisibilityScope
    operational_hint_shared: bool
    operational_hint: ConsentedOperationalHint
    authorized_staff_only: bool
    alert_payload_demo: Dict[str, Any]
    blocks_trip_assistance_flow: bool
    risk_flags: List[str]
    audit_flags: List[str]
    privacy_notice: str
    legal_scope_notice: str
    warnings: List[str]
    timestamp_utc: str

def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(keys.intersection(PROHIBITED_FIELDS))
    if forbidden:
        raise ValueError(
            "El payload contains campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )

def purge_prohibited_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Sección XXXVII: Purga irreversible de cualquier vector restringido de entrada."""
    if not isinstance(payload, dict):
        return payload
    sanitized_payload = {}
    for key, value in payload.items():
        normalized_key = str(key).strip().lower()
        if normalized_key in PROHIBITED_FIELDS:
            continue
        if isinstance(value, dict):
            sanitized_payload[key] = purge_prohibited_fields(value)
        else:
            sanitized_payload[key] = value
    return sanitized_payload
def create_demo_priority_attribute_for_trip(
    priority_attribute_token: str = "demo-priority-attribute-001",
    active: bool = True,
    valid_for_trip: bool = True,
    generic_visibility_label: str = "Usuario SUBE Prioridad",
    consented_operational_hint: ConsentedOperationalHint = ConsentedOperationalHint.NONE,
    consented_operational_hint_enabled: bool = False,
) -> PriorityAttributeForTripDemo:
    payload = {
        "priority_attribute_token": priority_attribute_token,
        "generic_visibility_label": generic_visibility_label,
    }
    assert_no_prohibited_fields(payload)
    _require_non_empty(payload)
    return PriorityAttributeForTripDemo(
        priority_attribute_token=priority_attribute_token.strip(),
        active=active,
        valid_for_trip=valid_for_trip,
        generic_visibility_label=generic_visibility_label.strip(),
        consented_operational_hint=consented_operational_hint,
        consented_operational_hint_enabled=consented_operational_hint_enabled,
    )

def create_demo_trip_activation_preference(
    assistance_mode: TripAssistanceMode = TripAssistanceMode.INTERNAL_PASSIVE,
    user_requests_assistance_this_trip: bool = True,
    user_allows_public_generic_notice: bool = False,
    user_allows_authorized_staff_notice: bool = False,
    user_allows_luminous_signal: bool = False,
    user_allows_station_hint: bool = False,
) -> TripActivationPreferenceDemo:
    return TripActivationPreferenceDemo(
        assistance_mode=assistance_mode,
        user_requests_assistance_this_trip=user_requests_assistance_this_trip,
        user_allows_public_generic_notice=user_allows_public_generic_notice,
        user_allows_authorized_staff_notice=user_allows_authorized_staff_notice,
        user_allows_luminous_signal=user_allows_luminous_signal,
        user_allows_station_hint=user_allows_station_hint,
    )

def create_demo_trip_validation_context(
    trip_event_demo_id: str = "demo-trip-event-001",
    transport_context: TransportContext = TransportContext.BUS,
    validation_paid: bool = True,
    validation_timestamp_utc: Optional[datetime] = None,
    validator_or_turnstile_demo_token: str = "demo-validator-token-001",
    operator_context_demo_token: Optional[str] = "demo-operator-context-001",
) -> TripValidationContextDemo:
    payload = {
        "trip_event_demo_id": trip_event_demo_id,
        "validator_or_turnstile_demo_token": validator_or_turnstile_demo_token,
        "operator_context_demo_token": operator_context_demo_token or "not-provided",
    }
    assert_no_prohibited_fields(payload)
    _require_non_empty(
        {
            "trip_event_demo_id": trip_event_demo_id,
            "validator_or_turnstile_demo_token": validator_or_turnstile_demo_token,
        }
    )
    return TripValidationContextDemo(
        trip_event_demo_id=trip_event_demo_id.strip(),
        transport_context=transport_context,
        validation_paid=validation_paid,
        validation_timestamp_utc=(validation_timestamp_utc or datetime.now(timezone.utc)),
        validator_or_turnstile_demo_token=validator_or_turnstile_demo_token.strip(),
        operator_context_demo_token=(operator_context_demo_token.strip() if operator_context_demo_token else None),
    )

def create_demo_trip_activation_request(
    priority_attribute: Optional[PriorityAttributeForTripDemo] = None,
    preference: Optional[TripActivationPreferenceDemo] = None,
    validation_context: Optional[TripValidationContextDemo] = None,
) -> TripActivationRequestDemo:
    return TripActivationRequestDemo(
        priority_attribute=priority_attribute or create_demo_priority_attribute_for_trip(),
        preference=preference or create_demo_trip_activation_preference(),
        validation_context=validation_context or create_demo_trip_validation_context(),
    )
def evaluate_trip_activation_policy(
    request: TripActivationRequestDemo,
) -> TripActivationResultDemo:
    raw_payload_check = {
        "token": request.priority_attribute.priority_attribute_token,
        "event_id": request.validation_context.trip_event_demo_id
    }
    # Aseguramos el pipeline sanitizando proactiva y recursivamente los contextos transaccionales
    sanitized_check = purge_prohibited_fields(raw_payload_check)
    
    risk_flags = _risk_flags(request)
    audit_flags = _audit_flags(request)
    if risk_flags:
        return _result(
            request=request,
            status=TripActivationStatus.REJECTED,
            visible_as="Sin atributo SUBE Prioridad activo para este viaje",
            visibility_scope=VisibilityScope.NONE,
            operational_hint_shared=False,
            authorized_staff_only=False,
            blocks_trip_assistance_flow=True,
            risk_flags=risk_flags,
            audit_flags=audit_flags,
        )
    if not request.preference.user_requests_assistance_this_trip:
        return _result(
            request=request,
            status=TripActivationStatus.ACTIVE_SILENT_BACKUP,
            visible_as="Usuario SUBE Prioridad",
            visibility_scope=VisibilityScope.SYSTEM_ONLY,
            operational_hint_shared=False,
            authorized_staff_only=False,
            blocks_trip_assistance_flow=False,
            risk_flags=[],
            audit_flags=audit_flags + ["user_chose_no_active_assistance_this_trip"],
        )
    status, scope, hint_shared, staff_only = _resolve_activation(request=request)
    return _result(
        request=request,
        status=status,
        visible_as="Usuario SUBE Prioridad",
        visibility_scope=scope,
        operational_hint_shared=hint_shared,
        authorized_staff_only=staff_only,
        blocks_trip_assistance_flow=False,
        risk_flags=[],
        audit_flags=audit_flags,
    )

def result_to_dict(result: TripActivationResultDemo) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "priority_attribute_active": result.priority_attribute_active,
        "visible_as": result.visible_as,
        "visibility_scope": result.visibility_scope.value,
        "operational_hint_shared": result.operational_hint_shared,
        "operational_hint": result.operational_hint.value,
        "authorized_staff_only": result.authorized_staff_only,
        "alert_payload_demo": result.alert_payload_demo,
        "blocks_trip_assistance_flow": result.blocks_trip_assistance_flow,
        "risk_flags": result.risk_flags,
        "audit_flags": result.audit_flags,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }
def run_demo() -> Dict[str, Any]:
    result = evaluate_trip_activation_policy(create_demo_trip_activation_request())
    return result_to_dict(result)

def run_silent_backup_demo() -> Dict[str, Any]:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.SILENT,
            user_requests_assistance_this_trip=False,
        )
    )
    result = evaluate_trip_activation_policy(request)
    return result_to_dict(result)

def run_station_hint_demo() -> Dict[str, Any]:
    request = create_demo_trip_activation_request(
        priority_attribute=create_demo_priority_attribute_for_trip(
            consented_operational_hint=ConsentedOperationalHint.MAY_NEED_PLATFORM_ASSISTANCE,
            consented_operational_hint_enabled=True,
        ),
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.STATION_AUTHORIZED_STAFF,
            user_requests_assistance_this_trip=True,
            user_allows_authorized_staff_notice=True,
            user_allows_station_hint=True,
        ),
        validation_context=create_demo_trip_validation_context(
            transport_context=TransportContext.PLATFORM,
        ),
    )
    result = evaluate_trip_activation_policy(request)
    return result_to_dict(result)

def _risk_flags(request: TripActivationRequestDemo) -> List[str]:
    flags: List[str] = []
    attribute = request.priority_attribute
    preference = request.preference
    validation = request.validation_context
    if not attribute.active:
        flags.append("priority_attribute_not_active")
    if not attribute.valid_for_trip:
        flags.append("priority_attribute_not_valid_for_trip")
    if attribute.generic_visibility_label != "Usuario SUBE Prioridad":
        flags.append("invalid_generic_visibility_label")
    if not validation.validation_paid:
        flags.append("validation_payment_not_confirmed")
    if preference.assistance_mode == TripAssistanceMode.LUMINOUS and not preference.user_allows_luminous_signal:
        flags.append("luminous_signal_not_consented")
    if preference.assistance_mode == TripAssistanceMode.VISIBLE and not preference.user_allows_public_generic_notice:
        flags.append("visible_notice_not_consented")
    if preference.assistance_mode == TripAssistanceMode.STATION_AUTHORIZED_STAFF and not preference.user_allows_authorized_staff_notice:
        flags.append("authorized_staff_notice_not_consented")
    if preference.user_allows_station_hint and not attribute.consented_operational_hint_enabled:
        flags.append("station_hint_preference_without_attribute_consent")
    if attribute.consented_operational_hint_enabled and attribute.consented_operational_hint == ConsentedOperationalHint.NONE:
        flags.append("operational_hint_enabled_without_hint")
    if not attribute.consented_operational_hint_enabled and attribute.consented_operational_hint != ConsentedOperationalHint.NONE:
        flags.append("operational_hint_present_without_attribute_consent")
    return _deduplicate(flags)
def _audit_flags(request: TripActivationRequestDemo) -> List[str]:
    flags = [
        "trip_level_activation_policy",
        "attribute_active_does_not_force_assistance_every_trip",
        "street_visibility_generic_sube_prioridad",
        "no_diagnosis_visible",
        "no_cud_visible",
        "no_real_integration",
    ]
    if request.preference.assistance_mode == TripAssistanceMode.SILENT:
        flags.append("silent_mode_supported")
    if request.preference.assistance_mode == TripAssistanceMode.INTERNAL_PASSIVE:
        flags.append("internal_passive_mode_supported")
    if request.preference.assistance_mode == TripAssistanceMode.DISCREET:
        flags.append("discreet_mode_supported")
    if request.preference.assistance_mode == TripAssistanceMode.VISIBLE:
        flags.append("visible_generic_mode_supported")
    if request.preference.assistance_mode == TripAssistanceMode.LUMINOUS:
        flags.append("luminous_mode_supported_with_consent")
    if request.preference.assistance_mode == TripAssistanceMode.STATION_AUTHORIZED_STAFF:
        flags.append("authorized_staff_station_mode_supported")
    if request.validation_context.transport_context in {
        TransportContext.TRAIN_STATION, TransportContext.SUBWAY_STATION,
        TransportContext.TURNSTILE, TransportContext.PLATFORM,
    }:
        flags.append("station_platform_context")
    return _deduplicate(flags)

def _resolve_activation(request: TripActivationRequestDemo) -> tuple[TripActivationStatus, VisibilityScope, bool, bool]:
    preference = request.preference
    context = request.validation_context.transport_context
    attribute = request.priority_attribute
    station_context = context in {
        TransportContext.TRAIN_STATION, TransportContext.SUBWAY_STATION,
        TransportContext.TURNSTILE, TransportContext.PLATFORM,
    }
    if preference.assistance_mode == TripAssistanceMode.SILENT:
        return (TripActivationStatus.ACTIVE_SILENT_BACKUP, VisibilityScope.SYSTEM_ONLY, False, False)
    if preference.assistance_mode == TripAssistanceMode.INTERNAL_PASSIVE:
        return (TripActivationStatus.ACTIVE_PASSIVE_NOTICE, VisibilityScope.SYSTEM_ONLY, False, False)
    if preference.assistance_mode == TripAssistanceMode.DISCREET:
        return (TripActivationStatus.ACTIVE_DISCREET_NOTICE, VisibilityScope.SYSTEM_ONLY, False, False)
    if preference.assistance_mode == TripAssistanceMode.VISIBLE:
        return (TripActivationStatus.ACTIVE_VISIBLE_NOTICE, VisibilityScope.PUBLIC_GENERIC, False, False)
    if preference.assistance_mode == TripAssistanceMode.LUMINOUS:
        return (TripActivationStatus.ACTIVE_VISIBLE_NOTICE, VisibilityScope.PUBLIC_GENERIC, False, False)
    
    if (
        preference.assistance_mode == TripAssistanceMode.STATION_AUTHORIZED_STAFF
        and station_context
        and preference.user_allows_station_hint
        and attribute.consented_operational_hint_enabled
        and attribute.consented_operational_hint != ConsentedOperationalHint.NONE
    ):
        return (TripActivationStatus.ACTIVE_STATION_AUTHORIZED_NOTICE, VisibilityScope.AUTHORIZED_STAFF_ONLY, True, True)
        
    if preference.assistance_mode == TripAssistanceMode.STATION_AUTHORIZED_STAFF:
        return (TripActivationStatus.ACTIVE_PASSIVE_NOTICE, VisibilityScope.SYSTEM_ONLY, False, False)
        
    return (TripActivationStatus.NEEDS_REVIEW, VisibilityScope.SYSTEM_ONLY, False, False)

def _result(
    request: TripActivationRequestDemo,
    status: TripActivationStatus,
    visible_as: str,
    visibility_scope: VisibilityScope,
    operational_hint_shared: bool,
    authorized_staff_only: bool,
    blocks_trip_assistance_flow: bool,
    risk_flags: List[str],
    audit_flags: List[str],
) -> TripActivationResultDemo:
    hint = request.priority_attribute.consented_operational_hint if operational_hint_shared else ConsentedOperationalHint.NONE
    
    raw_alert_payload = _alert_payload_demo(
        request=request, status=status, visibility_scope=visibility_scope,
        operational_hint_shared=operational_hint_shared, hint=hint, authorized_staff_only=authorized_staff_only
    )
    # Blindamos dinámicamente el payload interno simulado de la alerta antes del retorno
    safe_alert_payload = purge_prohibited_fields(raw_alert_payload)

    return TripActivationResultDemo(
        project=PROJECT_NAME, module=MODULE_NAME, version=MODULE_VERSION, demo_mode=DEMO_MODE,
        status=status, priority_attribute_active=request.priority_attribute.active, visible_as=visible_as,
        visibility_scope=visibility_scope, operational_hint_shared=operational_hint_shared, operational_hint=hint,
        authorized_staff_only=authorized_staff_only, alert_payload_demo=safe_alert_payload,
        blocks_trip_assistance_flow=blocks_trip_assistance_flow, risk_flags=_deduplicate(risk_flags),
        audit_flags=_deduplicate(audit_flags), privacy_notice=_privacy_notice(), legal_scope_notice=_legal_scope_notice(),
        warnings=_common_warnings(), timestamp_utc=datetime.now(timezone.utc).isoformat()
    )

def _alert_payload_demo(
    request: TripActivationRequestDemo, status: TripActivationStatus, visibility_scope: VisibilityScope,
    operational_hint_shared: bool, hint: ConsentedOperationalHint, authorized_staff_only: bool
) -> Dict[str, Any]:
    return {
        "trip_event_demo_id": request.validation_context.trip_event_demo_id,
        "transport_context": request.validation_context.transport_context.value,
        "status": status.value,
        "visible_as": "Usuario SUBE Prioridad" if request.priority_attribute.active else "Sin atributo SUBE Prioridad activo",
        "visibility_scope": visibility_scope.value,
        "operational_hint_shared": operational_hint_shared,
        "operational_hint": hint.value,
        "authorized_staff_only": authorized_staff_only,
        "contains_diagnosis": False,
        "contains_cud_visible": False,
        "contains_medical_certificate": False,
        "contains_identity_data": False,
        "driver_burden": "no_new_driver_obligation"
    }

def _privacy_notice() -> str:
    return "La activación por viaje no transmite DNI, nombre, diagnóstico, CUD visible, certificado médico, historia clínica, lesión, embarazo, tratamiento ni causa específica."

def _legal_scope_notice() -> str:
    return "Modelo conceptual sin integración real con SUBE, Red SUBE, Mi Argentina, validadores, molinetes, operadores ni bases estatales reales."

def _common_warnings() -> List[str]:
    return [
        "Sin integración real con SUBE.", "Sin integración real con Red SUBE.", "Sin integración real con Mi Argentina.",
        "Sin consulta a validadoras reales.", "Sin consulta a molinetes reales.", "Sin DNI.", "Sin diagnóstico.",
        "Sin CUD visible.", "Sin certificado médico.", "Sin saldo real.", "Sin tarifa real.", "Sin obligación nueva para choferes.",
        "El atributo activo no fuerza asistencia en todos los viajes.", "La visibilidad de calle es siempre genérica.",
        "El indicio operativo adicional sólo existe con consentimiento."
    ]

def _require_non_empty(payload: Dict[str, str]) -> None:
    for field_name, value in payload.items():
        if not value or not str(value).strip():
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
    print(json.dumps(run_silent_backup_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_station_hint_demo(), indent=2, ensure_ascii=False))

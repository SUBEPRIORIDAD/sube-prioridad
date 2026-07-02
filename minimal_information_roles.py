"""
SUBE Prioridad — Matriz demo de información mínima por rol.
Este módulo modela una regla estructural del proyecto:
 Cada actor del ecosistema SUBE Prioridad recibe únicamente la información
 mínima necesaria para cumplir su función.

Regla general:
 En calle, unidades, validadoras, molinetes y entorno operativo general,
 el usuario se muestra únicamente como:
 "Usuario SUBE Prioridad"
 sin revelar causa, diagnóstico, CUD visible, documentación médica,
 edad, embarazo, lesión, tratamiento, identidad civil ni historia clínica.

Excepción:
 En trenes, subtes, estaciones, andenes o plataformas puede compartirse
 un indicio operativo respetuoso con personal autorizado, sólo si el usuario
 prestó consentimiento expreso.

No integra SUBE real.
No integra Red SUBE real.
No integra Mi Argentina real.
No consulta bases estatales reales.
No consulta ANDIS real.
No consulta SISA real.
No consulta RENAPER real.
No consulta historias clínicas.
No usa DNI visible.
No usa diagnóstico.
No usa CUD visible.
No expone documentación médica.
No aplica beneficios tarifarios reales.
No modifica saldo.
No genera obligación nueva para choferes o personal operativo.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Matriz Demo de Información Mínima por Rol"
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
    "phone",
    "email",
    "correo",
    "diagnostico",
    "diagnóstico",
    "patologia",
    "patología",
    "enfermedad",
    "historia_clinica",
    "historia_clínica",
    "certificado_medico",
    "certificado_médico",
    "orden_medica",
    "orden_médica",
    "medico",
    "médico",
    "matricula",
    "matrícula",
    "obra_social",
    "cud",
    "certificado_unico_discapacidad",
    "certificado_único_discapacidad",
    "discapacidad",
    "embarazo",
    "embarazo_visible",
    "lesion",
    "lesión",
    "fractura",
    "tratamiento",
    "medicacion",
    "medicación",
    "saldo",
    "dinero",
    "tarifa",
    "gps",
    "latitud",
    "longitud",
    "latitude",
    "longitude",
    "imei",
    "mac",
}

class EcosystemRole(str, Enum):
    PRIORITY_USER = "priority_user"
    MI_ARGENTINA = "mi_argentina"
    RED_SUBE_BACKEND = "red_sube_backend"
    SUBE_ACCOUNT_FRONTEND = "sube_account_frontend"
    VALIDATOR_OR_TURNSTILE = "validator_or_turnstile"
    BUS_DRIVER = "bus_driver"
    TRAIN_GUARD = "train_guard"
    STATION_AUTHORIZED_STAFF = "station_authorized_staff"
    SECURITY_STAFF_STATION = "security_staff_station"
    TRANSPORT_OPERATOR_CONTROL_CENTER = "transport_operator_control_center"
    COLLABORATING_PASSENGER = "collaborating_passenger"
    AGGREGATE_ANALYTICS = "aggregate_analytics"
    PUBLIC_ENVIRONMENT = "public_environment"

class OperationalContext(str, Enum):
    GENERAL_STREET_OR_ONBOARD = "general_street_or_onboard"
    BUS_ONBOARD = "bus_onboard"
    TRAIN_ONBOARD = "train_onboard"
    SUBWAY_ONBOARD = "subway_onboard"
    TRAIN_STATION_WAIT = "train_station_wait"
    SUBWAY_STATION_WAIT = "subway_station_wait"
    TURNSTILE_ACCESS = "turnstile_access"
    PLATFORM_ACCESS_OR_DESCENT = "platform_access_or_descent"
    TERMINAL_OR_ASSISTED_CHANNEL = "terminal_or_assisted_channel"

class InformationSensitivity(str, Enum):
    PUBLIC_GENERIC = "public_generic"
    INTERNAL_TECHNICAL = "internal_technical"
    AUTHORIZED_OPERATIONAL = "authorized_operational"
    AGGREGATED_ANONYMIZED = "aggregated_anonymized"
    PROHIBITED = "prohibited"

class InformationItem(str, Enum):
    GENERIC_PRIORITY_LABEL = "generic_priority_label"
    PRIORITY_ATTRIBUTE_ACTIVE = "priority_attribute_active"
    PRIORITY_ATTRIBUTE_TOKEN = "priority_attribute_token"
    VALIDITY_WINDOW = "validity_window"
    PREFERENCE_PROFILE_TOKEN = "preference_profile_token"
    ASSISTANCE_MODE = "assistance_mode"
    VALIDATION_EVENT_TOKEN = "validation_event_token"
    TRANSPORT_CONTEXT_TOKEN = "transport_context_token"
    AUTHORIZED_STATION_HINT = "authorized_station_hint"
    ASSISTED_CHANNEL_REQUIRED = "assisted_channel_required"
    AGGREGATE_USAGE_METRIC = "aggregate_usage_metric"
    SOLIDARY_EVENT_TOKEN = "solidary_event_token"
    BONUS_ELIGIBILITY_DEMO_FLAG = "bonus_eligibility_demo_flag"
class ProhibitedInformationItem(str, Enum):
    DNI = "dni"
    NAME = "name"
    ADDRESS = "address"
    PHONE = "phone"
    EMAIL = "email"
    DIAGNOSIS = "diagnosis"
    CUD_VISIBLE = "cud_visible"
    MEDICAL_CERTIFICATE = "medical_certificate"
    CLINICAL_HISTORY = "clinical_history"
    MEDICAL_TREATMENT = "medical_treatment"
    SPECIFIC_CONDITION = "specific_condition"
    PREGNANCY_DETAIL = "pregnancy_detail"
    INJURY_DETAIL = "injury_detail"
    BALANCE = "balance"
    FARE = "fare"
    PRECISE_GEOLOCATION = "precise_geolocation"
    DEVICE_IDENTIFIER = "device_identifier"

class DisclosureDecision(str, Enum):
    ALLOWED = "allowed"
    ALLOWED_WITH_CONSENT = "allowed_with_consent"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"

@dataclass(frozen=True)
class MinimalInformationPolicy:
    role: EcosystemRole
    context: OperationalContext
    allowed_information: List[InformationItem]
    prohibited_information: List[ProhibitedInformationItem]
    sensitivity: InformationSensitivity
    consent_required: bool
    authorized_staff_only: bool
    public_visibility_label: str
    purpose: str

@dataclass(frozen=True)
class InformationDisclosureRequest:
    role: EcosystemRole
    context: OperationalContext
    requested_information: List[InformationItem]
    user_has_priority_attribute_active: bool
    user_consented_station_operational_hint: bool
    station_operational_hint_requested: bool
    purpose_token: str
    event_demo_token: str

@dataclass(frozen=True)
class InformationDisclosureResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    decision: DisclosureDecision
    role: EcosystemRole
    context: OperationalContext
    disclosed_information: List[InformationItem]
    blocked_information: List[str]
    public_visibility_label: str
    authorized_staff_only: bool
    consent_required: bool
    consent_present: bool
    minimum_information_applied: bool
    payload_demo: Dict[str, Any]
    risk_flags: List[str]
    audit_flags: List[str]
    privacy_notice: str
    legal_scope_notice: str
    warnings: List[str]
    timestamp_utc: str

def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """Mantiene compatibilidad hacia atrás si los tests unitarios de Actions invocan este método."""
    keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(keys.intersection(PROHIBITED_FIELDS))
    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )

def purge_prohibited_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sección XI y XXXVII del Pliego Técnico: Filtro de sanitización activa.
    Detecta y purga de forma irreversible cualquier campo restringido en el payload
    de entrada para evitar caídas del firmware ante JSONs pesados de Mi Argentina.
    """
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

def create_policy_for_role(
    role: EcosystemRole,
    context: OperationalContext = OperationalContext.GENERAL_STREET_OR_ONBOARD,
) -> MinimalInformationPolicy:
    if role == EcosystemRole.PRIORITY_USER:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.GENERIC_PRIORITY_LABEL,
                InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
                InformationItem.VALIDITY_WINDOW,
                InformationItem.PREFERENCE_PROFILE_TOKEN,
                InformationItem.ASSISTANCE_MODE,
                InformationItem.ASSISTED_CHANNEL_REQUIRED,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.INTERNAL_TECHNICAL,
            consent_required=False,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Permitir que el usuario conozca y administre su atributo y preferencias.",
        )
    if role == EcosystemRole.MI_ARGENTINA:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
                InformationItem.PRIORITY_ATTRIBUTE_TOKEN,
                InformationItem.VALIDITY_WINDOW,
                InformationItem.PREFERENCE_PROFILE_TOKEN,
                InformationItem.ASSISTANCE_MODE,
                InformationItem.ASSISTED_CHANNEL_REQUIRED,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.INTERNAL_TECHNICAL,
            consent_required=True,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Mostrar autorización demo y permitir consentimiento de activación.",
        )
    if role == EcosystemRole.RED_SUBE_BACKEND:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
                InformationItem.PRIORITY_ATTRIBUTE_TOKEN,
                InformationItem.VALIDITY_WINDOW,
                InformationItem.PREFERENCE_PROFILE_TOKEN,
                InformationItem.ASSISTANCE_MODE,
                InformationItem.TRANSPORT_CONTEXT_TOKEN,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.INTERNAL_TECHNICAL,
            consent_required=False,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Activar y sincronizar el atributo técnico sin exponer la causa.",
        )
    if role == EcosystemRole.SUBE_ACCOUNT_FRONTEND:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.GENERIC_PRIORITY_LABEL,
                InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
                InformationItem.VALIDITY_WINDOW,
                InformationItem.PREFERENCE_PROFILE_TOKEN,
                InformationItem.ASSISTANCE_MODE,
                InformationItem.ASSISTED_CHANNEL_REQUIRED,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.INTERNAL_TECHNICAL,
            consent_required=True,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Permitir configuración de preferencias desde canales SUBE demo.",
        )
    if role == EcosystemRole.VALIDATOR_OR_TURNSTILE:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.GENERIC_PRIORITY_LABEL,
                InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
                InformationItem.PREFERENCE_PROFILE_TOKEN,
                InformationItem.ASSISTANCE_MODE,
                InformationItem.VALIDATION_EVENT_TOKEN,
                InformationItem.TRANSPORT_CONTEXT_TOKEN,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.INTERNAL_TECHNICAL,
            consent_required=False,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Activar una señal genérica compatible con preferencias del usuario.",
        )
    if role == EcosystemRole.BUS_DRIVER:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.GENERIC_PRIORITY_LABEL,
                InformationItem.ASSISTANCE_MODE,
                InformationItem.TRANSPORT_CONTEXT_TOKEN,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.PUBLIC_GENERIC,
            consent_required=False,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Recibir, cuando corresponda, una señal operativa genérica sin nueva obligación.",
        )
    if role == EcosystemRole.TRAIN_GUARD:
        return _station_or_train_staff_policy(
            role=role,
            context=context,
            purpose="Recibir aviso operativo genérico o indicio consentido en contextos ferroviarios.",
        )
    if role == EcosystemRole.STATION_AUTHORIZED_STAFF:
        return _station_or_train_staff_policy(
            role=role,
            context=context,
            purpose="Asistir preventivamente en estación, andén, molinete o plataforma.",
        )
    if role == EcosystemRole.SECURITY_STAFF_STATION:
        return _station_or_train_staff_policy(
            role=role,
            context=context,
            purpose="Recibir indicio operativo respetuoso sólo con consentimiento y en contexto sensible.",
        )
    if role == EcosystemRole.TRANSPORT_OPERATOR_CONTROL_CENTER:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
                InformationItem.TRANSPORT_CONTEXT_TOKEN,
                InformationItem.VALIDATION_EVENT_TOKEN,
                InformationItem.AGGREGATE_USAGE_METRIC,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.INTERNAL_TECHNICAL,
            consent_required=False,
            authorized_staff_only=True,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Coordinar operación o análisis agregado sin datos sensibles.",
        )
    if role == EcosystemRole.COLLABORATING_PASSENGER:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.GENERIC_PRIORITY_LABEL,
                InformationItem.SOLIDARY_EVENT_TOKEN,
                InformationItem.BONUS_ELIGIBILITY_DEMO_FLAG,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.PUBLIC_GENERIC,
            consent_required=False,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Permitir colaboración voluntaria sin conocer causa ni identidad.",
        )
    if role == EcosystemRole.AGGREGATE_ANALYTICS:
        return MinimalInformationPolicy(
            role=role,
            context=context,
            allowed_information=[
                InformationItem.AGGREGATE_USAGE_METRIC,
                InformationItem.TRANSPORT_CONTEXT_TOKEN,
            ],
            prohibited_information=_all_prohibited_information(),
            sensitivity=InformationSensitivity.AGGREGATED_ANONYMIZED,
            consent_required=False,
            authorized_staff_only=False,
            public_visibility_label="Usuario SUBE Prioridad",
            purpose="Evaluar funcionamiento mediante datos agregados y anonimizados.",
        )
    return MinimalInformationPolicy(
        role=role,
        context=context,
        allowed_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
        ],
        prohibited_information=_all_prohibited_information(),
        sensitivity=InformationSensitivity.PUBLIC_GENERIC,
        consent_required=False,
        authorized_staff_only=False,
        public_visibility_label="Usuario SUBE Prioridad",
        purpose="Comunicación pública genérica sin datos sensibles.",
    )

def create_demo_information_disclosure_request(
    role: EcosystemRole = EcosystemRole.VALIDATOR_OR_TURNSTILE,
    context: OperationalContext = OperationalContext.GENERAL_STREET_OR_ONBOARD,
    requested_information: Optional[List[InformationItem]] = None,
    user_has_priority_attribute_active: bool = True,
    user_consented_station_operational_hint: bool = False,
    station_operational_hint_requested: bool = False,
    purpose_token: str = "demo-purpose-token-001",
    event_demo_token: str = "demo-event-token-001",
) -> InformationDisclosureRequest:
    
    raw_payload = {
        "purpose_token": purpose_token,
        "event_demo_token": event_demo_token,
    }
    
    sanitized_payload = purge_prohibited_fields(raw_payload)
    _require_non_empty(sanitized_payload)
    
    return InformationDisclosureRequest(
        role=role,
        context=context,
        requested_information=requested_information
        or [
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
        ],
        user_has_priority_attribute_active=user_has_priority_attribute_active,
        user_consented_station_operational_hint=user_consented_station_operational_hint,
        station_operational_hint_requested=station_operational_hint_requested,
        purpose_token=str(sanitized_payload.get("purpose_token", purpose_token)).strip(),
        event_demo_token=str(sanitized_payload.get("event_demo_token", event_demo_token)).strip(),
    )

def evaluate_minimal_information_disclosure(
    request: InformationDisclosureRequest,
) -> InformationDisclosureResult:
    policy = create_policy_for_role(
        role=request.role,
        context=request.context,
    )
    risk_flags = _risk_flags(request, policy)
    audit_flags = _audit_flags(request, policy)
    
    if not request.user_has_priority_attribute_active:
        return _result(
            request=request,
            policy=policy,
            decision=DisclosureDecision.BLOCKED,
            disclosed_information=[],
            blocked_information=["priority_attribute_not_active"],
            risk_flags=["priority_attribute_not_active"],
            audit_flags=audit_flags,
        )
    if risk_flags:
        return _result(
            request=request,
            policy=policy,
            decision=DisclosureDecision.BLOCKED,
            disclosed_information=[],
            blocked_information=risk_flags,
            risk_flags=risk_flags,
            audit_flags=audit_flags,
        )
        
    disclosed_information: List[InformationItem] = []
    blocked_information: List[str] = []
    
    for item in request.requested_information:
        if item in policy.allowed_information:
            disclosed_information.append(item)
        else:
            blocked_information.append(item.value)
            
    if (
        request.station_operational_hint_requested
        and InformationItem.AUTHORIZED_STATION_HINT not in disclosed_information
        and _can_share_station_hint(request, policy)
    ):
        disclosed_information.append(InformationItem.AUTHORIZED_STATION_HINT)
        
    if blocked_information:
        decision = DisclosureDecision.NEEDS_REVIEW
    elif (
        InformationItem.AUTHORIZED_STATION_HINT in disclosed_information
        and policy.consent_required
    ):
        decision = DisclosureDecision.ALLOWED_WITH_CONSENT
    else:
        decision = DisclosureDecision.ALLOWED
        
    return _result(
        request=request,
        policy=policy,
        decision=decision,
        disclosed_information=_deduplicate_items(disclosed_information),
        blocked_information=_deduplicate_strings(blocked_information),
        risk_flags=[],
        audit_flags=audit_flags,
    )
def result_to_dict(result: InformationDisclosureResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "decision": result.decision.value,
        "role": result.role.value,
        "context": result.context.value,
        "disclosed_information": [
            item.value for item in result.disclosed_information
        ],
        "blocked_information": result.blocked_information,
        "public_visibility_label": result.public_visibility_label,
        "authorized_staff_only": result.authorized_staff_only,
        "consent_required": result.consent_required,
        "consent_present": result.consent_present,
        "minimum_information_applied": result.minimum_information_applied,
        "payload_demo": result.payload_demo,
        "risk_flags": result.risk_flags,
        "audit_flags": result.audit_flags,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }

def run_demo() -> Dict[str, Any]:
    request = create_demo_information_disclosure_request()
    result = evaluate_minimal_information_disclosure(request)
    return result_to_dict(result)

def run_station_authorized_hint_demo() -> Dict[str, Any]:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.STATION_AUTHORIZED_STAFF,
        context=OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.AUTHORIZED_STATION_HINT,
        ],
        user_consented_station_operational_hint=True,
        station_operational_hint_requested=True,
    )
    result = evaluate_minimal_information_disclosure(request)
    return result_to_dict(result)

def run_collaborating_passenger_demo() -> Dict[str, Any]:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.COLLABORATING_PASSENGER,
        context=OperationalContext.GENERAL_STREET_OR_ONBOARD,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.SOLIDARY_EVENT_TOKEN,
            InformationItem.BONUS_ELIGIBILITY_DEMO_FLAG,
        ],
    )
    result = evaluate_minimal_information_disclosure(request)
    return result_to_dict(result)

def _station_or_train_staff_policy(
    role: EcosystemRole,
    context: OperationalContext,
    purpose: str,
) -> MinimalInformationPolicy:
    return MinimalInformationPolicy(
        role=role,
        context=context,
        allowed_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
            InformationItem.ASSISTANCE_MODE,
            InformationItem.TRANSPORT_CONTEXT_TOKEN,
            InformationItem.VALIDATION_EVENT_TOKEN,
            InformationItem.AUTHORIZED_STATION_HINT,
        ],
        prohibited_information=_all_prohibited_information(),
        sensitivity=InformationSensitivity.AUTHORIZED_OPERATIONAL,
        consent_required=True,
        authorized_staff_only=True,
        public_visibility_label="Usuario SUBE Prioridad",
        purpose=purpose,
    )

def _risk_flags(
    request: InformationDisclosureRequest,
    policy: MinimalInformationPolicy,
) -> List[str]:
    flags: List[str] = []
    if policy.public_visibility_label != "Usuario SUBE Prioridad":
        flags.append("invalid_public_visibility_label")
    if request.station_operational_hint_requested:
        if not _is_station_or_platform_context(request.context):
            flags.append("station_hint_requested_outside_station_context")
        if not policy.authorized_staff_only:
            flags.append("station_hint_requested_for_non_authorized_staff_role")
        if not request.user_consented_station_operational_hint:
            flags.append("station_hint_requested_without_user_consent")
    for item in request.requested_information:
        if item == InformationItem.AUTHORIZED_STATION_HINT:
            if not _can_share_station_hint(request, policy):
                flags.append("authorized_station_hint_not_allowed")
    return _deduplicate_strings(flags)

def _audit_flags(
    request: InformationDisclosureRequest,
    policy: MinimalInformationPolicy,
) -> List[str]:
    flags = [
        "minimum_information_policy",
        "street_visibility_generic_sube_prioridad",
        "no_diagnosis_visible",
        "no_cud_visible",
        "no_medical_certificate_visible",
        "no_identity_data_visible",
        "no_real_integration",
    ]
    if policy.authorized_staff_only:
        flags.append("authorized_staff_only_policy")
    if policy.consent_required:
        flags.append("consent_required_for_role_or_context")
    if request.user_consented_station_operational_hint:
        flags.append("station_operational_hint_user_consented")
    if request.role == EcosystemRole.COLLABORATING_PASSENGER:
        flags.append("collaborating_passenger_sees_no_cause")
    if request.role == EcosystemRole.BUS_DRIVER:
        flags.append("no_new_driver_obligation")
    if request.role == EcosystemRole.AGGREGATE_ANALYTICS:
        flags.append("aggregated_anonymized_use_only")
    return _deduplicate_strings(flags)

def _can_share_station_hint(
    request: InformationDisclosureRequest,
    policy: MinimalInformationPolicy,
) -> bool:
    return (
        request.station_operational_hint_requested
        and request.user_consented_station_operational_hint
        and policy.authorized_staff_only
        and policy.consent_required
        and _is_station_or_platform_context(request.context)
        and InformationItem.AUTHORIZED_STATION_HINT in policy.allowed_information
    )

def _is_station_or_platform_context(context: OperationalContext) -> bool:
    return context in {
        OperationalContext.TRAIN_STATION_WAIT,
        OperationalContext.SUBWAY_STATION_WAIT,
        OperationalContext.TURNSTILE_ACCESS,
        OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
        OperationalContext.TERMINAL_OR_ASSISTED_CHANNEL,
    }

def _result(
    request: InformationDisclosureRequest,
    policy: MinimalInformationPolicy,
    decision: DisclosureDecision,
    disclosed_information: List[InformationItem],
    blocked_information: List[str],
    risk_flags: List[str],
    audit_flags: List[str],
) -> InformationDisclosureResult:
    station_hint_shared = InformationItem.AUTHORIZED_STATION_HINT in disclosed_information
    
    # Doble blindaje: Filtramos el payload de salida simulado antes de retornarlo
    raw_payload = _payload_demo(
        request=request,
        policy=policy,
        disclosed_information=disclosed_information,
        station_hint_shared=station_hint_shared,
    )
    safe_payload = purge_prohibited_fields(raw_payload)

    return InformationDisclosureResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=MODULE_VERSION,
        demo_mode=DEMO_MODE,
        decision=decision,
        role=request.role,
        context=request.context,
        disclosed_information=disclosed_information,
        blocked_information=blocked_information,
        public_visibility_label=policy.public_visibility_label,
        authorized_staff_only=policy.authorized_staff_only and station_hint_shared,
        consent_required=policy.consent_required and station_hint_shared,
        consent_present=request.user_consented_station_operational_hint,
        minimum_information_applied=True,
        payload_demo=safe_payload,
        risk_flags=_deduplicate_strings(risk_flags),
        audit_flags=_deduplicate_strings(audit_flags),
        privacy_notice=_privacy_notice(),
        legal_scope_notice=_legal_scope_notice(),
        warnings=_common_warnings(),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )

def _payload_demo(
    request: InformationDisclosureRequest,
    policy: MinimalInformationPolicy,
    disclosed_information: List[InformationItem],
    station_hint_shared: bool,
) -> Dict[str, Any]:
    return {
        "event_demo_token": request.event_demo_token,
        "purpose_token": request.purpose_token,
        "role": request.role.value,
        "context": request.context.value,
        "visible_as": policy.public_visibility_label,
        "disclosed_information": [item.value for item in disclosed_information],
        "authorized_station_hint_shared": station_hint_shared,
        "authorized_staff_only": policy.authorized_staff_only and station_hint_shared,
        "contains_dni": False,
        "contains_name": False,
        "contains_address": False,
        "contains_phone": False,
        "contains_email": False,
        "contains_diagnosis": False,
        "contains_cud_visible": False,
        "contains_medical_certificate": False,
        "contains_clinical_history": False,
        "contains_specific_condition": False,
        "contains_balance": False,
        "contains_fare": False,
        "contains_precise_geolocation": False,
        "driver_burden": "no_new_driver_obligation",
        "purpose": policy.purpose,
    }

def _privacy_notice() -> str:
    return (
        "La matriz de información mínima impide transmitir DNI, nombre, "
        "domicilio, teléfono, email, diagnóstico, CUD visible, certificado "
        "médico, historia clínica, patología, tratamiento, lesión, embarazo "
        "identificado, saldo, tarifa o geolocalización precisa."
    )

def _legal_scope_notice() -> str:
    return (
        "Modelo conceptual sin integración real con SUBE, Red SUBE, Mi Argentina, "
        "ANDIS, SISA, RENAPER, validadores, molinetes, operadores ni bases "
        "estatales reales."
    )

def _common_warnings() -> List[str]:
    return [
    return {
        "event_demo_token": request.event_demo_token,
        "purpose_token": request.purpose_token,
        "role": request.role.value,
        "context": request.context.value,
        "visible_as": policy.public_visibility_label,
        "disclosed_information": [item.value for item in disclosed_information],
        "authorized_station_hint_shared": station_hint_shared,
        "authorized_staff_only": policy.authorized_staff_only and station_hint_shared,
        "contains_dni": False,
        "contains_name": False,
        "contains_address": False,
        "contains_phone": False,
        "contains_email": False,
        "contains_diagnosis": False,
        "contains_cud_visible": False,
        "contains_medical_certificate": False,
        "contains_clinical_history": False,
        "contains_specific_condition": False,
        "contains_balance": False,
        "contains_fare": False,
        "contains_precise_geolocation": False,
        "driver_burden": "no_new_driver_obligation",
        "purpose": policy.purpose,
    }

def _privacy_notice() -> str:
    return (
        "La matriz de información mínima impide transmitir DNI, nombre, "
        "domicilio, teléfono, email, diagnóstico, CUD visible, certificado "
        "médico, historia clínica, patología, tratamiento, lesión, embarazo "
        "identificado, saldo, tarifa o geolocalización precisa."
    )

def _legal_scope_notice() -> str:
    return (
        "Modelo conceptual sin integración real con SUBE, Red SUBE, Mi Argentina, "
        "ANDIS, SISA, RENAPER, validadores, molinetes, operadores ni bases "
        "estatales reales."
    )

def _common_warnings() -> List[str]:
    return [
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin integración real con Mi Argentina.",
        "Sin consulta a bases estatales reales.",
        "Sin DNI visible.",
        "Sin diagnóstico.",
        "Sin CUD visible.",
        "Sin certificado médico.",
        "Sin historia clínica.",
        "Sin saldo real.",
        "Sin tarifa real.",
        "Sin obligación nueva para choferes.",
        "La visibilidad pública es siempre genérica: Usuario SUBE Prioridad.",
        "El indicio operativo adicional sólo existe con consentimiento.",
        "El indicio operativo adicional sólo se comparte con personal autorizado.",
    ]

def _all_prohibited_information() -> List[ProhibitedInformationItem]:
    return [
        ProhibitedInformationItem.DNI,
        ProhibitedInformationItem.NAME,
        ProhibitedInformationItem.ADDRESS,
        ProhibitedInformationItem.PHONE,
        ProhibitedInformationItem.EMAIL,
        ProhibitedInformationItem.DIAGNOSIS,
        ProhibitedInformationItem.CUD_VISIBLE,
        ProhibitedInformationItem.MEDICAL_CERTIFICATE,
        ProhibitedInformationItem.CLINICAL_HISTORY,
        ProhibitedInformationItem.MEDICAL_TREATMENT,
        ProhibitedInformationItem.SPECIFIC_CONDITION,
        ProhibitedInformationItem.PREGNANCY_DETAIL,
        ProhibitedInformationItem.INJURY_DETAIL,
        ProhibitedInformationItem.BALANCE,
        ProhibitedInformationItem.FARE,
        ProhibitedInformationItem.PRECISE_GEOLOCATION,
        ProhibitedInformationItem.DEVICE_IDENTIFIER,
    ]

def _require_non_empty(payload: Dict[str, Any]) -> None:
    for field_name, value in payload.items():
        if not value or not str(value).strip():
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")

def _deduplicate_items(items: List[InformationItem]) -> List[InformationItem]:
    seen = set()
    result: List[InformationItem] = []
    for item in items:
        if item.value not in seen:
            seen.add(item.value)
            result.append(item)
    return result

def _deduplicate_strings(items: List[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_station_authorized_hint_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_collaborating_passenger_demo(), indent=2, ensure_ascii=False))

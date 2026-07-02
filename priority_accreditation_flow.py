"""
SUBE Prioridad — Flujo demo de acreditación previa y activación del atributo.

Este módulo modela la etapa anterior al uso del transporte:

    acreditación médica / administrativa previa
        ↓
    validación interinstitucional demo
        ↓
    autorización demo visible en Mi Argentina
        ↓
    consentimiento del usuario
        ↓
    sincronización demo con Red SUBE
        ↓
    atributo SUBE Prioridad activo

Regla central:
    En el funcionamiento de calle, toda persona con atributo activo se ve
    operativamente como "Usuario SUBE Prioridad", sin revelar causa, diagnóstico,
    CUD, lesión, embarazo, edad, tratamiento ni condición específica.

Excepción:
    En trenes, subtes, estaciones, andenes o plataformas, puede existir un
    indicio operativo respetuoso para personal autorizado, sólo si el usuario
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
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Flujo Demo de Acreditación Previa"
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
    "tratamiento",
    "medicacion",
    "medicación",
    "embarazo_visible",
    "lesion",
    "lesión",
    "fractura",
    "saldo",
    "dinero",
    "tarifa",
    "gps",
    "latitud",
    "longitud",
    "latitude",
    "longitude",
}


class AccreditationOrigin(str, Enum):
    MEDICAL_PROFESSIONAL_DEMO = "medical_professional_demo"
    PUBLIC_HEALTH_PROVIDER_DEMO = "public_health_provider_demo"
    STATE_PROGRAM_DEMO = "state_program_demo"
    CUD_INTEROPERABILITY_DEMO = "cud_interoperability_demo"
    ASSISTED_CHANNEL_DEMO = "assisted_channel_demo"
    MIXED_ADMINISTRATIVE_REVIEW_DEMO = "mixed_administrative_review_demo"


class AssistanceNeedKind(str, Enum):
    TEMPORARY_MEDICAL_RECOVERY = "temporary_medical_recovery"
    PREGNANCY_OR_GESTATIONAL_NEED = "pregnancy_or_gestational_need"
    OLDER_ADULT = "older_adult"
    REDUCED_MOBILITY = "reduced_mobility"
    CUD_RELATED_NEED = "cud_related_need"
    INVISIBLE_OR_NON_OBVIOUS_NEED = "invisible_or_non_obvious_need"
    STATE_PROGRAM_AUTHORIZED = "state_program_authorized"
    ABSTRACT_PREVIOUSLY_ACCREDITED_NEED = "abstract_previously_accredited_need"


class AccreditationStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    OBSERVED = "observed"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class MiArgentinaAuthorizationStatus(str, Enum):
    NOT_CREATED = "not_created"
    CREATED = "created"
    USER_NOTIFIED = "user_notified"
    USER_CONSENT_PENDING = "user_consent_pending"
    USER_CONSENT_ACCEPTED = "user_consent_accepted"
    USER_CONSENT_DECLINED = "user_consent_declined"


class RedSubeSyncStatus(str, Enum):
    NOT_READY = "not_ready"
    PENDING_SYNC = "pending_sync"
    SYNCED_ATTRIBUTE_PENDING_ACTIVATION = "synced_attribute_pending_activation"
    ACTIVE_ATTRIBUTE = "active_attribute"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PriorityAttributeVisibility(str, Enum):
    GENERIC_SUBE_PRIORIDAD = "generic_sube_prioridad"
    CONSENTED_OPERATIONAL_INDICATION = "consented_operational_indication"


class OperationalContext(str, Enum):
    BUS_OR_ONBOARD_VALIDATOR = "bus_or_onboard_validator"
    TRAIN_STATION_WAIT = "train_station_wait"
    SUBWAY_STATION_WAIT = "subway_station_wait"
    PLATFORM_ACCESS_OR_DESCENT = "platform_access_or_descent"
    TURNSTILE_ACCESS = "turnstile_access"
    GENERAL_TRANSPORT_CONTEXT = "general_transport_context"


class ConsentedOperationalIndication(str, Enum):
    NONE = "none"
    MAY_NEED_STATION_ASSISTANCE = "may_need_station_assistance"
    MAY_NEED_PLATFORM_ASSISTANCE = "may_need_platform_assistance"
    MAY_NEED_DESCENT_SUPPORT = "may_need_descent_support"
    MAY_NEED_DISCREET_SECURITY_NOTICE = "may_need_discreet_security_notice"
    MAY_NEED_NON_SPECIFIC_DECOMPENSATION_SUPPORT = (
        "may_need_non_specific_decompensation_support"
    )


@dataclass(frozen=True)
class AccreditationRequestDemo:
    request_demo_id: str
    origin: AccreditationOrigin
    assistance_need_kind: AssistanceNeedKind
    submitted_at_utc: datetime
    requested_valid_from_utc: datetime
    requested_valid_until_utc: Optional[datetime]
    supporting_evidence_token: str
    applicant_identity_token: str
    status: AccreditationStatus
    authority_review_token: Optional[str]
    rejection_reason_code: Optional[str]


@dataclass(frozen=True)
class InteragencyValidationDemo:
    validation_demo_id: str
    request_demo_id: str
    validating_authority_token: str
    validation_timestamp_utc: datetime
    approved: bool
    validity_from_utc: datetime
    validity_until_utc: Optional[datetime]
    abstract_priority_reason_token: str
    data_minimization_applied: bool
    sensitive_data_removed: bool
    warnings: List[str]


@dataclass(frozen=True)
class MiArgentinaAuthorizationDemo:
    mi_argentina_authorization_token: str
    request_demo_id: str
    applicant_identity_token: str
    status: MiArgentinaAuthorizationStatus
    authorization_code_demo: str
    visible_to_user: bool
    requires_user_consent: bool
    user_consented_priority_attribute_activation: bool
    user_consented_operational_indication: bool
    selected_operational_indication: ConsentedOperationalIndication
    created_at_utc: datetime
    expires_at_utc: Optional[datetime]


@dataclass(frozen=True)
class RedSubePriorityAttributeDemo:
    priority_attribute_token: str
    applicant_identity_token: str
    sube_account_demo_token: Optional[str]
    sube_card_demo_token: Optional[str]
    payment_method_demo_token: Optional[str]
    status: RedSubeSyncStatus
    active: bool
    valid_from_utc: datetime
    valid_until_utc: Optional[datetime]
    street_visibility: PriorityAttributeVisibility
    operational_indication_visibility: PriorityAttributeVisibility
    operational_indication: ConsentedOperationalIndication
    created_at_utc: datetime
    synced_at_utc: Optional[datetime]


@dataclass(frozen=True)
class AccreditationFlowRequestDemo:
    accreditation_request: AccreditationRequestDemo
    user_has_mi_argentina_access: bool
    user_has_sube_account: bool
    user_has_sube_card: bool
    user_has_mobile_device: bool
    assisted_channel_available: bool
    user_accepts_priority_attribute_activation: bool
    user_accepts_operational_indication_for_station_contexts: bool
    selected_operational_indication: ConsentedOperationalIndication
    sube_account_demo_token: Optional[str]
    sube_card_demo_token: Optional[str]
    payment_method_demo_token: Optional[str]


@dataclass(frozen=True)
class AccreditationFlowResultDemo:
    project: str
    module: str
    version: str
    demo_mode: bool
    accreditation_status: AccreditationStatus
    mi_argentina_status: MiArgentinaAuthorizationStatus
    red_sube_sync_status: RedSubeSyncStatus
    priority_attribute_active: bool
    visible_in_street_as: str
    operational_context_notice: Dict[str, Any]
    interagency_validation: Optional[InteragencyValidationDemo]
    mi_argentina_authorization: Optional[MiArgentinaAuthorizationDemo]
    red_sube_priority_attribute: Optional[RedSubePriorityAttributeDemo]
    blocks_activation: bool
    requires_assisted_channel: bool
    risk_flags: List[str]
    audit_flags: List[str]
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


def create_demo_accreditation_request(
    request_demo_id: str = "demo-accreditation-request-001",
    origin: AccreditationOrigin = AccreditationOrigin.MEDICAL_PROFESSIONAL_DEMO,
    assistance_need_kind: AssistanceNeedKind = AssistanceNeedKind.TEMPORARY_MEDICAL_RECOVERY,
    submitted_at_utc: Optional[datetime] = None,
    requested_valid_from_utc: Optional[datetime] = None,
    requested_valid_until_utc: Optional[datetime] = None,
    supporting_evidence_token: str = "demo-supporting-evidence-token-001",
    applicant_identity_token: str = "demo-identity-token-001",
    status: AccreditationStatus = AccreditationStatus.SUBMITTED,
    authority_review_token: Optional[str] = "demo-authority-review-token-001",
    rejection_reason_code: Optional[str] = None,
) -> AccreditationRequestDemo:
    now = submitted_at_utc or datetime.now(timezone.utc)
    valid_from = requested_valid_from_utc or now
    valid_until = requested_valid_until_utc or now + timedelta(days=90)

    payload = {
        "request_demo_id": request_demo_id,
        "supporting_evidence_token": supporting_evidence_token,
        "applicant_identity_token": applicant_identity_token,
    }

    assert_no_prohibited_fields(payload)
    _require_non_empty(payload)

    return AccreditationRequestDemo(
        request_demo_id=request_demo_id.strip(),
        origin=origin,
        assistance_need_kind=assistance_need_kind,
        submitted_at_utc=now,
        requested_valid_from_utc=valid_from,
        requested_valid_until_utc=valid_until,
        supporting_evidence_token=supporting_evidence_token.strip(),
        applicant_identity_token=applicant_identity_token.strip(),
        status=status,
        authority_review_token=(
            authority_review_token.strip() if authority_review_token else None
        ),
        rejection_reason_code=rejection_reason_code,
    )


def create_demo_accreditation_flow_request(
    accreditation_request: Optional[AccreditationRequestDemo] = None,
    user_has_mi_argentina_access: bool = True,
    user_has_sube_account: bool = True,
    user_has_sube_card: bool = True,
    user_has_mobile_device: bool = True,
    assisted_channel_available: bool = True,
    user_accepts_priority_attribute_activation: bool = True,
    user_accepts_operational_indication_for_station_contexts: bool = False,
    selected_operational_indication: ConsentedOperationalIndication = ConsentedOperationalIndication.NONE,
    sube_account_demo_token: Optional[str] = "demo-sube-account-001",
    sube_card_demo_token: Optional[str] = "demo-sube-card-001",
    payment_method_demo_token: Optional[str] = "demo-payment-method-001",
) -> AccreditationFlowRequestDemo:
    accreditation_request = accreditation_request or create_demo_accreditation_request()

    token_payload = {
        "sube_account_demo_token": sube_account_demo_token or "not-provided",
        "sube_card_demo_token": sube_card_demo_token or "not-provided",
        "payment_method_demo_token": payment_method_demo_token or "not-provided",
    }

    assert_no_prohibited_fields(token_payload)

    return AccreditationFlowRequestDemo(
        accreditation_request=accreditation_request,
        user_has_mi_argentina_access=user_has_mi_argentina_access,
        user_has_sube_account=user_has_sube_account,
        user_has_sube_card=user_has_sube_card,
        user_has_mobile_device=user_has_mobile_device,
        assisted_channel_available=assisted_channel_available,
        user_accepts_priority_attribute_activation=user_accepts_priority_attribute_activation,
        user_accepts_operational_indication_for_station_contexts=(
            user_accepts_operational_indication_for_station_contexts
        ),
        selected_operational_indication=selected_operational_indication,
        sube_account_demo_token=sube_account_demo_token,
        sube_card_demo_token=sube_card_demo_token,
        payment_method_demo_token=payment_method_demo_token,
    )


def simulate_priority_accreditation_flow(
    request: AccreditationFlowRequestDemo,
) -> AccreditationFlowResultDemo:
    risk_flags = _risk_flags(request)
    audit_flags = _audit_flags(request)

    if risk_flags:
        return _build_result(
            request=request,
            accreditation_status=request.accreditation_request.status,
            mi_argentina_status=MiArgentinaAuthorizationStatus.NOT_CREATED,
            red_sube_sync_status=RedSubeSyncStatus.NOT_READY,
            interagency_validation=None,
            mi_argentina_authorization=None,
            red_sube_priority_attribute=None,
            blocks_activation=True,
            requires_assisted_channel=_requires_assisted_channel(request),
            risk_flags=risk_flags,
            audit_flags=audit_flags,
        )

    interagency_validation = _create_interagency_validation(request)
    mi_argentina_authorization = _create_mi_argentina_authorization(
        request=request,
        validation=interagency_validation,
    )

    if not mi_argentina_authorization.user_consented_priority_attribute_activation:
        return _build_result(
            request=request,
            accreditation_status=AccreditationStatus.APPROVED,
            mi_argentina_status=MiArgentinaAuthorizationStatus.USER_CONSENT_DECLINED,
            red_sube_sync_status=RedSubeSyncStatus.NOT_READY,
            interagency_validation=interagency_validation,
            mi_argentina_authorization=mi_argentina_authorization,
            red_sube_priority_attribute=None,
            blocks_activation=True,
            requires_assisted_channel=_requires_assisted_channel(request),
            risk_flags=["user_declined_priority_attribute_activation"],
            audit_flags=audit_flags,
        )

    red_sube_priority_attribute = _create_red_sube_priority_attribute(
        request=request,
        validation=interagency_validation,
        mi_argentina_authorization=mi_argentina_authorization,
    )

    return _build_result(
        request=request,
        accreditation_status=AccreditationStatus.APPROVED,
        mi_argentina_status=MiArgentinaAuthorizationStatus.USER_CONSENT_ACCEPTED,
        red_sube_sync_status=RedSubeSyncStatus.ACTIVE_ATTRIBUTE,
        interagency_validation=interagency_validation,
        mi_argentina_authorization=mi_argentina_authorization,
        red_sube_priority_attribute=red_sube_priority_attribute,
        blocks_activation=False,
        requires_assisted_channel=_requires_assisted_channel(request),
        risk_flags=[],
        audit_flags=audit_flags,
    )


def build_operational_context_notice(
    attribute: Optional[RedSubePriorityAttributeDemo],
    context: OperationalContext,
) -> Dict[str, Any]:
    """
    Devuelve qué puede ver el entorno operativo según el contexto.

    Regla general:
        En calle/transporte común sólo se muestra "Usuario SUBE Prioridad".

    Excepción:
        En trenes, subtes, estaciones, andenes o plataformas se puede transmitir
        un indicio operativo respetuoso sólo si el usuario consintió esa capa.
    """
    if attribute is None or not attribute.active:
        return {
            "attribute_active": False,
            "visible_as": "no_priority_attribute",
            "operational_indication_shared": False,
            "operational_indication": ConsentedOperationalIndication.NONE.value,
            "authorized_staff_only": False,
        }

    station_context = context in {
        OperationalContext.TRAIN_STATION_WAIT,
        OperationalContext.SUBWAY_STATION_WAIT,
        OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
        OperationalContext.TURNSTILE_ACCESS,
    }

    has_consented_indication = (
        attribute.operational_indication_visibility
        == PriorityAttributeVisibility.CONSENTED_OPERATIONAL_INDICATION
        and attribute.operational_indication != ConsentedOperationalIndication.NONE
    )

    if station_context and has_consented_indication:
        return {
            "attribute_active": True,
            "visible_as": "Usuario SUBE Prioridad",
            "operational_indication_shared": True,
            "operational_indication": attribute.operational_indication.value,
            "authorized_staff_only": True,
            "privacy_rule": (
                "El indicio operativo no revela diagnóstico, CUD visible, "
                "documentación médica ni causa específica."
            ),
        }

    return {
        "attribute_active": True,
        "visible_as": "Usuario SUBE Prioridad",
        "operational_indication_shared": False,
        "operational_indication": ConsentedOperationalIndication.NONE.value,
        "authorized_staff_only": False,
        "privacy_rule": (
            "El entorno sólo recibe una señal genérica de SUBE Prioridad."
        ),
    }


def result_to_dict(result: AccreditationFlowResultDemo) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "accreditation_status": result.accreditation_status.value,
        "mi_argentina_status": result.mi_argentina_status.value,
        "red_sube_sync_status": result.red_sube_sync_status.value,
        "priority_attribute_active": result.priority_attribute_active,
        "visible_in_street_as": result.visible_in_street_as,
        "operational_context_notice": result.operational_context_notice,
        "interagency_validation": (
            _interagency_validation_to_dict(result.interagency_validation)
            if result.interagency_validation
            else None
        ),
        "mi_argentina_authorization": (
            _mi_argentina_authorization_to_dict(result.mi_argentina_authorization)
            if result.mi_argentina_authorization
            else None
        ),
        "red_sube_priority_attribute": (
            _red_sube_priority_attribute_to_dict(result.red_sube_priority_attribute)
            if result.red_sube_priority_attribute
            else None
        ),
        "blocks_activation": result.blocks_activation,
        "requires_assisted_channel": result.requires_assisted_channel,
        "risk_flags": result.risk_flags,
        "audit_flags": result.audit_flags,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    flow_request = create_demo_accreditation_flow_request()

    result = simulate_priority_accreditation_flow(flow_request)

    return result_to_dict(result)


def run_station_consent_demo() -> Dict[str, Any]:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_operational_indication_for_station_contexts=True,
        selected_operational_indication=(
            ConsentedOperationalIndication.MAY_NEED_PLATFORM_ASSISTANCE
        ),
    )

    result = simulate_priority_accreditation_flow(flow_request)

    if result.red_sube_priority_attribute is None:
        return result_to_dict(result)

    data = result_to_dict(result)
    data["station_context_notice"] = build_operational_context_notice(
        attribute=result.red_sube_priority_attribute,
        context=OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
    )

    return data


def run_no_consent_demo() -> Dict[str, Any]:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_priority_attribute_activation=True,
        user_accepts_operational_indication_for_station_contexts=False,
        selected_operational_indication=ConsentedOperationalIndication.NONE,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    if result.red_sube_priority_attribute is None:
        return result_to_dict(result)

    data = result_to_dict(result)
    data["station_context_notice"] = build_operational_context_notice(
        attribute=result.red_sube_priority_attribute,
        context=OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
    )

    return data


def _risk_flags(request: AccreditationFlowRequestDemo) -> List[str]:
    flags: List[str] = []
    accreditation = request.accreditation_request

    if accreditation.status in {
        AccreditationStatus.REJECTED,
        AccreditationStatus.OBSERVED,
        AccreditationStatus.EXPIRED,
    }:
        flags.append(f"accreditation_status_{accreditation.status.value}")

    if accreditation.requested_valid_until_utc is not None:
        if accreditation.requested_valid_until_utc <= datetime.now(timezone.utc):
            flags.append("requested_validity_expired")

        if accreditation.requested_valid_until_utc <= accreditation.requested_valid_from_utc:
            flags.append("invalid_validity_range")

    if not request.user_has_mi_argentina_access and not request.assisted_channel_available:
        flags.append("no_mi_argentina_access_and_no_assisted_channel")

    if not request.user_has_sube_account and not request.user_has_sube_card:
        flags.append("no_sube_account_or_card_available")

    if (
        request.user_accepts_operational_indication_for_station_contexts
        and request.selected_operational_indication
        == ConsentedOperationalIndication.NONE
    ):
        flags.append("operational_indication_consent_without_selected_indication")

    if (
        not request.user_accepts_operational_indication_for_station_contexts
        and request.selected_operational_indication
        != ConsentedOperationalIndication.NONE
    ):
        flags.append("selected_operational_indication_without_user_consent")

    return _deduplicate(flags)


def _audit_flags(request: AccreditationFlowRequestDemo) -> List[str]:
    flags = [
        "medical_or_administrative_accreditation_required_before_attribute",
        "mi_argentina_demo_authorization_layer",
        "red_sube_demo_sync_layer",
        "minimum_information_principle",
        "street_visibility_generic_sube_prioridad",
        "no_diagnosis_visible",
        "no_cud_visible",
        "no_real_integration",
    ]

    if request.accreditation_request.requested_valid_until_utc is not None:
        flags.append("temporary_validity_supported")

    if not request.user_has_mobile_device:
        flags.append("user_without_mobile_supported")

    if _requires_assisted_channel(request):
        flags.append("assisted_channel_required_or_recommended")

    if request.user_accepts_operational_indication_for_station_contexts:
        flags.append("consented_operational_indication_for_station_contexts")

    return _deduplicate(flags)


def _requires_assisted_channel(request: AccreditationFlowRequestDemo) -> bool:
    return (
        not request.user_has_mi_argentina_access
        or not request.user_has_mobile_device
        or not request.user_has_sube_account
    ) and request.assisted_channel_available


def _create_interagency_validation(
    request: AccreditationFlowRequestDemo,
) -> InteragencyValidationDemo:
    accreditation = request.accreditation_request
    now = datetime.now(timezone.utc)

    return InteragencyValidationDemo(
        validation_demo_id=f"validation-{accreditation.request_demo_id}",
        request_demo_id=accreditation.request_demo_id,
        validating_authority_token=(
            accreditation.authority_review_token
            or "demo-validating-authority-token"
        ),
        validation_timestamp_utc=now,
        approved=True,
        validity_from_utc=accreditation.requested_valid_from_utc,
        validity_until_utc=accreditation.requested_valid_until_utc,
        abstract_priority_reason_token="demo-abstract-priority-reason-token",
        data_minimization_applied=True,
        sensitive_data_removed=True,
        warnings=[
            "La validación demo no transmite diagnóstico.",
            "La validación demo no transmite CUD visible.",
            "La validación demo no transmite documentación médica al transporte.",
        ],
    )


def _create_mi_argentina_authorization(
    request: AccreditationFlowRequestDemo,
    validation: InteragencyValidationDemo,
) -> MiArgentinaAuthorizationDemo:
    accepted = request.user_accepts_priority_attribute_activation
    status = (
        MiArgentinaAuthorizationStatus.USER_CONSENT_ACCEPTED
        if accepted
        else MiArgentinaAuthorizationStatus.USER_CONSENT_DECLINED
    )

    selected_indication = (
        request.selected_operational_indication
        if request.user_accepts_operational_indication_for_station_contexts
        else ConsentedOperationalIndication.NONE
    )

    return MiArgentinaAuthorizationDemo(
        mi_argentina_authorization_token=(
            f"mi-argentina-auth-{request.accreditation_request.request_demo_id}"
        ),
        request_demo_id=request.accreditation_request.request_demo_id,
        applicant_identity_token=request.accreditation_request.applicant_identity_token,
        status=status,
        authorization_code_demo="DEMO-SUBE-PRIORIDAD-001",
        visible_to_user=True,
        requires_user_consent=True,
        user_consented_priority_attribute_activation=accepted,
        user_consented_operational_indication=(
            request.user_accepts_operational_indication_for_station_contexts
        ),
        selected_operational_indication=selected_indication,
        created_at_utc=datetime.now(timezone.utc),
        expires_at_utc=validation.validity_until_utc,
    )


def _create_red_sube_priority_attribute(
    request: AccreditationFlowRequestDemo,
    validation: InteragencyValidationDemo,
    mi_argentina_authorization: MiArgentinaAuthorizationDemo,
) -> RedSubePriorityAttributeDemo:
    operational_visibility = (
        PriorityAttributeVisibility.CONSENTED_OPERATIONAL_INDICATION
        if mi_argentina_authorization.user_consented_operational_indication
        else PriorityAttributeVisibility.GENERIC_SUBE_PRIORIDAD
    )

    operational_indication = (
        mi_argentina_authorization.selected_operational_indication
        if mi_argentina_authorization.user_consented_operational_indication
        else ConsentedOperationalIndication.NONE
    )

    return RedSubePriorityAttributeDemo(
        priority_attribute_token=(
            f"priority-attribute-{request.accreditation_request.request_demo_id}"
        ),
        applicant_identity_token=request.accreditation_request.applicant_identity_token,
        sube_account_demo_token=request.sube_account_demo_token,
        sube_card_demo_token=request.sube_card_demo_token,
        payment_method_demo_token=request.payment_method_demo_token,
        status=RedSubeSyncStatus.ACTIVE_ATTRIBUTE,
        active=True,
        valid_from_utc=validation.validity_from_utc,
        valid_until_utc=validation.validity_until_utc,
        street_visibility=PriorityAttributeVisibility.GENERIC_SUBE_PRIORIDAD,
        operational_indication_visibility=operational_visibility,
        operational_indication=operational_indication,
        created_at_utc=datetime.now(timezone.utc),
        synced_at_utc=datetime.now(timezone.utc),
    )


def _build_result(
    request: AccreditationFlowRequestDemo,
    accreditation_status: AccreditationStatus,
    mi_argentina_status: MiArgentinaAuthorizationStatus,
    red_sube_sync_status: RedSubeSyncStatus,
    interagency_validation: Optional[InteragencyValidationDemo],
    mi_argentina_authorization: Optional[MiArgentinaAuthorizationDemo],
    red_sube_priority_attribute: Optional[RedSubePriorityAttributeDemo],
    blocks_activation: bool,
    requires_assisted_channel: bool,
    risk_flags: List[str],
    audit_flags: List[str],
) -> AccreditationFlowResultDemo:
    priority_attribute_active = (
        red_sube_priority_attribute.active
        if red_sube_priority_attribute is not None
        else False
    )

    operational_notice = build_operational_context_notice(
        attribute=red_sube_priority_attribute,
        context=OperationalContext.GENERAL_TRANSPORT_CONTEXT,
    )

    return AccreditationFlowResultDemo(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=MODULE_VERSION,
        demo_mode=DEMO_MODE,
        accreditation_status=accreditation_status,
        mi_argentina_status=mi_argentina_status,
        red_sube_sync_status=red_sube_sync_status,
        priority_attribute_active=priority_attribute_active,
        visible_in_street_as=(
            "Usuario SUBE Prioridad"
            if priority_attribute_active
            else "Sin atributo SUBE Prioridad activo"
        ),
        operational_context_notice=operational_notice,
        interagency_validation=interagency_validation,
        mi_argentina_authorization=mi_argentina_authorization,
        red_sube_priority_attribute=red_sube_priority_attribute,
        blocks_activation=blocks_activation,
        requires_assisted_channel=requires_assisted_channel,
        risk_flags=risk_flags,
        audit_flags=audit_flags,
        privacy_notice=_privacy_notice(),
        legal_scope_notice=_legal_scope_notice(),
        warnings=_common_warnings(),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )


def _interagency_validation_to_dict(
    validation: InteragencyValidationDemo,
) -> Dict[str, Any]:
    return {
        "validation_demo_id": validation.validation_demo_id,
        "request_demo_id": validation.request_demo_id,
        "validating_authority_token": validation.validating_authority_token,
        "validation_timestamp_utc": validation.validation_timestamp_utc.isoformat(),
        "approved": validation.approved,
        "validity_from_utc": validation.validity_from_utc.isoformat(),
        "validity_until_utc": (
            validation.validity_until_utc.isoformat()
            if validation.validity_until_utc
            else None
        ),
        "abstract_priority_reason_token": validation.abstract_priority_reason_token,
        "data_minimization_applied": validation.data_minimization_applied,
        "sensitive_data_removed": validation.sensitive_data_removed,
        "warnings": validation.warnings,
    }


def _mi_argentina_authorization_to_dict(
    authorization: MiArgentinaAuthorizationDemo,
) -> Dict[str, Any]:
    return {
        "mi_argentina_authorization_token": authorization.mi_argentina_authorization_token,
        "request_demo_id": authorization.request_demo_id,
        "applicant_identity_token": authorization.applicant_identity_token,
        "status": authorization.status.value,
        "authorization_code_demo": authorization.authorization_code_demo,
        "visible_to_user": authorization.visible_to_user,
        "requires_user_consent": authorization.requires_user_consent,
        "user_consented_priority_attribute_activation": (
            authorization.user_consented_priority_attribute_activation
        ),
        "user_consented_operational_indication": (
            authorization.user_consented_operational_indication
        ),
        "selected_operational_indication": (
            authorization.selected_operational_indication.value
        ),
        "created_at_utc": authorization.created_at_utc.isoformat(),
        "expires_at_utc": (
            authorization.expires_at_utc.isoformat()
            if authorization.expires_at_utc
            else None
        ),
    }


def _red_sube_priority_attribute_to_dict(
    attribute: RedSubePriorityAttributeDemo,
) -> Dict[str, Any]:
    return {
        "priority_attribute_token": attribute.priority_attribute_token,
        "applicant_identity_token": attribute.applicant_identity_token,
        "sube_account_demo_token": attribute.sube_account_demo_token,
        "sube_card_demo_token": attribute.sube_card_demo_token,
        "payment_method_demo_token": attribute.payment_method_demo_token,
        "status": attribute.status.value,
        "active": attribute.active,
        "valid_from_utc": attribute.valid_from_utc.isoformat(),
        "valid_until_utc": (
            attribute.valid_until_utc.isoformat()
            if attribute.valid_until_utc
            else None
        ),
        "street_visibility": attribute.street_visibility.value,
        "operational_indication_visibility": (
            attribute.operational_indication_visibility.value
        ),
        "operational_indication": attribute.operational_indication.value,
        "created_at_utc": attribute.created_at_utc.isoformat(),
        "synced_at_utc": (
            attribute.synced_at_utc.isoformat()
            if attribute.synced_at_utc
            else None
        ),
    }


def _privacy_notice() -> str:
    return (
        "El flujo demo usa tokens técnicos y no transmite al transporte DNI, "
        "nombre, diagnóstico, CUD visible, certificado médico, historia clínica, "
        "tratamiento, patología ni documentación médica."
    )


def _legal_scope_notice() -> str:
    return (
        "Modelo conceptual sin integración real con Mi Argentina, Red SUBE, "
        "SUBE, ANDIS, SISA, RENAPER, organismos estatales, validadores, "
        "molinetes ni tarjetas reales."
    )


def _common_warnings() -> List[str]:
    return [
        "Sin integración real con Mi Argentina.",
        "Sin integración real con Red SUBE.",
        "Sin integración real con SUBE.",
        "Sin consulta a bases estatales reales.",
        "Sin consulta a documentación médica real.",
        "Sin DNI visible.",
        "Sin diagnóstico.",
        "Sin CUD visible.",
        "Sin historia clínica.",
        "Sin saldo real.",
        "Sin tarifa real.",
        "Sin beneficio económico real.",
        "La visibilidad de calle es siempre genérica: Usuario SUBE Prioridad.",
        "El indicio operativo adicional sólo existe con consentimiento.",
        "El indicio operativo adicional sólo se comparte con personal autorizado.",
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
    print(json.dumps(run_station_consent_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_no_consent_demo(), indent=2, ensure_ascii=False))

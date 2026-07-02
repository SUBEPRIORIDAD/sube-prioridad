"""
SUBE Prioridad — Flujo real principal de usuario.

Este módulo integra el flujo base:

    1. ¿Quién acredita?
       Médico, institución de salud u organismo autorizado.

    2. ¿Quién activa?
       Mi Argentina / sistema estatal autoriza.
       Red SUBE activa el atributo técnico.

    3. ¿Cómo lo usa la persona?
       Viaja normalmente y valida su medio de pago.

    4. ¿Qué ve el sistema?
       Atributo activo, vigencia, preferencias, contexto y validación pagada.

    5. ¿Qué ve la calle?
       Sólo "Usuario SUBE Prioridad".

    6. Excepción:
       En trenes, subtes, estaciones, andenes o plataformas puede compartirse
       un indicio operativo respetuoso sólo con consentimiento expreso y sólo
       con personal autorizado.

No integra SUBE real.
No integra Red SUBE real.
No integra Mi Argentina real.
No consulta bases reales.
No usa DNI.
No usa diagnóstico.
No usa CUD visible.
No expone causa médica.
No modifica saldo.
No aplica beneficios reales.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Flujo Real Principal Demo"
MODULE_VERSION = "0.1.0"
DEMO_MODE = True


class AccreditationActor(str, Enum):
    MEDICAL_PROFESSIONAL = "medical_professional"
    HEALTH_INSTITUTION = "health_institution"
    STATE_AGENCY = "state_agency"
    ANDIS_OR_CUD_INTEROPERABILITY = "andis_or_cud_interoperability"
    ASSISTED_ADMINISTRATIVE_CHANNEL = "assisted_administrative_channel"


class ActivationActor(str, Enum):
    MI_ARGENTINA = "mi_argentina"
    RED_SUBE = "red_sube"
    SUBE_ACCOUNT = "sube_account"
    ASSISTED_SUBE_CHANNEL = "assisted_sube_channel"


class TransportContext(str, Enum):
    BUS_ONBOARD = "bus_onboard"
    TRAIN_ONBOARD = "train_onboard"
    SUBWAY_ONBOARD = "subway_onboard"
    TRAIN_STATION_WAIT = "train_station_wait"
    SUBWAY_STATION_WAIT = "subway_station_wait"
    TURNSTILE_ACCESS = "turnstile_access"
    PLATFORM_ACCESS_OR_DESCENT = "platform_access_or_descent"


class UserPreferenceMode(str, Enum):
    SILENT = "silent"
    PASSIVE = "passive"
    DISCREET = "discreet"
    VISIBLE_GENERIC = "visible_generic"
    AUTHORIZED_STAFF_WITH_CONSENTED_HINT = "authorized_staff_with_consented_hint"


class CoreFlowStatus(str, Enum):
    ATTRIBUTE_NOT_ACTIVE = "attribute_not_active"
    READY_FOR_TRIP = "ready_for_trip"
    TRIP_VALIDATED_SILENT = "trip_validated_silent"
    TRIP_VALIDATED_PASSIVE = "trip_validated_passive"
    TRIP_VALIDATED_GENERIC_VISIBLE = "trip_validated_generic_visible"
    TRIP_VALIDATED_AUTHORIZED_STAFF_NOTICE = "trip_validated_authorized_staff_notice"
    REJECTED = "rejected"


class OperationalHint(str, Enum):
    NONE = "none"
    MAY_NEED_STATION_ASSISTANCE = "may_need_station_assistance"
    MAY_NEED_PLATFORM_ASSISTANCE = "may_need_platform_assistance"
    MAY_NEED_DESCENT_SUPPORT = "may_need_descent_support"
    MAY_NEED_DISCREET_SECURITY_NOTICE = "may_need_discreet_security_notice"


@dataclass(frozen=True)
class AccreditationDemo:
    actor: AccreditationActor
    need_accredited: bool
    valid_from_utc: datetime
    valid_until_utc: Optional[datetime]
    authorization_token: str


@dataclass(frozen=True)
class ActivationDemo:
    mi_argentina_authorized: bool
    red_sube_attribute_active: bool
    activation_actor: ActivationActor
    priority_attribute_token: str
    user_consented_attribute_activation: bool


@dataclass(frozen=True)
class TripUseDemo:
    transport_context: TransportContext
    validation_paid: bool
    preference_mode: UserPreferenceMode
    user_consented_operational_hint: bool
    operational_hint: OperationalHint


@dataclass(frozen=True)
class CoreUserFlowRequest:
    accreditation: AccreditationDemo
    activation: ActivationDemo
    trip: TripUseDemo


@dataclass(frozen=True)
class CoreUserFlowResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: CoreFlowStatus
    accredited_by: AccreditationActor
    activated_by: ActivationActor
    priority_attribute_active: bool
    visible_to_public_as: str
    system_view: Dict[str, Any]
    operational_view: Dict[str, Any]
    risk_flags: List[str]
    audit_flags: List[str]
    privacy_notice: str
    legal_scope_notice: str
    timestamp_utc: str


def create_demo_core_user_flow_request(
    actor: AccreditationActor = AccreditationActor.MEDICAL_PROFESSIONAL,
    activation_actor: ActivationActor = ActivationActor.RED_SUBE,
    transport_context: TransportContext = TransportContext.BUS_ONBOARD,
    preference_mode: UserPreferenceMode = UserPreferenceMode.PASSIVE,
    user_consented_operational_hint: bool = False,
    operational_hint: OperationalHint = OperationalHint.NONE,
) -> CoreUserFlowRequest:
    now = datetime.now(timezone.utc)

    accreditation = AccreditationDemo(
        actor=actor,
        need_accredited=True,
        valid_from_utc=now - timedelta(days=1),
        valid_until_utc=now + timedelta(days=90),
        authorization_token="demo-authorization-token-001",
    )

    activation = ActivationDemo(
        mi_argentina_authorized=True,
        red_sube_attribute_active=True,
        activation_actor=activation_actor,
        priority_attribute_token="demo-priority-attribute-token-001",
        user_consented_attribute_activation=True,
    )

    trip = TripUseDemo(
        transport_context=transport_context,
        validation_paid=True,
        preference_mode=preference_mode,
        user_consented_operational_hint=user_consented_operational_hint,
        operational_hint=operational_hint,
    )

    return CoreUserFlowRequest(
        accreditation=accreditation,
        activation=activation,
        trip=trip,
    )


def evaluate_core_user_flow(
    request: CoreUserFlowRequest,
) -> CoreUserFlowResult:
    risk_flags = _risk_flags(request)
    audit_flags = _audit_flags(request)

    if risk_flags:
        return _result(
            request=request,
            status=CoreFlowStatus.REJECTED,
            priority_attribute_active=False,
            risk_flags=risk_flags,
            audit_flags=audit_flags,
        )

    if not request.activation.red_sube_attribute_active:
        return _result(
            request=request,
            status=CoreFlowStatus.ATTRIBUTE_NOT_ACTIVE,
            priority_attribute_active=False,
            risk_flags=[],
            audit_flags=audit_flags,
        )

    status = _resolve_trip_status(request)

    return _result(
        request=request,
        status=status,
        priority_attribute_active=True,
        risk_flags=[],
        audit_flags=audit_flags,
    )


def result_to_dict(result: CoreUserFlowResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "accredited_by": result.accredited_by.value,
        "activated_by": result.activated_by.value,
        "priority_attribute_active": result.priority_attribute_active,
        "visible_to_public_as": result.visible_to_public_as,
        "system_view": result.system_view,
        "operational_view": result.operational_view,
        "risk_flags": result.risk_flags,
        "audit_flags": result.audit_flags,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    result = evaluate_core_user_flow(
        create_demo_core_user_flow_request()
    )

    return result_to_dict(result)


def run_station_consent_demo() -> Dict[str, Any]:
    request = create_demo_core_user_flow_request(
        transport_context=TransportContext.PLATFORM_ACCESS_OR_DESCENT,
        preference_mode=UserPreferenceMode.AUTHORIZED_STAFF_WITH_CONSENTED_HINT,
        user_consented_operational_hint=True,
        operational_hint=OperationalHint.MAY_NEED_PLATFORM_ASSISTANCE,
    )

    result = evaluate_core_user_flow(request)

    return result_to_dict(result)


def run_no_consent_station_demo() -> Dict[str, Any]:
    request = create_demo_core_user_flow_request(
        transport_context=TransportContext.PLATFORM_ACCESS_OR_DESCENT,
        preference_mode=UserPreferenceMode.AUTHORIZED_STAFF_WITH_CONSENTED_HINT,
        user_consented_operational_hint=False,
        operational_hint=OperationalHint.NONE,
    )

    result = evaluate_core_user_flow(request)

    return result_to_dict(result)


def _risk_flags(request: CoreUserFlowRequest) -> List[str]:
    flags: List[str] = []

    now = datetime.now(timezone.utc)

    if not request.accreditation.need_accredited:
        flags.append("need_not_accredited")

    if request.accreditation.valid_until_utc is not None:
        if request.accreditation.valid_until_utc <= now:
            flags.append("accreditation_expired")

        if request.accreditation.valid_until_utc <= request.accreditation.valid_from_utc:
            flags.append("invalid_accreditation_validity_range")

    if not request.activation.mi_argentina_authorized:
        flags.append("mi_argentina_authorization_missing")

    if not request.activation.user_consented_attribute_activation:
        flags.append("user_did_not_consent_attribute_activation")

    if not request.trip.validation_paid:
        flags.append("trip_validation_not_paid")

    if (
        request.trip.operational_hint != OperationalHint.NONE
        and not request.trip.user_consented_operational_hint
    ):
        flags.append("operational_hint_without_user_consent")

    if (
        request.trip.preference_mode
        == UserPreferenceMode.AUTHORIZED_STAFF_WITH_CONSENTED_HINT
        and request.trip.user_consented_operational_hint
        and request.trip.operational_hint == OperationalHint.NONE
    ):
        flags.append("consent_without_operational_hint")

    return _deduplicate(flags)


def _audit_flags(request: CoreUserFlowRequest) -> List[str]:
    flags = [
        "medical_or_administrative_accreditation_before_attribute",
        "mi_argentina_authorization_layer",
        "red_sube_attribute_activation_layer",
        "trip_validation_required",
        "public_visibility_generic_only",
        "no_diagnosis_visible",
        "no_cud_visible",
        "minimum_information_principle",
        "no_real_integration",
    ]

    if request.trip.transport_context in {
        TransportContext.TRAIN_STATION_WAIT,
        TransportContext.SUBWAY_STATION_WAIT,
        TransportContext.TURNSTILE_ACCESS,
        TransportContext.PLATFORM_ACCESS_OR_DESCENT,
    }:
        flags.append("station_platform_context")

    if request.trip.user_consented_operational_hint:
        flags.append("consented_operational_hint")

    return _deduplicate(flags)


def _resolve_trip_status(request: CoreUserFlowRequest) -> CoreFlowStatus:
    mode = request.trip.preference_mode

    if mode == UserPreferenceMode.SILENT:
        return CoreFlowStatus.TRIP_VALIDATED_SILENT

    if mode in {
        UserPreferenceMode.PASSIVE,
        UserPreferenceMode.DISCREET,
    }:
        return CoreFlowStatus.TRIP_VALIDATED_PASSIVE

    if mode == UserPreferenceMode.VISIBLE_GENERIC:
        return CoreFlowStatus.TRIP_VALIDATED_GENERIC_VISIBLE

    if (
        mode == UserPreferenceMode.AUTHORIZED_STAFF_WITH_CONSENTED_HINT
        and request.trip.user_consented_operational_hint
        and request.trip.operational_hint != OperationalHint.NONE
        and _is_station_or_platform_context(request.trip.transport_context)
    ):
        return CoreFlowStatus.TRIP_VALIDATED_AUTHORIZED_STAFF_NOTICE

    return CoreFlowStatus.TRIP_VALIDATED_PASSIVE


def _result(
    request: CoreUserFlowRequest,
    status: CoreFlowStatus,
    priority_attribute_active: bool,
    risk_flags: List[str],
    audit_flags: List[str],
) -> CoreUserFlowResult:
    operational_hint_shared = (
        status == CoreFlowStatus.TRIP_VALIDATED_AUTHORIZED_STAFF_NOTICE
    )

    return CoreUserFlowResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=MODULE_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        accredited_by=request.accreditation.actor,
        activated_by=request.activation.activation_actor,
        priority_attribute_active=priority_attribute_active,
        visible_to_public_as=(
            "Usuario SUBE Prioridad"
            if priority_attribute_active
            else "Sin atributo SUBE Prioridad activo"
        ),
        system_view={
            "need_accredited": request.accreditation.need_accredited,
            "mi_argentina_authorized": request.activation.mi_argentina_authorized,
            "red_sube_attribute_active": request.activation.red_sube_attribute_active,
            "priority_attribute_token": request.activation.priority_attribute_token,
            "valid_from_utc": request.accreditation.valid_from_utc.isoformat(),
            "valid_until_utc": (
                request.accreditation.valid_until_utc.isoformat()
                if request.accreditation.valid_until_utc
                else None
            ),
            "validation_paid": request.trip.validation_paid,
            "transport_context": request.trip.transport_context.value,
            "preference_mode": request.trip.preference_mode.value,
        },
        operational_view={
            "visible_as": (
                "Usuario SUBE Prioridad"
                if priority_attribute_active
                else "Sin atributo SUBE Prioridad activo"
            ),
            "operational_hint_shared": operational_hint_shared,
            "operational_hint": (
                request.trip.operational_hint.value
                if operational_hint_shared
                else OperationalHint.NONE.value
            ),
            "authorized_staff_only": operational_hint_shared,
            "contains_diagnosis": False,
            "contains_cud_visible": False,
            "contains_medical_certificate": False,
            "contains_identity_data": False,
            "driver_burden": "no_new_driver_obligation",
        },
        risk_flags=_deduplicate(risk_flags),
        audit_flags=_deduplicate(audit_flags),
        privacy_notice=(
            "El flujo no expone DNI, nombre, diagnóstico, CUD visible, "
            "certificado médico, historia clínica ni causa de la prioridad."
        ),
        legal_scope_notice=(
            "Modelo conceptual sin integración real con Mi Argentina, Red SUBE, "
            "SUBE, bases estatales, validadoras, molinetes ni tarjetas reales."
        ),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )


def _is_station_or_platform_context(context: TransportContext) -> bool:
    return context in {
        TransportContext.TRAIN_STATION_WAIT,
        TransportContext.SUBWAY_STATION_WAIT,
        TransportContext.TURNSTILE_ACCESS,
        TransportContext.PLATFORM_ACCESS_OR_DESCENT,
    }


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
    print(json.dumps(run_no_consent_station_demo(), indent=2, ensure_ascii=False))

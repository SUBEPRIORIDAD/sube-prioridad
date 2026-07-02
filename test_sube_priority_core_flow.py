"""
Tests — SUBE Prioridad: flujo real principal de usuario.

Verifica:

- quién acredita la prioridad;
- quién activa el atributo;
- cómo lo usa la persona en el viaje;
- qué ve el sistema;
- qué ve la calle;
- que no se exponga diagnóstico, CUD visible ni causa médica;
- que el indicio operativo sólo se comparta con consentimiento y en contexto habilitado.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sube_priority_core_flow import (
    AccreditationActor,
    ActivationActor,
    CoreFlowStatus,
    OperationalHint,
    TransportContext,
    UserPreferenceMode,
    AccreditationDemo,
    ActivationDemo,
    TripUseDemo,
    CoreUserFlowRequest,
    create_demo_core_user_flow_request,
    evaluate_core_user_flow,
    result_to_dict,
    run_demo,
    run_no_consent_station_demo,
    run_station_consent_demo,
)


def test_run_demo_models_basic_real_user_flow() -> None:
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["demo_mode"] is True
    assert result["status"] == CoreFlowStatus.TRIP_VALIDATED_PASSIVE.value
    assert result["accredited_by"] == AccreditationActor.MEDICAL_PROFESSIONAL.value
    assert result["activated_by"] == ActivationActor.RED_SUBE.value
    assert result["priority_attribute_active"] is True
    assert result["visible_to_public_as"] == "Usuario SUBE Prioridad"

    assert result["system_view"]["need_accredited"] is True
    assert result["system_view"]["mi_argentina_authorized"] is True
    assert result["system_view"]["red_sube_attribute_active"] is True
    assert result["system_view"]["validation_paid"] is True

    assert result["operational_view"]["visible_as"] == "Usuario SUBE Prioridad"
    assert result["operational_view"]["contains_diagnosis"] is False
    assert result["operational_view"]["contains_cud_visible"] is False
    assert result["operational_view"]["contains_medical_certificate"] is False
    assert result["operational_view"]["contains_identity_data"] is False


def test_medical_or_administrative_accreditation_comes_before_attribute() -> None:
    request = create_demo_core_user_flow_request(
        actor=AccreditationActor.HEALTH_INSTITUTION,
        activation_actor=ActivationActor.MI_ARGENTINA,
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.TRIP_VALIDATED_PASSIVE
    assert result.accredited_by == AccreditationActor.HEALTH_INSTITUTION
    assert result.activated_by == ActivationActor.MI_ARGENTINA
    assert result.priority_attribute_active is True
    assert "medical_or_administrative_accreditation_before_attribute" in result.audit_flags
    assert "mi_argentina_authorization_layer" in result.audit_flags
    assert "red_sube_attribute_activation_layer" in result.audit_flags


def test_need_not_accredited_rejects_flow() -> None:
    now = datetime.now(timezone.utc)

    request = CoreUserFlowRequest(
        accreditation=AccreditationDemo(
            actor=AccreditationActor.MEDICAL_PROFESSIONAL,
            need_accredited=False,
            valid_from_utc=now - timedelta(days=1),
            valid_until_utc=now + timedelta(days=90),
            authorization_token="demo-authorization-token-001",
        ),
        activation=ActivationDemo(
            mi_argentina_authorized=True,
            red_sube_attribute_active=True,
            activation_actor=ActivationActor.RED_SUBE,
            priority_attribute_token="demo-priority-attribute-token-001",
            user_consented_attribute_activation=True,
        ),
        trip=TripUseDemo(
            transport_context=TransportContext.BUS_ONBOARD,
            validation_paid=True,
            preference_mode=UserPreferenceMode.PASSIVE,
            user_consented_operational_hint=False,
            operational_hint=OperationalHint.NONE,
        ),
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.REJECTED
    assert result.priority_attribute_active is False
    assert "need_not_accredited" in result.risk_flags


def test_expired_accreditation_rejects_flow() -> None:
    now = datetime.now(timezone.utc)

    request = CoreUserFlowRequest(
        accreditation=AccreditationDemo(
            actor=AccreditationActor.MEDICAL_PROFESSIONAL,
            need_accredited=True,
            valid_from_utc=now - timedelta(days=90),
            valid_until_utc=now - timedelta(days=1),
            authorization_token="demo-authorization-token-001",
        ),
        activation=ActivationDemo(
            mi_argentina_authorized=True,
            red_sube_attribute_active=True,
            activation_actor=ActivationActor.RED_SUBE,
            priority_attribute_token="demo-priority-attribute-token-001",
            user_consented_attribute_activation=True,
        ),
        trip=TripUseDemo(
            transport_context=TransportContext.BUS_ONBOARD,
            validation_paid=True,
            preference_mode=UserPreferenceMode.PASSIVE,
            user_consented_operational_hint=False,
            operational_hint=OperationalHint.NONE,
        ),
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.REJECTED
    assert "accreditation_expired" in result.risk_flags


def test_mi_argentina_authorization_missing_rejects_flow() -> None:
    request = create_demo_core_user_flow_request()

    modified = CoreUserFlowRequest(
        accreditation=request.accreditation,
        activation=ActivationDemo(
            mi_argentina_authorized=False,
            red_sube_attribute_active=True,
            activation_actor=ActivationActor.RED_SUBE,
            priority_attribute_token=request.activation.priority_attribute_token,
            user_consented_attribute_activation=True,
        ),
        trip=request.trip,
    )

    result = evaluate_core_user_flow(modified)

    assert result.status == CoreFlowStatus.REJECTED
    assert "mi_argentina_authorization_missing" in result.risk_flags


def test_user_must_consent_attribute_activation() -> None:
    request = create_demo_core_user_flow_request()

    modified = CoreUserFlowRequest(
        accreditation=request.accreditation,
        activation=ActivationDemo(
            mi_argentina_authorized=True,
            red_sube_attribute_active=True,
            activation_actor=ActivationActor.RED_SUBE,
            priority_attribute_token=request.activation.priority_attribute_token,
            user_consented_attribute_activation=False,
        ),
        trip=request.trip,
    )

    result = evaluate_core_user_flow(modified)

    assert result.status == CoreFlowStatus.REJECTED
    assert "user_did_not_consent_attribute_activation" in result.risk_flags


def test_red_sube_attribute_not_active_returns_attribute_not_active() -> None:
    request = create_demo_core_user_flow_request()

    modified = CoreUserFlowRequest(
        accreditation=request.accreditation,
        activation=ActivationDemo(
            mi_argentina_authorized=True,
            red_sube_attribute_active=False,
            activation_actor=ActivationActor.RED_SUBE,
            priority_attribute_token=request.activation.priority_attribute_token,
            user_consented_attribute_activation=True,
        ),
        trip=request.trip,
    )

    result = evaluate_core_user_flow(modified)

    assert result.status == CoreFlowStatus.ATTRIBUTE_NOT_ACTIVE
    assert result.priority_attribute_active is False
    assert result.visible_to_public_as == "Sin atributo SUBE Prioridad activo"


def test_unpaid_trip_validation_rejects_flow() -> None:
    request = create_demo_core_user_flow_request()

    modified = CoreUserFlowRequest(
        accreditation=request.accreditation,
        activation=request.activation,
        trip=TripUseDemo(
            transport_context=TransportContext.BUS_ONBOARD,
            validation_paid=False,
            preference_mode=UserPreferenceMode.PASSIVE,
            user_consented_operational_hint=False,
            operational_hint=OperationalHint.NONE,
        ),
    )

    result = evaluate_core_user_flow(modified)

    assert result.status == CoreFlowStatus.REJECTED
    assert "trip_validation_not_paid" in result.risk_flags


def test_silent_preference_validates_without_public_hint() -> None:
    request = create_demo_core_user_flow_request(
        preference_mode=UserPreferenceMode.SILENT,
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.TRIP_VALIDATED_SILENT
    assert result.visible_to_public_as == "Usuario SUBE Prioridad"
    assert result.operational_view["operational_hint_shared"] is False
    assert result.operational_view["authorized_staff_only"] is False


def test_visible_generic_preference_still_shows_only_generic_label() -> None:
    request = create_demo_core_user_flow_request(
        preference_mode=UserPreferenceMode.VISIBLE_GENERIC,
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.TRIP_VALIDATED_GENERIC_VISIBLE
    assert result.visible_to_public_as == "Usuario SUBE Prioridad"
    assert result.operational_view["visible_as"] == "Usuario SUBE Prioridad"
    assert result.operational_view["operational_hint_shared"] is False
    assert result.operational_view["contains_diagnosis"] is False


def test_station_consent_demo_shares_authorized_hint_only() -> None:
    result = run_station_consent_demo()

    assert result["status"] == CoreFlowStatus.TRIP_VALIDATED_AUTHORIZED_STAFF_NOTICE.value
    assert result["visible_to_public_as"] == "Usuario SUBE Prioridad"
    assert result["operational_view"]["operational_hint_shared"] is True
    assert result["operational_view"]["authorized_staff_only"] is True
    assert result["operational_view"]["operational_hint"] == (
        OperationalHint.MAY_NEED_PLATFORM_ASSISTANCE.value
    )
    assert result["operational_view"]["contains_diagnosis"] is False
    assert result["operational_view"]["contains_cud_visible"] is False


def test_no_consent_station_demo_keeps_generic_visibility() -> None:
    result = run_no_consent_station_demo()

    assert result["status"] == CoreFlowStatus.TRIP_VALIDATED_PASSIVE.value
    assert result["visible_to_public_as"] == "Usuario SUBE Prioridad"
    assert result["operational_view"]["operational_hint_shared"] is False
    assert result["operational_view"]["operational_hint"] == OperationalHint.NONE.value
    assert result["operational_view"]["authorized_staff_only"] is False


def test_hint_without_user_consent_rejects_flow() -> None:
    request = create_demo_core_user_flow_request(
        transport_context=TransportContext.PLATFORM_ACCESS_OR_DESCENT,
        preference_mode=UserPreferenceMode.AUTHORIZED_STAFF_WITH_CONSENTED_HINT,
        user_consented_operational_hint=False,
        operational_hint=OperationalHint.MAY_NEED_PLATFORM_ASSISTANCE,
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.REJECTED
    assert "operational_hint_without_user_consent" in result.risk_flags


def test_consent_without_hint_rejects_flow() -> None:
    request = create_demo_core_user_flow_request(
        transport_context=TransportContext.PLATFORM_ACCESS_OR_DESCENT,
        preference_mode=UserPreferenceMode.AUTHORIZED_STAFF_WITH_CONSENTED_HINT,
        user_consented_operational_hint=True,
        operational_hint=OperationalHint.NONE,
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.REJECTED
    assert "consent_without_operational_hint" in result.risk_flags


def test_authorized_staff_hint_not_shared_inside_bus_even_with_consent() -> None:
    request = create_demo_core_user_flow_request(
        transport_context=TransportContext.BUS_ONBOARD,
        preference_mode=UserPreferenceMode.AUTHORIZED_STAFF_WITH_CONSENTED_HINT,
        user_consented_operational_hint=True,
        operational_hint=OperationalHint.MAY_NEED_PLATFORM_ASSISTANCE,
    )

    result = evaluate_core_user_flow(request)

    assert result.status == CoreFlowStatus.TRIP_VALIDATED_PASSIVE
    assert result.operational_view["operational_hint_shared"] is False
    assert result.operational_view["authorized_staff_only"] is False


def test_result_to_dict_preserves_privacy_and_scope() -> None:
    result = evaluate_core_user_flow(create_demo_core_user_flow_request())
    data = result_to_dict(result)

    assert data["privacy_notice"]
    assert data["legal_scope_notice"]
    assert data["visible_to_public_as"] == "Usuario SUBE Prioridad"
    assert data["operational_view"]["contains_diagnosis"] is False
    assert data["operational_view"]["contains_cud_visible"] is False
    assert data["operational_view"]["contains_medical_certificate"] is False
    assert data["operational_view"]["contains_identity_data"] is False
    assert data["operational_view"]["driver_burden"] == "no_new_driver_obligation"

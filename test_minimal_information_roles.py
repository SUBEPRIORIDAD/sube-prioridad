"""
Tests — SUBE Prioridad: matriz de información mínima por rol.

Estos tests verifican que:

- cada actor reciba sólo la información mínima necesaria;
- la visibilidad pública sea siempre "Usuario SUBE Prioridad";
- validadoras y molinetes no reciban causa médica;
- choferes no reciban diagnóstico ni nuevas obligaciones;
- personal autorizado de estación pueda recibir indicio sólo con consentimiento;
- pasajeros colaboradores nunca conozcan causa, identidad ni diagnóstico;
- analítica use sólo datos agregados;
- se bloqueen solicitudes de indicios fuera de contexto autorizado;
- se bloqueen campos prohibidos como DNI, diagnóstico o CUD visible.
"""

from __future__ import annotations

import pytest

from minimal_information_roles import (
    DisclosureDecision,
    EcosystemRole,
    InformationItem,
    InformationSensitivity,
    OperationalContext,
    ProhibitedInformationItem,
    assert_no_prohibited_fields,
    create_demo_information_disclosure_request,
    create_policy_for_role,
    evaluate_minimal_information_disclosure,
    result_to_dict,
    run_collaborating_passenger_demo,
    run_demo,
    run_station_authorized_hint_demo,
)


def test_run_demo_discloses_only_generic_validator_information() -> None:
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["demo_mode"] is True
    assert result["decision"] == DisclosureDecision.ALLOWED.value
    assert result["role"] == EcosystemRole.VALIDATOR_OR_TURNSTILE.value
    assert result["public_visibility_label"] == "Usuario SUBE Prioridad"
    assert result["minimum_information_applied"] is True
    assert InformationItem.GENERIC_PRIORITY_LABEL.value in result["disclosed_information"]
    assert InformationItem.PRIORITY_ATTRIBUTE_ACTIVE.value in result["disclosed_information"]

    payload = result["payload_demo"]

    assert payload["visible_as"] == "Usuario SUBE Prioridad"
    assert payload["contains_dni"] is False
    assert payload["contains_name"] is False
    assert payload["contains_diagnosis"] is False
    assert payload["contains_cud_visible"] is False
    assert payload["contains_medical_certificate"] is False
    assert payload["contains_clinical_history"] is False
    assert payload["contains_specific_condition"] is False
    assert payload["contains_balance"] is False
    assert payload["contains_fare"] is False


def test_validator_or_turnstile_policy_never_allows_sensitive_data() -> None:
    policy = create_policy_for_role(EcosystemRole.VALIDATOR_OR_TURNSTILE)

    assert policy.public_visibility_label == "Usuario SUBE Prioridad"
    assert policy.sensitivity == InformationSensitivity.INTERNAL_TECHNICAL
    assert InformationItem.GENERIC_PRIORITY_LABEL in policy.allowed_information
    assert InformationItem.PRIORITY_ATTRIBUTE_ACTIVE in policy.allowed_information
    assert ProhibitedInformationItem.DIAGNOSIS in policy.prohibited_information
    assert ProhibitedInformationItem.CUD_VISIBLE in policy.prohibited_information
    assert ProhibitedInformationItem.MEDICAL_CERTIFICATE in policy.prohibited_information
    assert ProhibitedInformationItem.CLINICAL_HISTORY in policy.prohibited_information


def test_bus_driver_receives_generic_notice_without_new_obligation() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.BUS_DRIVER,
        context=OperationalContext.BUS_ONBOARD,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.ASSISTANCE_MODE,
            InformationItem.TRANSPORT_CONTEXT_TOKEN,
        ],
    )

    result = evaluate_minimal_information_disclosure(request)
    data = result_to_dict(result)

    assert data["decision"] == DisclosureDecision.ALLOWED.value
    assert data["public_visibility_label"] == "Usuario SUBE Prioridad"
    assert data["authorized_staff_only"] is False
    assert data["consent_required"] is False
    assert data["payload_demo"]["driver_burden"] == "no_new_driver_obligation"
    assert data["payload_demo"]["contains_diagnosis"] is False
    assert data["payload_demo"]["contains_cud_visible"] is False
    assert "no_new_driver_obligation" in data["audit_flags"]


def test_station_authorized_staff_can_receive_hint_only_with_consent() -> None:
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

    assert result.decision == DisclosureDecision.ALLOWED_WITH_CONSENT
    assert result.public_visibility_label == "Usuario SUBE Prioridad"
    assert result.authorized_staff_only is True
    assert result.consent_required is True
    assert result.consent_present is True
    assert InformationItem.AUTHORIZED_STATION_HINT in result.disclosed_information
    assert result.payload_demo["authorized_station_hint_shared"] is True
    assert result.payload_demo["authorized_staff_only"] is True
    assert result.payload_demo["contains_diagnosis"] is False
    assert result.payload_demo["contains_cud_visible"] is False


def test_station_hint_without_user_consent_is_blocked() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.STATION_AUTHORIZED_STAFF,
        context=OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.AUTHORIZED_STATION_HINT,
        ],
        user_consented_station_operational_hint=False,
        station_operational_hint_requested=True,
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.BLOCKED
    assert result.disclosed_information == []
    assert "station_hint_requested_without_user_consent" in result.risk_flags
    assert "authorized_station_hint_not_allowed" in result.risk_flags


def test_station_hint_outside_station_context_is_blocked() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.STATION_AUTHORIZED_STAFF,
        context=OperationalContext.BUS_ONBOARD,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.AUTHORIZED_STATION_HINT,
        ],
        user_consented_station_operational_hint=True,
        station_operational_hint_requested=True,
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.BLOCKED
    assert result.disclosed_information == []
    assert "station_hint_requested_outside_station_context" in result.risk_flags
    assert "authorized_station_hint_not_allowed" in result.risk_flags


def test_station_hint_for_non_authorized_role_is_blocked() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.COLLABORATING_PASSENGER,
        context=OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.AUTHORIZED_STATION_HINT,
        ],
        user_consented_station_operational_hint=True,
        station_operational_hint_requested=True,
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.BLOCKED
    assert result.disclosed_information == []
    assert "station_hint_requested_for_non_authorized_staff_role" in result.risk_flags
    assert "authorized_station_hint_not_allowed" in result.risk_flags


def test_collaborating_passenger_sees_no_cause_or_identity() -> None:
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

    assert result.decision == DisclosureDecision.ALLOWED
    assert result.public_visibility_label == "Usuario SUBE Prioridad"
    assert result.authorized_staff_only is False
    assert result.consent_required is False
    assert InformationItem.GENERIC_PRIORITY_LABEL in result.disclosed_information
    assert InformationItem.SOLIDARY_EVENT_TOKEN in result.disclosed_information
    assert InformationItem.BONUS_ELIGIBILITY_DEMO_FLAG in result.disclosed_information
    assert result.payload_demo["contains_name"] is False
    assert result.payload_demo["contains_diagnosis"] is False
    assert result.payload_demo["contains_cud_visible"] is False
    assert result.payload_demo["contains_specific_condition"] is False
    assert "collaborating_passenger_sees_no_cause" in result.audit_flags


def test_aggregate_analytics_uses_only_aggregated_information() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.AGGREGATE_ANALYTICS,
        context=OperationalContext.GENERAL_STREET_OR_ONBOARD,
        requested_information=[
            InformationItem.AGGREGATE_USAGE_METRIC,
            InformationItem.TRANSPORT_CONTEXT_TOKEN,
        ],
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.ALLOWED
    assert result.public_visibility_label == "Usuario SUBE Prioridad"
    assert InformationItem.AGGREGATE_USAGE_METRIC in result.disclosed_information
    assert InformationItem.TRANSPORT_CONTEXT_TOKEN in result.disclosed_information
    assert "aggregated_anonymized_use_only" in result.audit_flags
    assert result.payload_demo["contains_dni"] is False
    assert result.payload_demo["contains_precise_geolocation"] is False


def test_requesting_authorized_hint_without_context_is_blocked() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.VALIDATOR_OR_TURNSTILE,
        context=OperationalContext.GENERAL_STREET_OR_ONBOARD,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
            InformationItem.AUTHORIZED_STATION_HINT,
        ],
        station_operational_hint_requested=False,
        user_consented_station_operational_hint=False,
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.BLOCKED
    assert result.disclosed_information == []
    assert "authorized_station_hint_not_allowed" in result.risk_flags


def test_inactive_priority_attribute_blocks_disclosure() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.VALIDATOR_OR_TURNSTILE,
        context=OperationalContext.GENERAL_STREET_OR_ONBOARD,
        user_has_priority_attribute_active=False,
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.BLOCKED
    assert result.disclosed_information == []
    assert result.blocked_information == ["priority_attribute_not_active"]
    assert "priority_attribute_not_active" in result.risk_flags


def test_mi_argentina_policy_supports_consent_layer_without_public_cause() -> None:
    policy = create_policy_for_role(EcosystemRole.MI_ARGENTINA)

    assert policy.public_visibility_label == "Usuario SUBE Prioridad"
    assert policy.consent_required is True
    assert InformationItem.PRIORITY_ATTRIBUTE_ACTIVE in policy.allowed_information
    assert InformationItem.PRIORITY_ATTRIBUTE_TOKEN in policy.allowed_information
    assert InformationItem.VALIDITY_WINDOW in policy.allowed_information
    assert ProhibitedInformationItem.DIAGNOSIS in policy.prohibited_information
    assert ProhibitedInformationItem.CUD_VISIBLE in policy.prohibited_information


def test_red_sube_backend_policy_uses_tokens_not_sensitive_data() -> None:
    policy = create_policy_for_role(EcosystemRole.RED_SUBE_BACKEND)

    assert policy.public_visibility_label == "Usuario SUBE Prioridad"
    assert policy.sensitivity == InformationSensitivity.INTERNAL_TECHNICAL
    assert InformationItem.PRIORITY_ATTRIBUTE_TOKEN in policy.allowed_information
    assert InformationItem.PREFERENCE_PROFILE_TOKEN in policy.allowed_information
    assert InformationItem.TRANSPORT_CONTEXT_TOKEN in policy.allowed_information
    assert ProhibitedInformationItem.DNI in policy.prohibited_information
    assert ProhibitedInformationItem.DIAGNOSIS in policy.prohibited_information
    assert ProhibitedInformationItem.CUD_VISIBLE in policy.prohibited_information
    assert ProhibitedInformationItem.MEDICAL_CERTIFICATE in policy.prohibited_information


def test_transport_control_center_receives_operational_or_aggregate_tokens_only() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.TRANSPORT_OPERATOR_CONTROL_CENTER,
        context=OperationalContext.TRAIN_STATION_WAIT,
        requested_information=[
            InformationItem.PRIORITY_ATTRIBUTE_ACTIVE,
            InformationItem.TRANSPORT_CONTEXT_TOKEN,
            InformationItem.VALIDATION_EVENT_TOKEN,
            InformationItem.AGGREGATE_USAGE_METRIC,
        ],
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.ALLOWED
    assert result.public_visibility_label == "Usuario SUBE Prioridad"
    assert InformationItem.AGGREGATE_USAGE_METRIC in result.disclosed_information
    assert result.payload_demo["contains_diagnosis"] is False
    assert result.payload_demo["contains_clinical_history"] is False
    assert result.payload_demo["contains_specific_condition"] is False


def test_public_environment_gets_only_generic_priority_label() -> None:
    request = create_demo_information_disclosure_request(
        role=EcosystemRole.PUBLIC_ENVIRONMENT,
        context=OperationalContext.GENERAL_STREET_OR_ONBOARD,
        requested_information=[
            InformationItem.GENERIC_PRIORITY_LABEL,
        ],
    )

    result = evaluate_minimal_information_disclosure(request)

    assert result.decision == DisclosureDecision.ALLOWED
    assert result.public_visibility_label == "Usuario SUBE Prioridad"
    assert result.disclosed_information == [InformationItem.GENERIC_PRIORITY_LABEL]
    assert result.authorized_staff_only is False
    assert result.consent_required is False


def test_result_to_dict_contains_privacy_scope_and_warnings() -> None:
    request = create_demo_information_disclosure_request()
    result = evaluate_minimal_information_disclosure(request)

    data = result_to_dict(result)

    assert data["privacy_notice"]
    assert data["legal_scope_notice"]
    assert data["public_visibility_label"] == "Usuario SUBE Prioridad"
    assert data["minimum_information_applied"] is True
    assert "Sin integración real con SUBE." in data["warnings"]
    assert "Sin integración real con Red SUBE." in data["warnings"]
    assert "Sin diagnóstico." in data["warnings"]
    assert "Sin CUD visible." in data["warnings"]


def test_prohibited_fields_are_rejected_by_payload_keys() -> None:
    with pytest.raises(ValueError):
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "diagnostico": "dato prohibido",
                "cud": "dato prohibido",
                "user_token": "demo-user",
            }
        )


def test_run_station_authorized_hint_demo_shares_hint_with_consent() -> None:
    result = run_station_authorized_hint_demo()

    assert result["decision"] == DisclosureDecision.ALLOWED_WITH_CONSENT.value
    assert result["public_visibility_label"] == "Usuario SUBE Prioridad"
    assert result["authorized_staff_only"] is True
    assert result["consent_required"] is True
    assert result["consent_present"] is True
    assert InformationItem.AUTHORIZED_STATION_HINT.value in result["disclosed_information"]
    assert result["payload_demo"]["authorized_station_hint_shared"] is True
    assert result["payload_demo"]["contains_diagnosis"] is False
    assert result["payload_demo"]["contains_cud_visible"] is False


def test_run_collaborating_passenger_demo_keeps_information_minimal() -> None:
    result = run_collaborating_passenger_demo()

    assert result["decision"] == DisclosureDecision.ALLOWED.value
    assert result["role"] == EcosystemRole.COLLABORATING_PASSENGER.value
    assert result["public_visibility_label"] == "Usuario SUBE Prioridad"
    assert InformationItem.GENERIC_PRIORITY_LABEL.value in result["disclosed_information"]
    assert InformationItem.SOLIDARY_EVENT_TOKEN.value in result["disclosed_information"]
    assert result["payload_demo"]["contains_name"] is False
    assert result["payload_demo"]["contains_diagnosis"] is False
    assert result["payload_demo"]["contains_specific_condition"] is False
    assert "collaborating_passenger_sees_no_cause" in result["audit_flags"]

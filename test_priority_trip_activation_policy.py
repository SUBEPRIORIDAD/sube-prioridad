"""
Tests — SUBE Prioridad: política de activación por viaje.

Estos tests verifican que:

- tener atributo SUBE Prioridad activo no fuerce asistencia en todos los viajes;
- el usuario pueda elegir modo silencioso;
- el usuario pueda elegir modo pasivo interno;
- el modo visible requiera consentimiento;
- el modo luminoso requiera consentimiento;
- el indicio operativo sólo se comparta con consentimiento;
- el indicio operativo sólo se comparta en estación, andén, molinete o plataforma;
- la visibilidad general sea siempre "Usuario SUBE Prioridad";
- no se expongan diagnóstico, CUD visible ni datos sensibles;
- no se cree una obligación nueva para choferes.
"""

from __future__ import annotations

import pytest

from priority_trip_activation_policy import (
    ConsentedOperationalHint,
    OperationalContext,
    TransportContext,
    TripActivationStatus,
    TripAssistanceMode,
    VisibilityScope,
    assert_no_prohibited_fields,
    create_demo_priority_attribute_for_trip,
    create_demo_trip_activation_preference,
    create_demo_trip_activation_request,
    create_demo_trip_validation_context,
    evaluate_trip_activation_policy,
    result_to_dict,
    run_demo,
    run_silent_backup_demo,
    run_station_hint_demo,
)


def test_run_demo_uses_active_attribute_without_public_exposure() -> None:
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["demo_mode"] is True
    assert result["priority_attribute_active"] is True
    assert result["visible_as"] == "Usuario SUBE Prioridad"
    assert result["status"] == TripActivationStatus.ACTIVE_PASSIVE_NOTICE.value
    assert result["visibility_scope"] == VisibilityScope.SYSTEM_ONLY.value
    assert result["operational_hint_shared"] is False
    assert result["authorized_staff_only"] is False
    assert result["blocks_trip_assistance_flow"] is False


def test_active_attribute_does_not_force_assistance_every_trip() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.SILENT,
            user_requests_assistance_this_trip=False,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.priority_attribute_active is True
    assert result.status == TripActivationStatus.ACTIVE_SILENT_BACKUP
    assert result.visible_as == "Usuario SUBE Prioridad"
    assert result.visibility_scope == VisibilityScope.SYSTEM_ONLY
    assert result.operational_hint_shared is False
    assert result.authorized_staff_only is False
    assert result.blocks_trip_assistance_flow is False
    assert "user_chose_no_active_assistance_this_trip" in result.audit_flags


def test_internal_passive_mode_is_system_only() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.INTERNAL_PASSIVE,
            user_requests_assistance_this_trip=True,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.ACTIVE_PASSIVE_NOTICE
    assert result.visible_as == "Usuario SUBE Prioridad"
    assert result.visibility_scope == VisibilityScope.SYSTEM_ONLY
    assert result.operational_hint_shared is False
    assert result.blocks_trip_assistance_flow is False
    assert "internal_passive_mode_supported" in result.audit_flags


def test_discreet_mode_is_system_only_and_generic() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.DISCREET,
            user_requests_assistance_this_trip=True,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.ACTIVE_DISCREET_NOTICE
    assert result.visible_as == "Usuario SUBE Prioridad"
    assert result.visibility_scope == VisibilityScope.SYSTEM_ONLY
    assert result.operational_hint_shared is False
    assert result.authorized_staff_only is False
    assert "discreet_mode_supported" in result.audit_flags


def test_visible_mode_requires_public_generic_notice_consent() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.VISIBLE,
            user_requests_assistance_this_trip=True,
            user_allows_public_generic_notice=False,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "visible_notice_not_consented" in result.risk_flags


def test_visible_mode_with_consent_shows_only_generic_label() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.VISIBLE,
            user_requests_assistance_this_trip=True,
            user_allows_public_generic_notice=True,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.ACTIVE_VISIBLE_NOTICE
    assert result.visible_as == "Usuario SUBE Prioridad"
    assert result.visibility_scope == VisibilityScope.PUBLIC_GENERIC
    assert result.operational_hint_shared is False
    assert result.authorized_staff_only is False
    assert result.blocks_trip_assistance_flow is False


def test_luminous_mode_requires_luminous_signal_consent() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.LUMINOUS,
            user_requests_assistance_this_trip=True,
            user_allows_luminous_signal=False,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "luminous_signal_not_consented" in result.risk_flags


def test_luminous_mode_with_consent_remains_generic_public_notice() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.LUMINOUS,
            user_requests_assistance_this_trip=True,
            user_allows_luminous_signal=True,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.ACTIVE_VISIBLE_NOTICE
    assert result.visible_as == "Usuario SUBE Prioridad"
    assert result.visibility_scope == VisibilityScope.PUBLIC_GENERIC
    assert result.operational_hint_shared is False
    assert result.authorized_staff_only is False
    assert result.blocks_trip_assistance_flow is False


def test_station_authorized_staff_mode_requires_authorized_staff_consent() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.STATION_AUTHORIZED_STAFF,
            user_requests_assistance_this_trip=True,
            user_allows_authorized_staff_notice=False,
            user_allows_station_hint=True,
        ),
        priority_attribute=create_demo_priority_attribute_for_trip(
            consented_operational_hint_enabled=True,
            consented_operational_hint=(
                ConsentedOperationalHint.MAY_NEED_PLATFORM_ASSISTANCE
            ),
        ),
        validation_context=create_demo_trip_validation_context(
            transport_context=TransportContext.PLATFORM,
        ),
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "authorized_staff_notice_not_consented" in result.risk_flags


def test_station_hint_requires_attribute_consent() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.STATION_AUTHORIZED_STAFF,
            user_requests_assistance_this_trip=True,
            user_allows_authorized_staff_notice=True,
            user_allows_station_hint=True,
        ),
        priority_attribute=create_demo_priority_attribute_for_trip(
            consented_operational_hint_enabled=False,
            consented_operational_hint=ConsentedOperationalHint.NONE,
        ),
        validation_context=create_demo_trip_validation_context(
            transport_context=TransportContext.PLATFORM,
        ),
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "station_hint_preference_without_attribute_consent" in result.risk_flags


def test_station_hint_is_shared_only_in_station_or_platform_context() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.STATION_AUTHORIZED_STAFF,
            user_requests_assistance_this_trip=True,
            user_allows_authorized_staff_notice=True,
            user_allows_station_hint=True,
        ),
        priority_attribute=create_demo_priority_attribute_for_trip(
            consented_operational_hint_enabled=True,
            consented_operational_hint=(
                ConsentedOperationalHint.MAY_NEED_PLATFORM_ASSISTANCE
            ),
        ),
        validation_context=create_demo_trip_validation_context(
            transport_context=TransportContext.PLATFORM,
        ),
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.ACTIVE_STATION_AUTHORIZED_NOTICE
    assert result.visible_as == "Usuario SUBE Prioridad"
    assert result.visibility_scope == VisibilityScope.AUTHORIZED_STAFF_ONLY
    assert result.operational_hint_shared is True
    assert result.operational_hint == (
        ConsentedOperationalHint.MAY_NEED_PLATFORM_ASSISTANCE
    )
    assert result.authorized_staff_only is True
    assert result.blocks_trip_assistance_flow is False


def test_station_hint_is_not_shared_inside_bus_even_with_consent() -> None:
    request = create_demo_trip_activation_request(
        preference=create_demo_trip_activation_preference(
            assistance_mode=TripAssistanceMode.STATION_AUTHORIZED_STAFF,
            user_requests_assistance_this_trip=True,
            user_allows_authorized_staff_notice=True,
            user_allows_station_hint=True,
        ),
        priority_attribute=create_demo_priority_attribute_for_trip(
            consented_operational_hint_enabled=True,
            consented_operational_hint=(
                ConsentedOperationalHint.MAY_NEED_PLATFORM_ASSISTANCE
            ),
        ),
        validation_context=create_demo_trip_validation_context(
            transport_context=TransportContext.BUS,
        ),
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.ACTIVE_PASSIVE_NOTICE
    assert result.visible_as == "Usuario SUBE Prioridad"
    assert result.visibility_scope == VisibilityScope.SYSTEM_ONLY
    assert result.operational_hint_shared is False
    assert result.authorized_staff_only is False
    assert result.blocks_trip_assistance_flow is False


def test_inactive_attribute_blocks_trip_assistance_flow() -> None:
    request = create_demo_trip_activation_request(
        priority_attribute=create_demo_priority_attribute_for_trip(
            active=False,
            valid_for_trip=True,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.priority_attribute_active is False
    assert result.visible_as == "Sin atributo SUBE Prioridad activo para este viaje"
    assert result.blocks_trip_assistance_flow is True
    assert "priority_attribute_not_active" in result.risk_flags


def test_attribute_not_valid_for_trip_blocks_flow() -> None:
    request = create_demo_trip_activation_request(
        priority_attribute=create_demo_priority_attribute_for_trip(
            active=True,
            valid_for_trip=False,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "priority_attribute_not_valid_for_trip" in result.risk_flags


def test_unpaid_validation_blocks_trip_assistance_flow() -> None:
    request = create_demo_trip_activation_request(
        validation_context=create_demo_trip_validation_context(
            validation_paid=False,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "validation_payment_not_confirmed" in result.risk_flags


def test_invalid_generic_visibility_label_blocks_flow() -> None:
    request = create_demo_trip_activation_request(
        priority_attribute=create_demo_priority_attribute_for_trip(
            generic_visibility_label="Necesita ayuda médica",
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "invalid_generic_visibility_label" in result.risk_flags


def test_operational_hint_enabled_without_hint_blocks_flow() -> None:
    request = create_demo_trip_activation_request(
        priority_attribute=create_demo_priority_attribute_for_trip(
            consented_operational_hint_enabled=True,
            consented_operational_hint=ConsentedOperationalHint.NONE,
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "operational_hint_enabled_without_hint" in result.risk_flags


def test_operational_hint_present_without_attribute_consent_blocks_flow() -> None:
    request = create_demo_trip_activation_request(
        priority_attribute=create_demo_priority_attribute_for_trip(
            consented_operational_hint_enabled=False,
            consented_operational_hint=(
                ConsentedOperationalHint.MAY_NEED_STATION_ASSISTANCE
            ),
        )
    )

    result = evaluate_trip_activation_policy(request)

    assert result.status == TripActivationStatus.REJECTED
    assert result.blocks_trip_assistance_flow is True
    assert "operational_hint_present_without_attribute_consent" in result.risk_flags


def test_result_to_dict_contains_privacy_scope_and_driver_burden() -> None:
    request = create_demo_trip_activation_request()

    result = evaluate_trip_activation_policy(request)
    data = result_to_dict(result)

    assert data["privacy_notice"]
    assert data["legal_scope_notice"]
    assert data["visible_as"] == "Usuario SUBE Prioridad"
    assert data["alert_payload_demo"]["contains_diagnosis"] is False
    assert data["alert_payload_demo"]["contains_cud_visible"] is False
    assert data["alert_payload_demo"]["contains_medical_certificate"] is False
    assert data["alert_payload_demo"]["contains_identity_data"] is False
    assert data["alert_payload_demo"]["driver_burden"] == "no_new_driver_obligation"


def test_prohibited_fields_are_rejected_by_payload_keys() -> None:
    with pytest.raises(ValueError):
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "diagnostico": "dato prohibido",
                "user_token": "demo-user",
            }
        )


def test_run_silent_backup_demo_keeps_attribute_as_private_backup() -> None:
    result = run_silent_backup_demo()

    assert result["priority_attribute_active"] is True
    assert result["status"] == TripActivationStatus.ACTIVE_SILENT_BACKUP.value
    assert result["visible_as"] == "Usuario SUBE Prioridad"
    assert result["visibility_scope"] == VisibilityScope.SYSTEM_ONLY.value
    assert result["operational_hint_shared"] is False
    assert result["authorized_staff_only"] is False


def test_run_station_hint_demo_shares_authorized_staff_hint() -> None:
    result = run_station_hint_demo()

    assert result["priority_attribute_active"] is True
    assert result["status"] == (
        TripActivationStatus.ACTIVE_STATION_AUTHORIZED_NOTICE.value
    )
    assert result["visible_as"] == "Usuario SUBE Prioridad"
    assert result["visibility_scope"] == VisibilityScope.AUTHORIZED_STAFF_ONLY.value
    assert result["operational_hint_shared"] is True
    assert result["authorized_staff_only"] is True
    assert result["operational_hint"] == (
        ConsentedOperationalHint.MAY_NEED_PLATFORM_ASSISTANCE.value
    )


def test_operational_context_import_is_available_for_cross_module_language() -> None:
    """
    Este test protege el vocabulario conceptual compartido con
    priority_accreditation_flow.py.

    OperationalContext no se usa internamente en este módulo, pero puede ser útil
    como lenguaje puente entre acreditación previa y activación por viaje.
    """
    assert OperationalContext.PLATFORM_ACCESS_OR_DESCENT.value == (
        "platform_access_or_descent"
    )

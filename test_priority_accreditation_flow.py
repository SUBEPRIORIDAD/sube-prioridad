"""
Tests — SUBE Prioridad: acreditación previa y activación del atributo.

Estos tests verifican que:

- exista acreditación médica/administrativa previa;
- Mi Argentina funcione como capa demo de autorización;
- Red SUBE active luego el atributo demo;
- la calle sólo vea "Usuario SUBE Prioridad";
- el indicio operativo adicional sólo exista con consentimiento;
- sin consentimiento no se comparta indicio operativo;
- no se expongan diagnóstico, CUD visible ni datos sensibles;
- se contemplen personas sin celular o sin acceso directo a Mi Argentina;
- situaciones rechazadas, vencidas o inconsistentes bloqueen la activación.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from priority_accreditation_flow import (
    AccreditationOrigin,
    AccreditationStatus,
    AssistanceNeedKind,
    ConsentedOperationalIndication,
    MiArgentinaAuthorizationStatus,
    OperationalContext,
    RedSubeSyncStatus,
    assert_no_prohibited_fields,
    build_operational_context_notice,
    create_demo_accreditation_flow_request,
    create_demo_accreditation_request,
    result_to_dict,
    run_demo,
    run_no_consent_demo,
    run_station_consent_demo,
    simulate_priority_accreditation_flow,
)


def test_run_demo_activates_generic_sube_prioridad_attribute() -> None:
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["demo_mode"] is True
    assert result["priority_attribute_active"] is True
    assert result["accreditation_status"] == AccreditationStatus.APPROVED.value
    assert result["mi_argentina_status"] == (
        MiArgentinaAuthorizationStatus.USER_CONSENT_ACCEPTED.value
    )
    assert result["red_sube_sync_status"] == RedSubeSyncStatus.ACTIVE_ATTRIBUTE.value
    assert result["visible_in_street_as"] == "Usuario SUBE Prioridad"
    assert result["blocks_activation"] is False

    notice = result["operational_context_notice"]

    assert notice["attribute_active"] is True
    assert notice["visible_as"] == "Usuario SUBE Prioridad"
    assert notice["operational_indication_shared"] is False
    assert notice["authorized_staff_only"] is False


def test_default_flow_does_not_share_operational_indication_without_consent() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_operational_indication_for_station_contexts=False,
        selected_operational_indication=ConsentedOperationalIndication.NONE,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is True
    assert result.red_sube_priority_attribute is not None

    station_notice = build_operational_context_notice(
        attribute=result.red_sube_priority_attribute,
        context=OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
    )

    assert station_notice["attribute_active"] is True
    assert station_notice["visible_as"] == "Usuario SUBE Prioridad"
    assert station_notice["operational_indication_shared"] is False
    assert station_notice["operational_indication"] == (
        ConsentedOperationalIndication.NONE.value
    )
    assert station_notice["authorized_staff_only"] is False


def test_station_context_shares_respectful_indication_only_with_consent() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_operational_indication_for_station_contexts=True,
        selected_operational_indication=(
            ConsentedOperationalIndication.MAY_NEED_PLATFORM_ASSISTANCE
        ),
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is True
    assert result.red_sube_priority_attribute is not None

    station_notice = build_operational_context_notice(
        attribute=result.red_sube_priority_attribute,
        context=OperationalContext.PLATFORM_ACCESS_OR_DESCENT,
    )

    assert station_notice["attribute_active"] is True
    assert station_notice["visible_as"] == "Usuario SUBE Prioridad"
    assert station_notice["operational_indication_shared"] is True
    assert station_notice["operational_indication"] == (
        ConsentedOperationalIndication.MAY_NEED_PLATFORM_ASSISTANCE.value
    )
    assert station_notice["authorized_staff_only"] is True
    assert "diagnóstico" in station_notice["privacy_rule"]


def test_consented_indication_is_not_shared_in_general_transport_context() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_operational_indication_for_station_contexts=True,
        selected_operational_indication=(
            ConsentedOperationalIndication.MAY_NEED_PLATFORM_ASSISTANCE
        ),
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.red_sube_priority_attribute is not None

    general_notice = build_operational_context_notice(
        attribute=result.red_sube_priority_attribute,
        context=OperationalContext.BUS_OR_ONBOARD_VALIDATOR,
    )

    assert general_notice["attribute_active"] is True
    assert general_notice["visible_as"] == "Usuario SUBE Prioridad"
    assert general_notice["operational_indication_shared"] is False
    assert general_notice["authorized_staff_only"] is False


def test_user_declines_priority_attribute_activation_blocks_red_sube_sync() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_priority_attribute_activation=False,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is False
    assert result.blocks_activation is True
    assert result.mi_argentina_status == (
        MiArgentinaAuthorizationStatus.USER_CONSENT_DECLINED
    )
    assert result.red_sube_sync_status == RedSubeSyncStatus.NOT_READY
    assert result.red_sube_priority_attribute is None
    assert "user_declined_priority_attribute_activation" in result.risk_flags


def test_rejected_accreditation_blocks_activation() -> None:
    accreditation = create_demo_accreditation_request(
        status=AccreditationStatus.REJECTED,
        rejection_reason_code="demo-rejected-by-authority",
    )

    flow_request = create_demo_accreditation_flow_request(
        accreditation_request=accreditation,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is False
    assert result.blocks_activation is True
    assert result.red_sube_sync_status == RedSubeSyncStatus.NOT_READY
    assert "accreditation_status_rejected" in result.risk_flags


def test_expired_validity_blocks_activation() -> None:
    now = datetime.now(timezone.utc)

    accreditation = create_demo_accreditation_request(
        requested_valid_from_utc=now - timedelta(days=120),
        requested_valid_until_utc=now - timedelta(days=1),
    )

    flow_request = create_demo_accreditation_flow_request(
        accreditation_request=accreditation,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is False
    assert result.blocks_activation is True
    assert "requested_validity_expired" in result.risk_flags


def test_invalid_validity_range_blocks_activation() -> None:
    now = datetime.now(timezone.utc)

    accreditation = create_demo_accreditation_request(
        requested_valid_from_utc=now + timedelta(days=10),
        requested_valid_until_utc=now + timedelta(days=1),
    )

    flow_request = create_demo_accreditation_flow_request(
        accreditation_request=accreditation,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is False
    assert result.blocks_activation is True
    assert "invalid_validity_range" in result.risk_flags


def test_user_without_mi_argentina_can_use_assisted_channel() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_has_mi_argentina_access=False,
        assisted_channel_available=True,
        user_has_mobile_device=False,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is True
    assert result.blocks_activation is False
    assert result.requires_assisted_channel is True
    assert "assisted_channel_required_or_recommended" in result.audit_flags
    assert "user_without_mobile_supported" in result.audit_flags


def test_no_mi_argentina_and_no_assisted_channel_blocks_activation() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_has_mi_argentina_access=False,
        assisted_channel_available=False,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is False
    assert result.blocks_activation is True
    assert "no_mi_argentina_access_and_no_assisted_channel" in result.risk_flags


def test_selected_operational_indication_without_consent_blocks_activation() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_operational_indication_for_station_contexts=False,
        selected_operational_indication=(
            ConsentedOperationalIndication.MAY_NEED_STATION_ASSISTANCE
        ),
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is False
    assert result.blocks_activation is True
    assert "selected_operational_indication_without_user_consent" in result.risk_flags


def test_consent_without_selected_indication_blocks_activation() -> None:
    flow_request = create_demo_accreditation_flow_request(
        user_accepts_operational_indication_for_station_contexts=True,
        selected_operational_indication=ConsentedOperationalIndication.NONE,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is False
    assert result.blocks_activation is True
    assert "operational_indication_consent_without_selected_indication" in (
        result.risk_flags
    )


def test_request_supports_multiple_accreditation_origins_and_need_kinds() -> None:
    accreditation = create_demo_accreditation_request(
        origin=AccreditationOrigin.CUD_INTEROPERABILITY_DEMO,
        assistance_need_kind=AssistanceNeedKind.CUD_RELATED_NEED,
    )

    flow_request = create_demo_accreditation_flow_request(
        accreditation_request=accreditation,
    )

    result = simulate_priority_accreditation_flow(flow_request)

    assert result.priority_attribute_active is True
    assert result.blocks_activation is False
    assert result.interagency_validation is not None
    assert result.interagency_validation.data_minimization_applied is True
    assert result.interagency_validation.sensitive_data_removed is True


def test_result_to_dict_contains_privacy_and_scope_notices() -> None:
    flow_request = create_demo_accreditation_flow_request()

    result = simulate_priority_accreditation_flow(flow_request)

    data = result_to_dict(result)

    assert data["privacy_notice"]
    assert data["legal_scope_notice"]
    assert "Sin integración real con Mi Argentina." in data["warnings"]
    assert "Sin integración real con Red SUBE." in data["warnings"]
    assert "Sin diagnóstico." in data["warnings"]
    assert "Sin CUD visible." in data["warnings"]
    assert data["red_sube_priority_attribute"]["street_visibility"] == (
        "generic_sube_prioridad"
    )


def test_prohibited_fields_are_rejected_by_payload_keys() -> None:
    with pytest.raises(ValueError):
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "diagnostico": "dato prohibido",
                "user_token": "demo-user",
            }
        )


def test_run_station_consent_demo_includes_station_notice() -> None:
    result = run_station_consent_demo()

    assert result["priority_attribute_active"] is True
    assert "station_context_notice" in result
    assert result["station_context_notice"]["visible_as"] == "Usuario SUBE Prioridad"
    assert result["station_context_notice"]["operational_indication_shared"] is True
    assert result["station_context_notice"]["authorized_staff_only"] is True


def test_run_no_consent_demo_keeps_station_notice_generic() -> None:
    result = run_no_consent_demo()

    assert result["priority_attribute_active"] is True
    assert "station_context_notice" in result
    assert result["station_context_notice"]["visible_as"] == "Usuario SUBE Prioridad"
    assert result["station_context_notice"]["operational_indication_shared"] is False
    assert result["station_context_notice"]["authorized_staff_only"] is False

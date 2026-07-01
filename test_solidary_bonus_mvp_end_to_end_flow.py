from datetime import datetime, timedelta, timezone

import pytest

from solidary_bonus_mvp_end_to_end_flow import (
    EndToEndScenario,
    EndToEndStatus,
    assert_no_prohibited_fields,
    create_demo_end_to_end_policy,
    create_demo_solidary_bonus_mvp_end_to_end_request,
    result_to_dict,
    run_mobile_to_mobile_demo,
    run_priority_phone_nfc_card_demo,
    run_solidary_bonus_mvp_end_to_end,
    run_validator_assisted_card_tap_demo,
)

from solidary_bonus_mvp_accrual_flow import (
    create_demo_bonus_accrual_ledger,
    create_demo_bonus_accrual_policy,
)

from solidary_bonus_mvp_sync_options import (
    MvpSyncOption,
    TransportMode,
    ValidationPointType,
    create_demo_mvp_red_sube_context,
    create_demo_mvp_sync_option_request,
    create_demo_validator_assisted_card_tap_request,
)


def test_mobile_to_mobile_end_to_end_completes():
    result = run_mobile_to_mobile_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Orquestador MVP End-to-End de Bono Solidario"
    assert result["demo_mode"] is True

    assert result["status"] in {"completed", "completed_with_audit"}
    assert result["scenario"] == "mobile_to_mobile"
    assert result["selected_mvp_option"] == "mobile_to_mobile_redsube_context"
    assert result["sync_option_status"] == "ready"
    assert result["accrual_status"] in {"created", "created_with_audit"}

    assert result["instruction_created"] is True
    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["final_demo_discount_bps_if_eligible"] == 10000

    assert result["sync_option_result_demo"] is not None
    assert result["accrual_result_demo"] is not None

    assert result["security_summary"]["real_sube_integration"] is False
    assert result["security_summary"]["real_red_sube_integration"] is False
    assert result["security_summary"]["real_balance_modified"] is False
    assert result["security_summary"]["real_tariff_applied"] is False

    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "El Bono Solidario demo se limita al próximo viaje elegible." in result["warnings"]


def test_priority_phone_nfc_card_end_to_end_completes():
    result = run_priority_phone_nfc_card_demo()

    assert result["status"] in {"completed", "completed_with_audit"}
    assert result["scenario"] == "priority_phone_nfc_card"
    assert result["selected_mvp_option"] == "priority_phone_nfc_to_collaborator_card"
    assert result["sync_option_status"] == "ready"
    assert result["instruction_created"] is True
    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False

    assert result["accrual_result_demo"]["accrual_source"] == "priority_phone_nfc_card"
    assert result["accrual_result_demo"]["instruction"]["instruction_mode"] == "card_token_pending_demo"


def test_validator_assisted_end_to_end_completes_with_audit():
    result = run_validator_assisted_card_tap_demo()

    assert result["status"] == "completed_with_audit"
    assert result["scenario"] == "validator_assisted_card_tap"
    assert result["selected_mvp_option"] == "validator_assisted_card_tap"
    assert result["sync_option_status"] == "ready_with_audit"
    assert result["accrual_status"] == "created_with_audit"

    assert result["instruction_created"] is True
    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["security_summary"]["driver_console_optional_only"] is True

    assert "sync_validator_assisted_card_tap_audit" in result["audit_flags"]
    assert "sync_no_driver_obligation_audit" in result["audit_flags"]
    assert "accrual_no_driver_obligation_audit" in result["audit_flags"]
    assert "La validadora asistida es una alternativa piloto auditable." in result["warnings"]
    assert "El chofer no debe cargar con una obligación nueva." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-result-to-dict-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Orquestador MVP End-to-End de Bono Solidario"
    assert data["demo_mode"] is True
    assert isinstance(data["sync_option_result_demo"], dict)
    assert isinstance(data["accrual_result_demo"], dict)
    assert isinstance(data["security_summary"], dict)
    assert isinstance(data["hard_risk_flags"], list)
    assert isinstance(data["audit_flags"], list)
    assert isinstance(data["warnings"], list)


def test_end_to_end_rejects_at_sync_option_when_sync_fails():
    sync_request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-e2e-sync-fails-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        mobile_handshake_available=False,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-rejected-at-sync-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
        sync_option_request=sync_request,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.REJECTED_AT_SYNC_OPTION
    assert result.instruction_created is False
    assert result.opens_bonus_evaluation_window is False
    assert result.blocks_solidary_bonus_flow is True
    assert result.accrual_status is None

    assert "sync_mobile_handshake_required_for_mobile_to_mobile_option" in result.hard_risk_flags


def test_end_to_end_rejects_at_accrual_when_ledger_limit_exceeded():
    ledger = create_demo_bonus_accrual_ledger(
        priority_trip_event_count_demo=1,
    )

    accrual_policy = create_demo_bonus_accrual_policy(
        max_bonus_events_per_priority_trip_demo=1,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-accrual-limit-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
        accrual_policy=accrual_policy,
        accrual_ledger=ledger,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.REJECTED_AT_ACCRUAL
    assert result.instruction_created is False
    assert result.blocks_solidary_bonus_flow is True
    assert result.sync_option_status == "ready"
    assert result.accrual_status == "rejected"

    assert "accrual_priority_trip_bonus_limit_exceeded" in result.hard_risk_flags


def test_end_to_end_rejects_at_accrual_when_collaborator_day_limit_exceeded():
    ledger = create_demo_bonus_accrual_ledger(
        collaborator_day_event_count_demo=3,
    )

    accrual_policy = create_demo_bonus_accrual_policy(
        max_bonus_events_per_collaborator_day_demo=3,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-collaborator-day-limit-001",
        scenario=EndToEndScenario.PRIORITY_PHONE_NFC_CARD,
        accrual_policy=accrual_policy,
        accrual_ledger=ledger,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.REJECTED_AT_ACCRUAL
    assert result.instruction_created is False
    assert result.blocks_solidary_bonus_flow is True
    assert "accrual_collaborator_day_bonus_limit_exceeded" in result.hard_risk_flags


def test_end_to_end_can_hide_nested_payloads():
    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-hide-payloads-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
    )

    policy = create_demo_end_to_end_policy(
        include_sync_payload_demo=False,
        include_accrual_payload_demo=False,
    )

    result = run_solidary_bonus_mvp_end_to_end(
        request=request,
        policy=policy,
    )

    assert result.status in {
        EndToEndStatus.COMPLETED,
        EndToEndStatus.COMPLETED_WITH_AUDIT,
    }
    assert result.sync_option_result_demo is None
    assert result.accrual_result_demo is None
    assert result.instruction_created is True


def test_end_to_end_with_discount_cap_completes_with_capped_final_discount():
    accrual_policy = create_demo_bonus_accrual_policy(
        bonus_extra_discount_bps_demo=5000,
        max_total_discount_bps_demo=9000,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-discount-cap-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
        accrual_policy=accrual_policy,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.COMPLETED_WITH_AUDIT
    assert result.final_demo_discount_bps_if_eligible == 9000
    assert "accrual_discount_cap_applied_demo" in result.audit_flags


def test_end_to_end_validator_assisted_bus_has_driver_console_optional_only():
    sync_request = create_demo_validator_assisted_card_tap_request(
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-validator-bus-001",
        scenario=EndToEndScenario.VALIDATOR_ASSISTED_CARD_TAP,
        sync_option_request=sync_request,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.COMPLETED_WITH_AUDIT
    assert result.selected_mvp_option == "validator_assisted_card_tap"
    assert result.security_summary["driver_console_optional_only"] is True
    assert result.blocks_solidary_bonus_flow is False

    assert "chofer no decide" in result.driver_burden_notice.lower()
    assert "no recibe una obligación nueva" in result.driver_burden_notice.lower()


def test_end_to_end_validator_assisted_coastal_train_completes():
    sync_request = create_demo_validator_assisted_card_tap_request(
        transport_mode=TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR,
        validation_point_type=ValidationPointType.ONBOARD_TRAIN_VALIDATOR,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-validator-coastal-train-001",
        scenario=EndToEndScenario.VALIDATOR_ASSISTED_CARD_TAP,
        sync_option_request=sync_request,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.COMPLETED_WITH_AUDIT
    assert result.instruction_created is True
    assert result.blocks_solidary_bonus_flow is False
    assert result.sync_option_result_demo["security_summary"]["transport_mode"] == "coastal_train_or_onboard_validator"
    assert result.sync_option_result_demo["security_summary"]["validation_point_type"] == "onboard_train_validator"


def test_end_to_end_rejects_expired_sync_window():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_mvp_red_sube_context(
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=30),
    )

    sync_request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-e2e-expired-sync-window-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        red_sube_context=context,
        mobile_handshake_available=True,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-expired-sync-window-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
        sync_option_request=sync_request,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.REJECTED_AT_SYNC_OPTION
    assert result.blocks_solidary_bonus_flow is True
    assert "sync_sync_window_expired" in result.hard_risk_flags


def test_end_to_end_rejects_when_sync_has_no_shared_context():
    sync_request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-e2e-no-shared-context-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        same_network_demo_id=False,
        same_route_demo_id=False,
        same_service_window_demo_id=False,
        same_validator_or_turnstile_demo_id=False,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_station_demo_id=False,
        same_platform_demo_id=False,
        mobile_handshake_available=True,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-no-shared-context-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
        sync_option_request=sync_request,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.REJECTED_AT_SYNC_OPTION
    assert result.blocks_solidary_bonus_flow is True
    assert "sync_no_shared_transport_context" in result.hard_risk_flags


def test_end_to_end_rejects_sync_collaborator_unilateral_claim():
    sync_request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-e2e-unilateral-sync-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        collaborator_claims_unilaterally=True,
        mobile_handshake_available=True,
    )

    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        end_to_end_event_demo_id="test-e2e-unilateral-sync-001",
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
        sync_option_request=sync_request,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    assert result.status == EndToEndStatus.REJECTED_AT_SYNC_OPTION
    assert result.blocks_solidary_bonus_flow is True
    assert "sync_collaborator_unilateral_claim" in result.hard_risk_flags


def test_end_to_end_keeps_privacy_and_legal_scope_notices():
    result = run_mobile_to_mobile_demo()

    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]
    assert "GPS exacto" in result["privacy_notice"]

    assert "conceptual" in result["legal_scope_notice"].lower()
    assert "no aplica descuentos reales" in result["legal_scope_notice"].lower()
    assert "no modifica saldo real" in result["legal_scope_notice"].lower()
    assert "no integra sube" in result["legal_scope_notice"].lower()


def test_assert_no_prohibited_fields_rejects_sensitive_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "diagnostico": "dato no permitido",
                "cud": "dato no permitido",
                "gps": "-34.0,-58.0",
                "telefono": "dato no permitido",
                "email": "dato no permitido",
                "saldo": "dato no permitido",
                "dinero": "dato no permitido",
                "ranking": "dato no permitido",
                "sancion": "dato no permitido",
            }
        )

    message = str(error.value).lower()

    assert "dni" in message
    assert "diagnostico" in message
    assert "cud" in message
    assert "gps" in message
    assert "telefono" in message
    assert "email" in message
    assert "saldo" in message
    assert "dinero" in message
    assert "ranking" in message
    assert "sancion" in message


def test_create_end_to_end_request_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_solidary_bonus_mvp_end_to_end_request(
            end_to_end_event_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_mvp_end_to_end_request(
            collaborator_account_demo_token="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_mvp_end_to_end_request(
            collaborator_sube_card_token="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_mvp_end_to_end_request(
            collaborator_payment_method_demo_token="",
        )

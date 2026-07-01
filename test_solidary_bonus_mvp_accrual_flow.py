from datetime import datetime, timedelta, timezone

import pytest

from solidary_bonus_mvp_accrual_flow import (
    BonusAccrualSource,
    BonusAccrualStatus,
    BonusInstructionMode,
    NextTripEligibilityStatus,
    assert_no_prohibited_fields,
    create_demo_bonus_accrual_ledger,
    create_demo_bonus_accrual_policy,
    create_demo_solidary_bonus_accrual_request,
    evaluate_solidary_bonus_mvp_accrual,
    result_to_dict,
    run_demo,
)

from solidary_bonus_mvp_sync_options import (
    AssistedActivationActor,
    MvpSyncOption,
    MvpSyncStatus,
    create_demo_mobile_to_mobile_request,
    create_demo_mvp_sync_option_request,
    create_demo_mvp_red_sube_context,
    create_demo_priority_phone_nfc_card_request,
    create_demo_validator_assisted_card_tap_request,
    evaluate_mvp_solidary_sync_option,
)


def test_run_demo_creates_bonus_instruction():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Flujo MVP de Acumulación de Bono Solidario"
    assert result["demo_mode"] is True

    assert result["status"] in {"created", "created_with_audit"}
    assert result["next_trip_eligibility_status"] == "pending_next_eligible_trip"
    assert result["instruction_created"] is True
    assert result["blocks_solidary_bonus_flow"] is False

    assert result["accrual_source"] == "mobile_to_mobile"
    assert result["selected_mvp_option"] == "mobile_to_mobile_redsube_context"

    assert result["base_red_sube_discount_bps_demo"] == 5000
    assert result["bonus_extra_discount_bps_demo"] == 5000
    assert result["final_demo_discount_bps_if_eligible"] == 10000

    instruction = result["instruction"]
    assert instruction is not None
    assert instruction["instruction_mode"] == "account_pending_demo"
    assert instruction["accrual_source"] == "mobile_to_mobile"
    assert instruction["applies_to_next_eligible_trip_only"] is True
    assert instruction["non_transferable"] is True
    assert instruction["not_cash_redeemable"] is True
    assert instruction["real_balance_modified"] is False
    assert instruction["real_tariff_applied"] is False

    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "El Bono Solidario demo se reserva para el próximo viaje elegible." in result["warnings"]
    assert "El colaborador no puede reclamar unilateralmente el bono." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-result-to-dict-001",
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Flujo MVP de Acumulación de Bono Solidario"
    assert data["demo_mode"] is True
    assert isinstance(data["instruction"], dict)
    assert isinstance(data["security_summary"], dict)
    assert isinstance(data["hard_risk_flags"], list)
    assert isinstance(data["audit_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_mobile_to_mobile_source_creates_account_pending_instruction():
    sync_request = create_demo_mobile_to_mobile_request()
    sync_result = evaluate_mvp_solidary_sync_option(sync_request)

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-mobile-to-mobile-accrual-001",
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status in {
        BonusAccrualStatus.CREATED,
        BonusAccrualStatus.CREATED_WITH_AUDIT,
    }
    assert result.next_trip_eligibility_status == NextTripEligibilityStatus.PENDING_NEXT_ELIGIBLE_TRIP
    assert result.accrual_source == BonusAccrualSource.MOBILE_TO_MOBILE
    assert result.instruction is not None
    assert result.instruction.instruction_mode == BonusInstructionMode.ACCOUNT_PENDING_DEMO
    assert result.instruction.accrual_source == BonusAccrualSource.MOBILE_TO_MOBILE
    assert result.blocks_solidary_bonus_flow is False


def test_priority_phone_nfc_card_source_creates_card_token_pending_instruction():
    sync_request = create_demo_priority_phone_nfc_card_request()
    sync_result = evaluate_mvp_solidary_sync_option(sync_request)

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-nfc-card-accrual-001",
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status in {
        BonusAccrualStatus.CREATED,
        BonusAccrualStatus.CREATED_WITH_AUDIT,
    }
    assert result.accrual_source == BonusAccrualSource.PRIORITY_PHONE_NFC_CARD
    assert result.selected_mvp_option == "priority_phone_nfc_to_collaborator_card"
    assert result.instruction is not None
    assert result.instruction.instruction_mode == BonusInstructionMode.CARD_TOKEN_PENDING_DEMO
    assert result.instruction.accrual_source == BonusAccrualSource.PRIORITY_PHONE_NFC_CARD
    assert "nfc_card_bonus_accrual_audit" in result.audit_flags


def test_validator_assisted_source_creates_validator_pending_instruction_with_audit():
    sync_request = create_demo_validator_assisted_card_tap_request()
    sync_result = evaluate_mvp_solidary_sync_option(sync_request)

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-validator-assisted-accrual-001",
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.CREATED_WITH_AUDIT
    assert result.accrual_source == BonusAccrualSource.VALIDATOR_ASSISTED_CARD_TAP
    assert result.selected_mvp_option == "validator_assisted_card_tap"
    assert result.instruction is not None
    assert result.instruction.instruction_mode == BonusInstructionMode.VALIDATOR_PENDING_DEMO
    assert result.instruction.accrual_source == BonusAccrualSource.VALIDATOR_ASSISTED_CARD_TAP
    assert result.requires_audit_review is True

    assert "validator_assisted_bonus_accrual_audit" in result.audit_flags
    assert "driver_console_optional_only_audit" in result.audit_flags
    assert "no_driver_obligation_audit" in result.audit_flags
    assert "mvp_sync_requires_audit_review" in result.audit_flags


def test_rejects_when_mvp_sync_result_is_not_ready():
    sync_request = create_demo_mobile_to_mobile_request()

    rejected_sync_request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-rejected-sync-for-accrual-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        participant_context=sync_request.participant_context,
        red_sube_context=sync_request.red_sube_context,
        mobile_handshake_available=False,
    )

    rejected_sync_result = evaluate_mvp_solidary_sync_option(rejected_sync_request)

    assert rejected_sync_result.status == MvpSyncStatus.REJECTED

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-accrual-rejects-not-ready-sync-001",
        mvp_sync_request=rejected_sync_request,
        mvp_sync_result=rejected_sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.next_trip_eligibility_status == NextTripEligibilityStatus.NOT_ELIGIBLE
    assert result.instruction_created is False
    assert result.blocks_solidary_bonus_flow is True
    assert "mvp_sync_not_ready" in result.hard_risk_flags


def test_rejects_when_mvp_sync_blocks_flow():
    sync_request = create_demo_mobile_to_mobile_request()
    sync_result = evaluate_mvp_solidary_sync_option(sync_request)

    blocked_sync_result = sync_result.__class__(
        **{
            **sync_result.__dict__,
            "blocks_solidary_bonus_flow": True,
        }
    )

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-accrual-rejects-blocked-sync-001",
        mvp_sync_request=sync_request,
        mvp_sync_result=blocked_sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "mvp_sync_blocks_solidary_bonus_flow" in result.hard_risk_flags


def test_rejects_previous_bonus_already_used():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-previous-bonus-used-001",
        previous_bonus_already_used=True,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.instruction_created is False
    assert result.blocks_solidary_bonus_flow is True
    assert "previous_bonus_already_used" in result.hard_risk_flags


def test_rejects_collaborator_unilateral_claim():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-collaborator-unilateral-claim-001",
        collaborator_claims_unilaterally=True,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_unilateral_claim" in result.hard_risk_flags


def test_rejects_without_priority_final_confirmation():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-no-priority-final-confirmation-001",
        priority_user_final_confirmation=False,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_user_final_confirmation_required" in result.hard_risk_flags


def test_rejects_if_not_next_trip_only():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-not-next-trip-only-001",
        next_trip_only=False,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "next_trip_only_required" in result.hard_risk_flags


def test_rejects_if_transferable():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-transferable-001",
        non_transferable=False,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "non_transferable_required" in result.hard_risk_flags


def test_rejects_if_cash_redeemable():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-cash-redeemable-001",
        not_cash_redeemable=False,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "not_cash_redeemable_required" in result.hard_risk_flags


def test_rejects_real_balance_change_request():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-real-balance-change-001",
        real_balance_change_requested=True,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "real_balance_change_not_allowed_in_demo" in result.hard_risk_flags


def test_rejects_real_tariff_application_request():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-real-tariff-application-001",
        real_tariff_application_requested=True,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "real_tariff_application_not_allowed_in_demo" in result.hard_risk_flags


def test_rejects_replay_accrual_event_id():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-replay-event-001",
    )

    ledger = create_demo_bonus_accrual_ledger(
        replay_event_ids=["test-replay-event-001"],
    )

    result = evaluate_solidary_bonus_mvp_accrual(
        request=request,
        ledger=ledger,
    )

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "replay_accrual_event_id" in result.hard_risk_flags


def test_rejects_priority_trip_bonus_limit_exceeded():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-priority-trip-limit-001",
    )

    policy = create_demo_bonus_accrual_policy(
        max_bonus_events_per_priority_trip_demo=1,
    )

    ledger = create_demo_bonus_accrual_ledger(
        priority_trip_event_count_demo=1,
    )

    result = evaluate_solidary_bonus_mvp_accrual(
        request=request,
        policy=policy,
        ledger=ledger,
    )

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_trip_bonus_limit_exceeded" in result.hard_risk_flags


def test_rejects_collaborator_day_bonus_limit_exceeded():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-collaborator-day-limit-001",
    )

    policy = create_demo_bonus_accrual_policy(
        max_bonus_events_per_collaborator_day_demo=3,
    )

    ledger = create_demo_bonus_accrual_ledger(
        collaborator_day_event_count_demo=3,
    )

    result = evaluate_solidary_bonus_mvp_accrual(
        request=request,
        policy=policy,
        ledger=ledger,
    )

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_day_bonus_limit_exceeded" in result.hard_risk_flags


def test_existing_ledger_counts_below_limit_create_with_audit():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-existing-counts-below-limit-001",
    )

    ledger = create_demo_bonus_accrual_ledger(
        priority_trip_event_count_demo=0,
        collaborator_day_event_count_demo=1,
    )

    result = evaluate_solidary_bonus_mvp_accrual(
        request=request,
        ledger=ledger,
    )

    assert result.status == BonusAccrualStatus.CREATED_WITH_AUDIT
    assert result.blocks_solidary_bonus_flow is False
    assert "collaborator_day_has_existing_bonus_events_demo" in result.audit_flags


def test_discount_is_capped_by_policy():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-discount-cap-001",
        base_red_sube_discount_bps_demo=5000,
    )

    policy = create_demo_bonus_accrual_policy(
        bonus_extra_discount_bps_demo=5000,
        max_total_discount_bps_demo=9000,
    )

    result = evaluate_solidary_bonus_mvp_accrual(
        request=request,
        policy=policy,
    )

    assert result.status in {
        BonusAccrualStatus.CREATED,
        BonusAccrualStatus.CREATED_WITH_AUDIT,
    }
    assert result.final_demo_discount_bps_if_eligible == 9000
    assert result.instruction is not None
    assert result.instruction.final_demo_discount_bps_if_eligible == 9000
    assert "discount_cap_applied_demo" in result.audit_flags


def test_instruction_window_uses_request_window():
    starts_at = datetime.now(timezone.utc)
    expires_at = starts_at + timedelta(hours=12)

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-custom-window-001",
        next_trip_window_starts_at_utc=starts_at,
        next_trip_window_expires_at_utc=expires_at,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status in {
        BonusAccrualStatus.CREATED,
        BonusAccrualStatus.CREATED_WITH_AUDIT,
    }
    assert result.instruction is not None
    assert result.instruction.next_trip_window_starts_at_utc == starts_at.isoformat()
    assert result.instruction.next_trip_window_expires_at_utc == expires_at.isoformat()
    assert result.security_summary["next_trip_window_starts_at_utc"] == starts_at.isoformat()
    assert result.security_summary["next_trip_window_expires_at_utc"] == expires_at.isoformat()


def test_free_text_tokens_are_rejected():
    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-free-text-token-001",
        collaborator_account_demo_token="quiero bono solidario gratis",
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_account_token_looks_like_free_text" in result.hard_risk_flags


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


def test_create_policy_rejects_invalid_values():
    with pytest.raises(ValueError):
        create_demo_bonus_accrual_policy(
            benefit_validity_hours=0,
        )

    with pytest.raises(ValueError):
        create_demo_bonus_accrual_policy(
            bonus_extra_discount_bps_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_bonus_accrual_policy(
            max_total_discount_bps_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_bonus_accrual_policy(
            max_bonus_events_per_priority_trip_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_bonus_accrual_policy(
            max_bonus_events_per_collaborator_day_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_bonus_accrual_policy(
            bonus_extra_discount_bps_demo=10001,
        )

    with pytest.raises(ValueError):
        create_demo_bonus_accrual_policy(
            max_total_discount_bps_demo=10001,
        )


def test_create_ledger_rejects_negative_values():
    with pytest.raises(ValueError):
        create_demo_bonus_accrual_ledger(
            priority_trip_event_count_demo=-1,
        )

    with pytest.raises(ValueError):
        create_demo_bonus_accrual_ledger(
            collaborator_day_event_count_demo=-1,
        )


def test_create_request_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_solidary_bonus_accrual_request(
            accrual_event_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_accrual_request(
            collaborator_account_demo_token="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_accrual_request(
            collaborator_sube_card_token="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_accrual_request(
            collaborator_payment_method_demo_token="",
        )


def test_create_request_rejects_invalid_discount_and_window():
    with pytest.raises(ValueError):
        create_demo_solidary_bonus_accrual_request(
            base_red_sube_discount_bps_demo=-1,
        )

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_accrual_request(
            base_red_sube_discount_bps_demo=10001,
        )

    starts_at = datetime.now(timezone.utc)
    expires_at = starts_at - timedelta(minutes=1)

    with pytest.raises(ValueError):
        create_demo_solidary_bonus_accrual_request(
            next_trip_window_starts_at_utc=starts_at,
            next_trip_window_expires_at_utc=expires_at,
        )


def test_accrual_keeps_driver_burden_notice_for_validator_assisted_option():
    sync_request = create_demo_validator_assisted_card_tap_request()
    sync_result = evaluate_mvp_solidary_sync_option(sync_request)

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-driver-burden-notice-001",
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert "chofer no decide" in result.driver_burden_notice.lower()
    assert "no recibe una obligación nueva" in result.driver_burden_notice.lower()
    assert "El chofer no debe cargar con una obligación nueva." in result.warnings


def test_accrual_with_validator_assisted_uses_driver_console_optional_audit():
    sync_request = create_demo_validator_assisted_card_tap_request()
    sync_result = evaluate_mvp_solidary_sync_option(sync_request)

    assert sync_request.assisted_activation_actor == AssistedActivationActor.DRIVER_CONSOLE_OPTIONAL

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-driver-console-optional-audit-001",
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.CREATED_WITH_AUDIT
    assert "driver_console_optional_only_audit" in result.audit_flags
    assert "no_driver_obligation_audit" in result.audit_flags


def test_accrual_from_expired_mvp_sync_is_rejected():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_mvp_red_sube_context(
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=30),
    )

    sync_request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-expired-mvp-sync-for-accrual-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        red_sube_context=context,
        mobile_handshake_available=True,
    )

    sync_result = evaluate_mvp_solidary_sync_option(sync_request)

    assert sync_result.status == MvpSyncStatus.REJECTED

    request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id="test-accrual-from-expired-mvp-sync-001",
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
    )

    result = evaluate_solidary_bonus_mvp_accrual(request)

    assert result.status == BonusAccrualStatus.REJECTED
    assert "mvp_sync_not_ready" in result.hard_risk_flags

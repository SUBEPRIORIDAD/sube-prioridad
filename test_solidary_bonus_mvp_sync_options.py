from datetime import datetime, timedelta, timezone

import pytest

from solidary_bonus_mvp_sync_options import (
    AssistedActivationActor,
    BenefitInstructionKind,
    MvpSyncOption,
    MvpSyncStatus,
    SeatType,
    TransportMode,
    ValidationPointType,
    assert_no_prohibited_fields,
    create_demo_mobile_to_mobile_request,
    create_demo_mvp_participant_context,
    create_demo_mvp_red_sube_context,
    create_demo_mvp_sync_option_request,
    create_demo_mvp_sync_policy,
    create_demo_priority_phone_nfc_card_request,
    create_demo_validator_assisted_card_tap_request,
    evaluate_mvp_solidary_sync_option,
    result_to_dict,
    run_mobile_to_mobile_demo,
    run_priority_phone_nfc_card_demo,
    run_validator_assisted_card_tap_demo,
)


def test_run_mobile_to_mobile_demo_is_ready():
    result = run_mobile_to_mobile_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Opciones MVP de Sincronización para Bono Solidario"
    assert result["demo_mode"] is True

    assert result["option"] == "mobile_to_mobile_redsube_context"
    assert result["status"] == "ready"
    assert result["benefit_instruction_kind"] == "next_trip_demo_window"

    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["window_minutes"] == 10
    assert result["window_matched"] is True

    assert result["base_red_sube_discount_bps_demo"] == 5000
    assert result["bonus_extra_discount_bps_demo"] == 5000
    assert result["final_demo_discount_bps_if_eligible"] == 10000

    assert result["benefit_window_demo"] is not None
    assert result["benefit_window_demo"]["applies_to_next_eligible_trip_only"] is True
    assert result["benefit_window_demo"]["direct_card_write_performed"] is False
    assert result["benefit_window_demo"]["real_tariff_applied"] is False
    assert result["benefit_window_demo"]["real_balance_modified"] is False

    assert "Sin obligación de tener celular." in result["warnings"]
    assert "La sincronización entre celulares es sólo una opción." in result["warnings"]
    assert "El +50% demo sólo abre una hipótesis de próximo viaje elegible." in result["warnings"]


def test_run_priority_phone_nfc_card_demo_is_ready():
    result = run_priority_phone_nfc_card_demo()

    assert result["option"] == "priority_phone_nfc_to_collaborator_card"
    assert result["status"] == "ready"
    assert result["benefit_instruction_kind"] == "card_update_pending_demo"

    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["window_minutes"] == 10
    assert result["window_matched"] is True

    assert result["security_summary"]["priority_has_mobile_device"] is True
    assert result["security_summary"]["priority_mobile_has_nfc"] is True
    assert result["security_summary"]["collaborator_has_mobile_device"] is False
    assert result["security_summary"]["collaborator_has_physical_sube_card"] is True
    assert result["security_summary"]["nfc_card_tap_available"] is True

    assert "priority_phone_nfc_to_card_audit" in result["audit_flags"]
    assert "collaborator_without_mobile_supported" in result["audit_flags"]
    assert "El NFC teléfono-tarjeta es sólo una opción." in result["warnings"]


def test_run_validator_assisted_card_tap_demo_is_ready_with_audit():
    result = run_validator_assisted_card_tap_demo()

    assert result["option"] == "validator_assisted_card_tap"
    assert result["status"] == "ready_with_audit"
    assert result["benefit_instruction_kind"] == "validator_tap_pending_demo"

    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["requires_audit_review"] is True
    assert result["window_minutes"] == 8
    assert result["window_matched"] is True

    assert result["assisted_activation_actor"] == "driver_console_optional"
    assert result["driver_console_optional_only"] is True

    assert "validator_assisted_card_tap_audit" in result["audit_flags"]
    assert "driver_console_optional_only_audit" in result["audit_flags"]
    assert "no_driver_obligation_audit" in result["audit_flags"]
    assert "good_faith_social_recognition_declared_audit" in result["audit_flags"]

    assert "chofer no está obligado" in result["driver_burden_notice"].lower()
    assert "La validadora asistida es sólo una opción piloto auditable." in result["warnings"]
    assert "El chofer no debe cargar con una obligación nueva." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_mobile_to_mobile_request()

    result = evaluate_mvp_solidary_sync_option(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Opciones MVP de Sincronización para Bono Solidario"
    assert data["demo_mode"] is True
    assert isinstance(data["security_summary"], dict)
    assert isinstance(data["benefit_window_demo"], dict)
    assert isinstance(data["hard_risk_flags"], list)
    assert isinstance(data["audit_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_mobile_to_mobile_requires_both_mobile_devices_and_handshake():
    participant = create_demo_mvp_participant_context(
        priority_has_mobile_device=True,
        collaborator_has_mobile_device=False,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-mobile-to-mobile-without-collaborator-mobile-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        participant_context=participant,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_mobile_required_for_mobile_to_mobile_option" in result.hard_risk_flags


def test_mobile_to_mobile_requires_handshake():
    participant = create_demo_mvp_participant_context(
        priority_has_mobile_device=True,
        collaborator_has_mobile_device=True,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-mobile-to-mobile-no-handshake-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        participant_context=participant,
        mobile_handshake_available=False,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "mobile_handshake_required_for_mobile_to_mobile_option" in result.hard_risk_flags


def test_priority_phone_nfc_requires_priority_mobile_with_nfc():
    participant = create_demo_mvp_participant_context(
        priority_has_mobile_device=True,
        priority_mobile_has_nfc=False,
        collaborator_has_physical_sube_card=True,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-nfc-without-priority-nfc-001",
        option=MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD,
        participant_context=participant,
        mobile_handshake_available=False,
        nfc_card_tap_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_mobile_nfc_required_for_nfc_card_option" in result.hard_risk_flags


def test_priority_phone_nfc_requires_collaborator_physical_card():
    participant = create_demo_mvp_participant_context(
        priority_has_mobile_device=True,
        priority_mobile_has_nfc=True,
        collaborator_has_physical_sube_card=False,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-nfc-without-collaborator-card-001",
        option=MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD,
        participant_context=participant,
        mobile_handshake_available=False,
        nfc_card_tap_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_physical_card_required_for_nfc_card_option" in result.hard_risk_flags


def test_priority_phone_nfc_requires_card_tap():
    request = create_demo_priority_phone_nfc_card_request()

    modified = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-nfc-card-tap-missing-001",
        option=MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD,
        participant_context=request.participant_context,
        red_sube_context=request.red_sube_context,
        mobile_handshake_available=False,
        nfc_card_tap_available=False,
        assisted_activation_actor=AssistedActivationActor.NOT_REQUIRED,
    )

    result = evaluate_mvp_solidary_sync_option(modified)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "nfc_card_tap_required_for_nfc_card_option" in result.hard_risk_flags


def test_validator_assisted_bus_option_accepts_without_mobiles():
    request = create_demo_validator_assisted_card_tap_request(
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.READY_WITH_AUDIT
    assert result.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP
    assert result.benefit_instruction_kind == BenefitInstructionKind.VALIDATOR_TAP_PENDING_DEMO
    assert result.blocks_solidary_bonus_flow is False
    assert result.security_summary["priority_has_mobile_device"] is False
    assert result.security_summary["collaborator_has_mobile_device"] is False
    assert "priority_user_without_mobile_supported" in result.audit_flags
    assert "collaborator_without_mobile_supported" in result.audit_flags


def test_validator_assisted_coastal_train_onboard_validator_accepts():
    request = create_demo_validator_assisted_card_tap_request(
        transport_mode=TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR,
        validation_point_type=ValidationPointType.ONBOARD_TRAIN_VALIDATOR,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.READY_WITH_AUDIT
    assert result.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP
    assert result.opens_bonus_evaluation_window is True
    assert result.blocks_solidary_bonus_flow is False
    assert result.security_summary["transport_mode"] == "coastal_train_or_onboard_validator"
    assert result.security_summary["validation_point_type"] == "onboard_train_validator"
    assert result.security_summary["same_trainset_demo_id"] is True


def test_validator_assisted_rejects_station_turnstile():
    request = create_demo_validator_assisted_card_tap_request(
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "validator_assisted_option_requires_onboard_validator" in result.hard_risk_flags
    assert (
        "validator_assisted_option_limited_to_bus_or_onboard_validator_demo"
        in result.hard_risk_flags
    )


def test_validator_assisted_rejects_when_second_tap_missing():
    request = create_demo_validator_assisted_card_tap_request()

    modified = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-validator-second-tap-missing-001",
        option=MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP,
        participant_context=request.participant_context,
        red_sube_context=request.red_sube_context,
        mobile_handshake_available=False,
        nfc_card_tap_available=False,
        validator_second_tap_available=False,
        assisted_activation_actor=AssistedActivationActor.DRIVER_CONSOLE_OPTIONAL,
        same_vehicle_demo_id=True,
        good_faith_social_recognition_declared=True,
    )

    result = evaluate_mvp_solidary_sync_option(modified)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "validator_second_tap_required_for_validator_option" in result.hard_risk_flags


def test_validator_assisted_rejects_if_driver_console_optional_mode_disabled():
    request = create_demo_validator_assisted_card_tap_request()

    policy = create_demo_mvp_sync_policy(
        allow_driver_console_optional_mode=False,
    )

    result = evaluate_mvp_solidary_sync_option(
        request=request,
        policy=policy,
    )

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "driver_console_optional_mode_not_allowed_by_policy" in result.hard_risk_flags


def test_validator_assisted_rejects_if_driver_console_is_mandatory_by_policy():
    request = create_demo_validator_assisted_card_tap_request()

    policy = create_demo_mvp_sync_policy(
        driver_console_must_not_be_mandatory=False,
    )

    result = evaluate_mvp_solidary_sync_option(
        request=request,
        policy=policy,
    )

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "driver_console_cannot_be_mandatory" in result.hard_risk_flags


def test_sync_window_expired_rejects_option():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_mvp_red_sube_context(
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=30),
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-window-expired-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        red_sube_context=context,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.window_matched is False
    assert result.blocks_solidary_bonus_flow is True
    assert "sync_window_expired" in result.hard_risk_flags


def test_validator_assisted_uses_shorter_window_than_mobile_options():
    policy = create_demo_mvp_sync_policy(
        mobile_to_mobile_window_minutes=10,
        priority_phone_nfc_window_minutes=10,
        validator_assisted_window_minutes=8,
    )

    request = create_demo_validator_assisted_card_tap_request()

    result = evaluate_mvp_solidary_sync_option(
        request=request,
        policy=policy,
    )

    assert result.window_minutes == 8
    assert result.window_matched is True
    assert result.status == MvpSyncStatus.READY_WITH_AUDIT


def test_discount_is_capped_at_100_percent_demo():
    request = create_demo_mobile_to_mobile_request()

    policy = create_demo_mvp_sync_policy(
        bonus_extra_discount_bps_demo=5000,
        max_total_discount_bps_demo=9000,
    )

    result = evaluate_mvp_solidary_sync_option(
        request=request,
        policy=policy,
    )

    assert result.status == MvpSyncStatus.READY
    assert result.base_red_sube_discount_bps_demo == 5000
    assert result.bonus_extra_discount_bps_demo == 5000
    assert result.final_demo_discount_bps_if_eligible == 9000
    assert "discount_cap_applied_demo" in result.audit_flags


def test_no_shared_transport_context_rejects():
    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-no-shared-context-001",
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

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert result.security_summary["context_score"] == 0
    assert "no_shared_transport_context" in result.hard_risk_flags


def test_legal_priority_seat_is_not_eligible():
    request = create_demo_mobile_to_mobile_request()

    modified = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-legal-priority-seat-001",
        option=request.option,
        participant_context=request.participant_context,
        red_sube_context=request.red_sube_context,
        seat_type=SeatType.LEGAL_PRIORITY,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(modified)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "legal_priority_seat_not_eligible_for_bonus" in result.hard_risk_flags


def test_without_priority_confirmation_rejects():
    request = create_demo_mobile_to_mobile_request()

    modified = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-without-priority-confirmation-001",
        option=request.option,
        participant_context=request.participant_context,
        red_sube_context=request.red_sube_context,
        priority_user_confirms_seat_yield=False,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(modified)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_user_confirmation_required" in result.hard_risk_flags


def test_collaborator_unilateral_claim_rejects():
    request = create_demo_mobile_to_mobile_request()

    modified = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-collaborator-unilateral-claim-001",
        option=request.option,
        participant_context=request.participant_context,
        red_sube_context=request.red_sube_context,
        collaborator_claims_unilaterally=True,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(modified)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_unilateral_claim" in result.hard_risk_flags


def test_without_voluntary_seat_yield_rejects():
    request = create_demo_mobile_to_mobile_request()

    modified = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-without-voluntary-seat-yield-001",
        option=request.option,
        participant_context=request.participant_context,
        red_sube_context=request.red_sube_context,
        voluntary_seat_yield_declared=False,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(modified)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "voluntary_seat_yield_required" in result.hard_risk_flags


def test_inactive_priority_attribute_rejects():
    participant = create_demo_mvp_participant_context(
        priority_user_has_active_attribute=False,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-inactive-priority-attribute-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        participant_context=participant,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_attribute_not_active" in result.hard_risk_flags


def test_priority_need_not_accredited_rejects():
    participant = create_demo_mvp_participant_context(
        priority_need_previously_accredited=False,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-priority-need-not-accredited-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        participant_context=participant,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_need_not_previously_accredited" in result.hard_risk_flags


def test_unpaid_priority_validation_rejects():
    context = create_demo_mvp_red_sube_context(
        priority_paid_validation_confirmed=False,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-unpaid-priority-validation-001",
        red_sube_context=context,
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_paid_validation_required" in result.hard_risk_flags


def test_unpaid_collaborator_validation_rejects_for_mobile_option():
    context = create_demo_mvp_red_sube_context(
        collaborator_paid_validation_confirmed=False,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-unpaid-collaborator-validation-001",
        red_sube_context=context,
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_paid_validation_required" in result.hard_risk_flags


def test_validator_assisted_allows_collaborator_second_tap_instead_of_prior_paid_collaborator_validation():
    context = create_demo_mvp_red_sube_context(
        collaborator_paid_validation_confirmed=False,
    )

    participant = create_demo_mvp_participant_context(
        priority_has_mobile_device=False,
        priority_mobile_has_nfc=False,
        collaborator_has_mobile_device=False,
        collaborator_has_physical_sube_card=True,
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-validator-second-tap-no-prior-collaborator-paid-001",
        option=MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP,
        participant_context=participant,
        red_sube_context=context,
        mobile_handshake_available=False,
        nfc_card_tap_available=False,
        validator_second_tap_available=True,
        assisted_activation_actor=AssistedActivationActor.DRIVER_CONSOLE_OPTIONAL,
        same_vehicle_demo_id=True,
        good_faith_social_recognition_declared=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert "collaborator_paid_validation_required" not in result.hard_risk_flags
    assert result.status == MvpSyncStatus.READY_WITH_AUDIT
    assert result.opens_bonus_evaluation_window is True


def test_same_user_token_rejects():
    participant = create_demo_mvp_participant_context(
        priority_user_token="test-same-user-token",
        collaborator_user_token="test-same-user-token",
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-same-user-token-001",
        participant_context=participant,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "same_user_token_not_allowed" in result.hard_risk_flags


def test_free_text_tokens_are_rejected():
    participant = create_demo_mvp_participant_context(
        collaborator_user_token="quiero bono solidario gratis",
    )

    request = create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="test-free-text-token-001",
        participant_context=participant,
        mobile_handshake_available=True,
    )

    result = evaluate_mvp_solidary_sync_option(request)

    assert result.status == MvpSyncStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_user_token_looks_like_free_text" in result.hard_risk_flags


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


def test_create_policy_rejects_invalid_values():
    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            mobile_to_mobile_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            priority_phone_nfc_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            validator_assisted_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            station_turnstile_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            benefit_validity_hours=0,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            bonus_extra_discount_bps_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            max_total_discount_bps_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            bonus_extra_discount_bps_demo=10001,
        )

    with pytest.raises(ValueError):
        create_demo_mvp_sync_policy(
            max_total_discount_bps_demo=10001,
        )


def test_create_participant_context_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_mvp_participant_context(
            priority_user_token="",
        )

    with pytest.raises(ValueError):
        create_demo_mvp_participant_context(
            priority_attribute_token="",
        )

    with pytest.raises(ValueError):
        create_demo_mvp_participant_context(
            collaborator_user_token="",
        )

    with pytest.raises(ValueError):
        create_demo_mvp_participant_context(
            collaborator_sube_card_token="",
        )


def test_create_red_sube_context_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_mvp_red_sube_context(
            network_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_mvp_red_sube_context(
            route_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_mvp_red_sube_context(
            service_window_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_mvp_red_sube_context(
            validator_or_turnstile_demo_id="",
        )


def test_create_request_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_mvp_sync_option_request(
            mvp_sync_event_demo_id="",
        )

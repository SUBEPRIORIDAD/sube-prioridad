from datetime import datetime, timedelta, timezone

import pytest

from mobile_proximity_sync_guard import (
    ProximityGuardStatus,
    ProximityMethod,
    ProximityStrength,
    TransportAccessContext,
    assert_no_prohibited_fields,
    create_demo_mobile_device_binding,
    create_demo_no_mobile_proximity_signal,
    create_demo_proximity_guard_policy,
    create_demo_proximity_signal,
    create_demo_station_extended_proximity_signal,
    evaluate_mobile_proximity_sync_guard,
    result_to_dict,
    run_demo,
    run_no_mobile_demo,
    run_station_demo,
)


def test_run_demo_accepts_reinforced_mobile_proximity():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Guardia Demo de Proximidad Móvil No Excluyente"
    assert result["demo_mode"] is True

    assert result["status"] == "accepted_reinforced"
    assert result["proximity_strength"] == "strong"
    assert result["mobile_filter_available"] is True
    assert result["mobile_filter_used"] is True
    assert result["proximity_reinforced"] is True
    assert result["non_exclusive_filter"] is True
    assert result["blocks_solidary_bonus_flow"] is False

    assert result["access_context"] == "in_vehicle_after_payment"
    assert result["proximity_method"] == "qr_temporary_demo"
    assert result["access_window_matched"] is True
    assert result["trip_window_matched"] is True
    assert result["device_binding_matched"] is True
    assert result["handshake_signal_present"] is True
    assert result["same_transport_context_score"] > 0
    assert result["hard_risk_flags"] == []

    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]
    assert "GPS exacto" in result["privacy_notice"]
    assert "ausencia de celular no bloquea" in result["privacy_notice"].lower()
    assert "chofer no verifica" in result["driver_burden"].lower()

    assert "Filtro móvil no excluyente." in result["warnings"]
    assert "Sin obligación de tener celular." in result["warnings"]
    assert "La proximidad móvil refuerza, pero no reemplaza los demás filtros." in result["warnings"]


def test_run_station_demo_accepts_reinforced_extended_context():
    result = run_station_demo()

    assert result["status"] == "accepted_reinforced"
    assert result["mobile_filter_available"] is True
    assert result["mobile_filter_used"] is True
    assert result["proximity_reinforced"] is True
    assert result["blocks_solidary_bonus_flow"] is False

    assert result["access_context"] == "platform_wait_after_turnstile"
    assert result["proximity_method"] == "ble_nearby_demo"
    assert result["proximity_strength"] == "strong"

    assert result["access_window_matched"] is True
    assert result["trip_window_matched"] is True
    assert result["device_binding_matched"] is True
    assert result["handshake_signal_present"] is True
    assert result["same_transport_context_score"] > 0
    assert result["hard_risk_flags"] == []

    assert result["security_summary"]["station_extended_access_window_minutes"] == 60
    assert result["security_summary"]["mobile_required_for_bonus"] is False
    assert result["security_summary"]["require_mobile_for_extended_context"] is False
    assert result["security_summary"]["same_station_demo_id"] is True
    assert result["security_summary"]["same_platform_demo_id"] is True


def test_run_no_mobile_demo_does_not_block_flow():
    result = run_no_mobile_demo()

    assert result["status"] == "accepted_without_mobile_evidence"
    assert result["proximity_strength"] == "not_available"
    assert result["mobile_filter_available"] is False
    assert result["mobile_filter_used"] is False
    assert result["proximity_reinforced"] is False
    assert result["non_exclusive_filter"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["requires_audit_review"] is True

    assert "priority_user_mobile_not_available_non_blocking" in result["audit_flags"]
    assert "mobile_filter_not_available_non_blocking" in result["audit_flags"]
    assert "extended_context_without_mobile_reinforcement" in result["audit_flags"]
    assert "station_or_platform_context_audit" in result["audit_flags"]

    assert result["hard_risk_flags"] == []
    assert result["audit_record_demo"]["mobile_filter_available"] is False
    assert result["audit_record_demo"]["mobile_filter_used"] is False


def test_no_mobile_signal_is_non_exclusive_and_auditable():
    signal = create_demo_no_mobile_proximity_signal()

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.ACCEPTED_WITHOUT_MOBILE_EVIDENCE
    assert result.proximity_strength == ProximityStrength.NOT_AVAILABLE
    assert result.mobile_filter_available is False
    assert result.mobile_filter_used is False
    assert result.proximity_reinforced is False
    assert result.non_exclusive_filter is True
    assert result.blocks_solidary_bonus_flow is False
    assert result.requires_audit_review is True

    assert "mobile_filter_not_available_non_blocking" in result.audit_flags
    assert "extended_context_without_mobile_reinforcement" in result.audit_flags
    assert result.hard_risk_flags == []


def test_one_user_without_mobile_does_not_block_bonus_flow():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-one-user-without-mobile-001",
        priority_user_has_mobile_device=True,
        collaborator_has_mobile_device=False,
        access_context=TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT,
        same_vehicle_demo_id=True,
        same_service_window_demo_id=True,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.ACCEPTED_WITHOUT_MOBILE_EVIDENCE
    assert result.mobile_filter_available is False
    assert result.mobile_filter_used is False
    assert result.blocks_solidary_bonus_flow is False
    assert "collaborator_mobile_not_available_non_blocking" in result.audit_flags
    assert "mobile_filter_not_available_non_blocking" in result.audit_flags


def test_mobile_available_but_not_used_does_not_block_when_policy_is_non_exclusive():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-mobile-available-not-used-001",
        proximity_method=ProximityMethod.NONE_AVAILABLE,
        qr_or_code_token_demo=None,
        nfc_handshake_token_demo=None,
        ble_ephemeral_token_demo=None,
        priority_user_has_mobile_device=True,
        collaborator_has_mobile_device=True,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.ACCEPTED_WITHOUT_MOBILE_EVIDENCE
    assert result.mobile_filter_available is True
    assert result.mobile_filter_used is False
    assert result.blocks_solidary_bonus_flow is False
    assert result.requires_audit_review is True
    assert "mobile_filter_available_but_not_used" in result.audit_flags


def test_result_to_dict_is_serializable():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-result-to-dict-001",
    )

    result = evaluate_mobile_proximity_sync_guard(signal)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Guardia Demo de Proximidad Móvil No Excluyente"
    assert data["demo_mode"] is True
    assert isinstance(data["security_summary"], dict)
    assert isinstance(data["audit_record_demo"], dict)
    assert isinstance(data["hard_risk_flags"], list)
    assert isinstance(data["audit_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_station_extended_context_without_mobile_does_not_block_by_default():
    timestamp = datetime.now(timezone.utc)

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-station-no-mobile-default-001",
        access_context=TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        proximity_method=ProximityMethod.NONE_AVAILABLE,
        priority_user_has_mobile_device=False,
        collaborator_has_mobile_device=False,
        qr_or_code_token_demo=None,
        nfc_handshake_token_demo=None,
        ble_ephemeral_token_demo=None,
        same_station_demo_id=True,
        same_platform_demo_id=True,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_service_window_demo_id=True,
        created_at_utc=timestamp,
        sync_attempted_at_utc=timestamp + timedelta(minutes=40),
    )

    policy = create_demo_proximity_guard_policy(
        require_mobile_for_extended_context=False,
        mobile_required_for_bonus=False,
    )

    result = evaluate_mobile_proximity_sync_guard(
        signal=signal,
        policy=policy,
    )

    assert result.status == ProximityGuardStatus.ACCEPTED_WITHOUT_MOBILE_EVIDENCE
    assert result.mobile_filter_available is False
    assert result.mobile_filter_used is False
    assert result.blocks_solidary_bonus_flow is False
    assert result.requires_audit_review is True
    assert result.hard_risk_flags == []
    assert "extended_context_without_mobile_reinforcement" in result.audit_flags


def test_station_extended_context_can_block_only_if_policy_explicitly_requires_mobile():
    timestamp = datetime.now(timezone.utc)

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-station-mobile-required-policy-001",
        access_context=TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        proximity_method=ProximityMethod.NONE_AVAILABLE,
        priority_user_has_mobile_device=False,
        collaborator_has_mobile_device=True,
        same_station_demo_id=True,
        same_platform_demo_id=True,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_service_window_demo_id=True,
        created_at_utc=timestamp,
        sync_attempted_at_utc=timestamp + timedelta(minutes=35),
    )

    policy = create_demo_proximity_guard_policy(
        require_mobile_for_extended_context=True,
    )

    result = evaluate_mobile_proximity_sync_guard(
        signal=signal,
        policy=policy,
    )

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "extended_context_mobile_required_by_policy" in result.hard_risk_flags


def test_mobile_required_for_bonus_policy_can_block_when_explicitly_enabled():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-mobile-required-for-bonus-policy-001",
        priority_user_has_mobile_device=False,
        collaborator_has_mobile_device=False,
        proximity_method=ProximityMethod.NONE_AVAILABLE,
    )

    policy = create_demo_proximity_guard_policy(
        mobile_required_for_bonus=True,
    )

    result = evaluate_mobile_proximity_sync_guard(
        signal=signal,
        policy=policy,
    )

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "mobile_required_by_policy_but_not_available" in result.hard_risk_flags


def test_hard_risk_same_user_token_blocks_flow_even_without_mobile():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-hard-risk-same-user-no-mobile-001",
        priority_user_token="test-same-user-token",
        collaborator_token="test-same-user-token",
        priority_user_has_mobile_device=False,
        collaborator_has_mobile_device=False,
        proximity_method=ProximityMethod.NONE_AVAILABLE,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "same_user_token_not_allowed" in result.hard_risk_flags


def test_hard_risk_no_priority_user_confirmation_blocks_flow():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-no-priority-confirmation-001",
        priority_user_confirms_sync=False,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_user_confirmation_required" in result.hard_risk_flags


def test_hard_risk_collaborator_unilateral_claim_blocks_flow():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-collaborator-unilateral-001",
        collaborator_claims_unilaterally=True,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_unilateral_claim" in result.hard_risk_flags


def test_hard_risk_access_window_not_matched_blocks_flow():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-access-window-not-matched-001",
        access_window_matched=False,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "access_window_not_matched" in result.hard_risk_flags


def test_hard_risk_trip_window_not_matched_blocks_flow():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-trip-window-not-matched-001",
        trip_window_matched=False,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "trip_window_not_matched" in result.hard_risk_flags


def test_hard_risk_access_context_window_expired_blocks_flow():
    timestamp = datetime.now(timezone.utc)

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-access-context-window-expired-001",
        access_context=TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT,
        created_at_utc=timestamp,
        sync_attempted_at_utc=timestamp + timedelta(minutes=25),
    )

    policy = create_demo_proximity_guard_policy(
        in_vehicle_sync_window_minutes=10,
    )

    result = evaluate_mobile_proximity_sync_guard(
        signal=signal,
        policy=policy,
    )

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "access_context_window_expired" in result.hard_risk_flags


def test_hard_risk_no_shared_transport_context_blocks_flow():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-no-shared-transport-context-001",
        same_network_demo_id=False,
        same_route_demo_id=False,
        same_station_demo_id=False,
        same_platform_demo_id=False,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_service_window_demo_id=False,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.same_transport_context_score == 0
    assert result.blocks_solidary_bonus_flow is True
    assert "no_shared_transport_context" in result.hard_risk_flags


def test_hard_risk_same_payment_method_token_blocks_flow():
    same_payment = "test-same-payment-method-token"

    priority_device = create_demo_mobile_device_binding(
        device_session_token="test-priority-device-same-payment-001",
        account_demo_token="test-priority-account-same-payment-001",
        payment_method_demo_token=same_payment,
        sube_card_demo_token="test-priority-card-same-payment-001",
    )

    collaborator_device = create_demo_mobile_device_binding(
        device_session_token="test-collaborator-device-same-payment-001",
        account_demo_token="test-collaborator-account-same-payment-001",
        payment_method_demo_token=same_payment,
        sube_card_demo_token="test-collaborator-card-same-payment-001",
    )

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-same-payment-method-001",
        priority_device=priority_device,
        collaborator_device=collaborator_device,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "same_payment_method_token_not_allowed" in result.hard_risk_flags


def test_hard_risk_same_sube_card_token_blocks_flow():
    same_card = "test-same-sube-card-token"

    priority_device = create_demo_mobile_device_binding(
        device_session_token="test-priority-device-same-card-001",
        account_demo_token="test-priority-account-same-card-001",
        payment_method_demo_token="test-priority-payment-same-card-001",
        sube_card_demo_token=same_card,
    )

    collaborator_device = create_demo_mobile_device_binding(
        device_session_token="test-collaborator-device-same-card-001",
        account_demo_token="test-collaborator-account-same-card-001",
        payment_method_demo_token="test-collaborator-payment-same-card-001",
        sube_card_demo_token=same_card,
    )

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-same-sube-card-001",
        priority_device=priority_device,
        collaborator_device=collaborator_device,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "same_sube_card_token_not_allowed" in result.hard_risk_flags


def test_inactive_device_binding_is_audit_flag_not_hard_block_by_default():
    priority_device = create_demo_mobile_device_binding(
        device_session_token="test-priority-inactive-device-001",
        account_demo_token="test-priority-inactive-account-001",
        payment_method_demo_token="test-priority-inactive-payment-001",
        sube_card_demo_token="test-priority-inactive-card-001",
        device_binding_active=False,
    )

    collaborator_device = create_demo_mobile_device_binding(
        device_session_token="test-collaborator-active-device-001",
        account_demo_token="test-collaborator-active-account-001",
        payment_method_demo_token="test-collaborator-active-payment-001",
        sube_card_demo_token="test-collaborator-active-card-001",
    )

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-inactive-device-binding-001",
        priority_device=priority_device,
        collaborator_device=collaborator_device,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.ACCEPTED_REINFORCED
    assert result.blocks_solidary_bonus_flow is False
    assert "priority_device_binding_inactive_audit" in result.audit_flags


def test_mobile_not_linked_to_payment_is_audit_flag_not_hard_block_by_default():
    priority_device = create_demo_mobile_device_binding(
        device_session_token="test-priority-mobile-not-linked-001",
        account_demo_token="test-priority-account-not-linked-001",
        payment_method_demo_token="test-priority-payment-not-linked-001",
        sube_card_demo_token="test-priority-card-not-linked-001",
        mobile_account_linked_to_payment_demo=False,
    )

    collaborator_device = create_demo_mobile_device_binding(
        device_session_token="test-collaborator-mobile-linked-001",
        account_demo_token="test-collaborator-account-linked-001",
        payment_method_demo_token="test-collaborator-payment-linked-001",
        sube_card_demo_token="test-collaborator-card-linked-001",
    )

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-mobile-not-linked-to-payment-001",
        priority_device=priority_device,
        collaborator_device=collaborator_device,
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.ACCEPTED_REINFORCED
    assert result.blocks_solidary_bonus_flow is False
    assert "priority_mobile_not_linked_to_payment_demo_audit" in result.audit_flags


def test_offline_signal_can_be_deferred_without_blocking():
    timestamp = datetime.now(timezone.utc)

    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-offline-deferred-001",
        access_context=TransportAccessContext.PLATFORM_WAIT_AFTER_TURNSTILE,
        proximity_method=ProximityMethod.QR_TEMPORARY_DEMO,
        qr_or_code_token_demo="test-offline-qr-token-001",
        same_station_demo_id=True,
        same_platform_demo_id=True,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        offline_mode=True,
        created_at_utc=timestamp,
        sync_attempted_at_utc=timestamp + timedelta(minutes=30),
    )

    policy = create_demo_proximity_guard_policy(
        allow_offline_deferred_validation=True,
        max_pending_offline_minutes=120,
    )

    result = evaluate_mobile_proximity_sync_guard(
        signal=signal,
        policy=policy,
    )

    assert result.status == ProximityGuardStatus.DEFERRED_OFFLINE_VALIDATION
    assert result.blocks_solidary_bonus_flow is False
    assert result.requires_deferred_validation is True
    assert result.requires_audit_review is True
    assert "offline_validation_pending" in result.audit_flags
    assert result.hard_risk_flags == []


def test_offline_signal_blocks_only_when_policy_disallows_deferred_validation():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-offline-not-allowed-001",
        offline_mode=True,
    )

    policy = create_demo_proximity_guard_policy(
        allow_offline_deferred_validation=False,
    )

    result = evaluate_mobile_proximity_sync_guard(
        signal=signal,
        policy=policy,
    )

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "offline_validation_not_allowed" in result.hard_risk_flags


def test_manual_code_method_reinforces_when_code_token_exists():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-manual-code-with-token-001",
        proximity_method=ProximityMethod.MANUAL_CODE_DEMO,
        qr_or_code_token_demo="test-manual-code-token-001",
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.ACCEPTED_REINFORCED
    assert result.handshake_signal_present is True
    assert result.mobile_filter_used is True
    assert result.proximity_reinforced is True
    assert result.blocks_solidary_bonus_flow is False


def test_nfc_method_reinforces_when_nfc_token_exists():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-nfc-handshake-001",
        proximity_method=ProximityMethod.NFC_TEMPORARY_DEMO,
        qr_or_code_token_demo=None,
        nfc_handshake_token_demo="test-nfc-token-001",
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.ACCEPTED_REINFORCED
    assert result.handshake_signal_present is True
    assert result.mobile_filter_used is True
    assert result.proximity_reinforced is True
    assert result.blocks_solidary_bonus_flow is False


def test_rejects_free_text_tokens_as_hard_risk():
    signal = create_demo_proximity_signal(
        sync_event_demo_id="test-free-text-token-001",
        collaborator_token="quiero bono solidario gratis",
    )

    result = evaluate_mobile_proximity_sync_guard(signal)

    assert result.status == ProximityGuardStatus.REJECTED_HARD_RISK
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_token_looks_like_free_text" in result.hard_risk_flags


def test_assert_no_prohibited_fields_rejects_sensitive_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "diagnostico": "dato no permitido",
                "cud": "dato no permitido",
                "gps": "-34.0,-58.0",
                "telefono": "dato no permitido",
                "imei": "dato no permitido",
                "mac": "dato no permitido",
            }
        )

    message = str(error.value).lower()

    assert "dni" in message
    assert "diagnostico" in message
    assert "cud" in message
    assert "gps" in message
    assert "telefono" in message
    assert "imei" in message
    assert "mac" in message


def test_create_policy_rejects_invalid_values():
    with pytest.raises(ValueError):
        create_demo_proximity_guard_policy(
            in_vehicle_sync_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_proximity_guard_policy(
            station_extended_access_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_proximity_guard_policy(
            sync_moment_proximity_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_proximity_guard_policy(
            max_pending_offline_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_proximity_guard_policy(
            in_vehicle_sync_window_minutes=20,
            station_extended_access_window_minutes=10,
        )


def test_create_mobile_device_binding_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_mobile_device_binding(
            device_session_token="",
        )

    with pytest.raises(ValueError):
        create_demo_mobile_device_binding(
            account_demo_token="",
        )

    with pytest.raises(ValueError):
        create_demo_mobile_device_binding(
            payment_method_demo_token="",
        )

    with pytest.raises(ValueError):
        create_demo_mobile_device_binding(
            sube_card_demo_token="",
        )


def test_create_proximity_signal_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_proximity_signal(
            sync_event_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_proximity_signal(
            priority_user_token="",
        )

    with pytest.raises(ValueError):
        create_demo_proximity_signal(
            collaborator_token="",
        )

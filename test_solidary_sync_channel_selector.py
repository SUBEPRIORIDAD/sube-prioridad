from datetime import datetime, timedelta, timezone

import pytest

from solidary_sync_channel_selector import (
    ConfirmationMode,
    SyncChannel,
    SyncChannelStatus,
    TransportMode,
    ValidationPointType,
    WindowKind,
    assert_no_prohibited_fields,
    create_demo_no_mobile_validator_based_request,
    create_demo_red_sube_validation_context,
    create_demo_solidary_sync_channel_request,
    create_demo_station_no_mobile_deferred_request,
    create_demo_sync_channel_policy,
    create_demo_user_device_availability,
    evaluate_solidary_sync_channel,
    result_to_dict,
    run_demo,
    run_no_mobile_validator_demo,
    run_station_no_mobile_deferred_demo,
)


def test_run_demo_selects_priority_mobile_nfc_card_tap():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Selector Demo de Canales de Sincronización Solidaria"
    assert result["demo_mode"] is True

    assert result["status"] == "ready_reinforced"
    assert result["selected_channel"] == "priority_mobile_nfc_card_tap"
    assert result["window_kind"] == "in_vehicle_short_window"
    assert result["window_minutes"] == 10
    assert result["window_matched"] is True

    assert result["mobile_required"] is False
    assert result["priority_mobile_available"] is True
    assert result["collaborator_mobile_available"] is False
    assert result["no_mobile_path_supported"] is True

    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["hard_risk_flags"] == []

    assert "Sin obligación de tener celular." in result["warnings"]
    assert "El usuario SUBE Prioridad puede no tener celular." in result["warnings"]
    assert "El colaborador puede no tener celular." in result["warnings"]
    assert "Cada tipo de validadora o molinete puede tener una ventana temporal distinta." in result["warnings"]


def test_no_mobile_validator_demo_opens_contextual_window_without_blocking():
    result = run_no_mobile_validator_demo()

    assert result["status"] == "ready_without_mobile"
    assert result["selected_channel"] == "validator_context_window"
    assert result["window_kind"] == "in_vehicle_short_window"
    assert result["window_minutes"] == 10
    assert result["window_matched"] is True

    assert result["mobile_required"] is False
    assert result["priority_mobile_available"] is False
    assert result["collaborator_mobile_available"] is False
    assert result["no_mobile_path_supported"] is True

    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["requires_audit_review"] is True
    assert result["hard_risk_flags"] == []

    assert "priority_user_without_mobile_supported" in result["audit_flags"]
    assert "collaborator_without_mobile_supported" in result["audit_flags"]
    assert "no_mobile_both_users_non_blocking" in result["audit_flags"]
    assert "validator_window_opened_demo" in result["audit_flags"]
    assert "red_sube_contextual_channel_audit" in result["audit_flags"]


def test_station_no_mobile_deferred_demo_opens_extended_window():
    result = run_station_no_mobile_deferred_demo()

    assert result["status"] == "ready_without_mobile"
    assert result["selected_channel"] == "turnstile_or_station_window"
    assert result["window_kind"] == "station_extended_window"
    assert result["window_minutes"] == 60
    assert result["window_matched"] is True

    assert result["mobile_required"] is False
    assert result["priority_mobile_available"] is False
    assert result["collaborator_mobile_available"] is False

    assert result["opens_bonus_evaluation_window"] is True
    assert result["blocks_solidary_bonus_flow"] is False
    assert result["requires_audit_review"] is True

    assert "priority_user_without_mobile_supported" in result["audit_flags"]
    assert "collaborator_without_mobile_supported" in result["audit_flags"]
    assert "turnstile_or_station_window_opened_demo" in result["audit_flags"]
    assert "extended_window_audit" in result["audit_flags"]


def test_result_to_dict_is_serializable():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-result-to-dict-001",
    )

    result = evaluate_solidary_sync_channel(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Selector Demo de Canales de Sincronización Solidaria"
    assert data["demo_mode"] is True
    assert isinstance(data["security_summary"], dict)
    assert isinstance(data["hard_risk_flags"], list)
    assert isinstance(data["audit_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_priority_user_without_mobile_can_still_use_validator_context_window():
    request = create_demo_no_mobile_validator_based_request()

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.READY_WITHOUT_MOBILE
    assert result.selected_channel == SyncChannel.VALIDATOR_CONTEXT_WINDOW
    assert result.window_kind == WindowKind.IN_VEHICLE_SHORT_WINDOW
    assert result.mobile_required is False
    assert result.priority_mobile_available is False
    assert result.collaborator_mobile_available is False
    assert result.opens_bonus_evaluation_window is True
    assert result.blocks_solidary_bonus_flow is False
    assert "no_mobile_both_users_non_blocking" in result.audit_flags


def test_onboard_train_validator_uses_short_window():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_red_sube_validation_context(
        transport_mode=TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR,
        validation_point_type=ValidationPointType.ONBOARD_TRAIN_VALIDATOR,
        validator_or_turnstile_demo_id="test-onboard-train-validator-001",
        vehicle_demo_id=None,
        trainset_demo_id="test-trainset-001",
        station_demo_id=None,
        platform_demo_id=None,
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=8),
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-onboard-train-short-window-001",
        priority_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        collaborator_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        red_sube_context=context,
        confirmation_mode=ConfirmationMode.VALIDATOR_WINDOW_PENDING_CONFIRMATION,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=True,
        same_station_demo_id=False,
        same_platform_demo_id=False,
        same_validator_or_turnstile_demo_id=True,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.READY_WITHOUT_MOBILE
    assert result.selected_channel == SyncChannel.VALIDATOR_CONTEXT_WINDOW
    assert result.window_kind == WindowKind.ONBOARD_TRAIN_SHORT_WINDOW
    assert result.window_minutes == 10
    assert result.window_matched is True
    assert result.opens_bonus_evaluation_window is True
    assert result.blocks_solidary_bonus_flow is False


def test_onboard_train_validator_rejects_when_short_window_expires():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_red_sube_validation_context(
        transport_mode=TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR,
        validation_point_type=ValidationPointType.ONBOARD_TRAIN_VALIDATOR,
        validator_or_turnstile_demo_id="test-onboard-train-expired-validator-001",
        trainset_demo_id="test-trainset-expired-001",
        vehicle_demo_id=None,
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=25),
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-onboard-train-window-expired-001",
        red_sube_context=context,
        priority_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        collaborator_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        same_vehicle_demo_id=False,
        same_trainset_demo_id=True,
        same_validator_or_turnstile_demo_id=True,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.selected_channel == SyncChannel.NO_CHANNEL_AVAILABLE
    assert result.window_kind == WindowKind.ONBOARD_TRAIN_SHORT_WINDOW
    assert result.window_matched is False
    assert result.blocks_solidary_bonus_flow is True
    assert "sync_window_expired" in result.hard_risk_flags


def test_station_turnstile_uses_extended_window():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_red_sube_validation_context(
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        validator_or_turnstile_demo_id="test-station-turnstile-001",
        vehicle_demo_id=None,
        trainset_demo_id=None,
        station_demo_id="test-station-001",
        platform_demo_id="test-platform-001",
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=4),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=55),
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-station-extended-window-001",
        red_sube_context=context,
        priority_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        collaborator_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_station_demo_id=True,
        same_platform_demo_id=True,
        same_validator_or_turnstile_demo_id=True,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.READY_WITHOUT_MOBILE
    assert result.selected_channel == SyncChannel.TURNSTILE_OR_STATION_WINDOW
    assert result.window_kind == WindowKind.STATION_EXTENDED_WINDOW
    assert result.window_minutes == 60
    assert result.window_matched is True
    assert result.opens_bonus_evaluation_window is True
    assert result.requires_audit_review is True
    assert "extended_window_audit" in result.audit_flags


def test_station_turnstile_rejects_when_extended_window_expires():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_red_sube_validation_context(
        transport_mode=TransportMode.TRAIN,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        validator_or_turnstile_demo_id="test-station-expired-turnstile-001",
        vehicle_demo_id=None,
        trainset_demo_id=None,
        station_demo_id="test-station-expired-001",
        platform_demo_id="test-platform-expired-001",
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=3),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=75),
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-station-window-expired-001",
        red_sube_context=context,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_station_demo_id=True,
        same_platform_demo_id=True,
        same_validator_or_turnstile_demo_id=True,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.selected_channel == SyncChannel.NO_CHANNEL_AVAILABLE
    assert result.window_kind == WindowKind.STATION_EXTENDED_WINDOW
    assert result.window_matched is False
    assert result.blocks_solidary_bonus_flow is True
    assert "sync_window_expired" in result.hard_risk_flags


def test_collaborator_mobile_qr_channel_is_selected_when_priority_has_no_nfc_but_collaborator_has_app():
    priority_device = create_demo_user_device_availability(
        has_mobile_device=False,
        has_nfc_capable_device=False,
        has_app_or_account_access_now=False,
        has_connectivity_now=False,
        has_physical_sube_card=True,
    )

    collaborator_device = create_demo_user_device_availability(
        has_mobile_device=True,
        has_nfc_capable_device=True,
        has_app_or_account_access_now=True,
        has_connectivity_now=True,
        has_physical_sube_card=True,
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-collaborator-mobile-qr-001",
        priority_device_availability=priority_device,
        collaborator_device_availability=collaborator_device,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.READY_REINFORCED
    assert result.selected_channel == SyncChannel.COLLABORATOR_MOBILE_QR_OR_CODE
    assert result.priority_mobile_available is False
    assert result.collaborator_mobile_available is True
    assert result.opens_bonus_evaluation_window is True
    assert result.blocks_solidary_bonus_flow is False


def test_priority_mobile_nfc_channel_is_selected_when_priority_has_nfc_and_collaborator_has_card():
    priority_device = create_demo_user_device_availability(
        has_mobile_device=True,
        has_nfc_capable_device=True,
        has_app_or_account_access_now=True,
        has_connectivity_now=True,
        has_physical_sube_card=True,
    )

    collaborator_device = create_demo_user_device_availability(
        has_mobile_device=False,
        has_nfc_capable_device=False,
        has_app_or_account_access_now=False,
        has_connectivity_now=False,
        has_physical_sube_card=True,
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-priority-mobile-nfc-001",
        priority_device_availability=priority_device,
        collaborator_device_availability=collaborator_device,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.READY_REINFORCED
    assert result.selected_channel == SyncChannel.PRIORITY_MOBILE_NFC_CARD_TAP
    assert result.mobile_required is False
    assert result.opens_bonus_evaluation_window is True
    assert result.blocks_solidary_bonus_flow is False


def test_terminal_validator_can_select_assisted_channel():
    timestamp = datetime.now(timezone.utc)

    context = create_demo_red_sube_validation_context(
        transport_mode=TransportMode.OTHER_PUBLIC_TRANSPORT,
        validation_point_type=ValidationPointType.TERMINAL_VALIDATOR,
        validator_or_turnstile_demo_id="test-terminal-validator-001",
        vehicle_demo_id=None,
        trainset_demo_id=None,
        station_demo_id="test-terminal-001",
        platform_demo_id=None,
        priority_validation_timestamp_utc=timestamp,
        collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=2),
        sync_attempt_timestamp_utc=timestamp + timedelta(minutes=30),
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-terminal-assisted-channel-001",
        red_sube_context=context,
        confirmation_mode=ConfirmationMode.ASSISTED_CONFIRMATION,
        priority_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        collaborator_device_availability=create_demo_user_device_availability(
            has_mobile_device=False,
            has_nfc_capable_device=False,
            has_app_or_account_access_now=False,
            has_connectivity_now=False,
            has_physical_sube_card=True,
        ),
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_station_demo_id=True,
        same_platform_demo_id=False,
        same_validator_or_turnstile_demo_id=True,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.READY_DEFERRED_CONFIRMATION
    assert result.selected_channel == SyncChannel.ASSISTED_STATION_OR_TERMINAL_CHANNEL
    assert result.window_kind == WindowKind.TERMINAL_EXTENDED_WINDOW
    assert result.window_matched is True
    assert result.opens_bonus_evaluation_window is True
    assert result.requires_audit_review is True


def test_missing_priority_confirmation_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-missing-confirmation-001",
        confirmation_mode=ConfirmationMode.MISSING,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_confirmation_missing" in result.hard_risk_flags


def test_priority_user_cannot_confirm_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-cannot-confirm-001",
        priority_user_confirms_or_can_confirm=False,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_user_cannot_confirm" in result.hard_risk_flags


def test_collaborator_unilateral_claim_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-collaborator-unilateral-001",
        collaborator_claims_unilaterally=True,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_unilateral_claim" in result.hard_risk_flags


def test_without_voluntary_seat_yield_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-no-voluntary-seat-yield-001",
        voluntary_seat_yield_declared=False,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "voluntary_seat_yield_required" in result.hard_risk_flags


def test_inactive_priority_attribute_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-inactive-priority-attribute-001",
        priority_user_has_active_attribute=False,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_attribute_not_active" in result.hard_risk_flags


def test_priority_need_not_previously_accredited_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-need-not-accredited-001",
        priority_need_previously_accredited=False,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_need_not_previously_accredited" in result.hard_risk_flags


def test_unpaid_priority_validation_blocks_flow():
    context = create_demo_red_sube_validation_context(
        priority_paid_validation_confirmed=False,
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-unpaid-priority-validation-001",
        red_sube_context=context,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "priority_paid_validation_required" in result.hard_risk_flags


def test_unpaid_collaborator_validation_blocks_flow():
    context = create_demo_red_sube_validation_context(
        collaborator_paid_validation_confirmed=False,
    )

    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-unpaid-collaborator-validation-001",
        red_sube_context=context,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "collaborator_paid_validation_required" in result.hard_risk_flags


def test_same_user_token_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-same-user-token-001",
        priority_user_token="test-same-user-token",
        collaborator_user_token="test-same-user-token",
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "same_user_token_not_allowed" in result.hard_risk_flags


def test_no_shared_transport_context_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-no-shared-context-001",
        same_network_demo_id=False,
        same_route_demo_id=False,
        same_service_window_demo_id=False,
        same_validator_or_turnstile_demo_id=False,
        same_vehicle_demo_id=False,
        same_trainset_demo_id=False,
        same_station_demo_id=False,
        same_platform_demo_id=False,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.context_score == 0
    assert result.blocks_solidary_bonus_flow is True
    assert "no_shared_transport_context" in result.hard_risk_flags


def test_previous_handoff_security_rejected_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-previous-handoff-rejected-001",
        previous_handoff_security_accepted=False,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "previous_handoff_security_not_accepted" in result.hard_risk_flags


def test_previous_proximity_guard_blocking_blocks_flow():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-previous-proximity-blocks-001",
        previous_proximity_guard_blocks_flow=True,
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
    assert result.blocks_solidary_bonus_flow is True
    assert "previous_proximity_guard_blocks_flow" in result.hard_risk_flags


def test_free_text_tokens_are_rejected():
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-free-text-token-001",
        collaborator_user_token="quiero bono solidario gratis",
    )

    result = evaluate_solidary_sync_channel(request)

    assert result.status == SyncChannelStatus.REJECTED
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


def test_create_policy_rejects_invalid_values():
    with pytest.raises(ValueError):
        create_demo_sync_channel_policy(
            in_vehicle_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_sync_channel_policy(
            onboard_train_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_sync_channel_policy(
            station_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_sync_channel_policy(
            terminal_window_minutes=0,
        )

    with pytest.raises(ValueError):
        create_demo_sync_channel_policy(
            deferred_confirmation_window_hours=0,
        )

    with pytest.raises(ValueError):
        create_demo_sync_channel_policy(
            max_context_score_for_ready_without_mobile=0,
        )


def test_create_red_sube_context_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_red_sube_validation_context(
            network_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_red_sube_validation_context(
            route_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_red_sube_validation_context(
            service_window_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_red_sube_validation_context(
            validator_or_turnstile_demo_id="",
        )


def test_create_request_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_solidary_sync_channel_request(
            sync_channel_event_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_sync_channel_request(
            priority_user_token="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_sync_channel_request(
            priority_attribute_token="",
        )

    with pytest.raises(ValueError):
        create_demo_solidary_sync_channel_request(
            collaborator_user_token="",
        )

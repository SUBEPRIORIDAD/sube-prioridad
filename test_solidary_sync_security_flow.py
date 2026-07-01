from datetime import datetime, timedelta, timezone

import pytest

from solidary_sync_security_flow import (
    SeatType,
    SyncSecurityLedger,
    SyncStatus,
    assert_no_prohibited_fields,
    create_demo_sync_request,
    create_demo_transport_sync_context,
    result_to_dict,
    run_demo,
    simulate_solidary_sync_security,
)


def test_run_demo_accepts_valid_solidary_sync():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Flujo de Seguridad de Sincronización Solidaria"
    assert result["demo_mode"] is True
    assert result["status"] == "accepted"
    assert result["accepted_demo_sync"] is True
    assert result["solidary_point_demo"] == 1
    assert result["risk_flags"] == []
    assert "priority_signal_created" in result["stages_completed"]
    assert "collaborator_signal_created" in result["stages_completed"]
    assert "user_confirmation_received" in result["stages_completed"]
    assert "context_matched" in result["stages_completed"]
    assert "security_checks_passed" in result["stages_completed"]
    assert "demo_sync_ready" in result["stages_completed"]
    assert "usuario SUBE Prioridad" in result["priority_user_control"]
    assert "colaborador no puede" in result["collaborator_limit"].lower()
    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "Sin diagnóstico médico." in result["warnings"]
    assert "Sin CUD real." in result["warnings"]


def test_valid_sync_result_to_dict_is_serializable():
    ledger = SyncSecurityLedger()
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-to-dict-001",
        priority_user_token="test-priority-user-to-dict-001",
        priority_attribute_token="test-priority-attribute-to-dict-001",
        collaborator_token="test-collaborator-to-dict-001",
    )

    result = simulate_solidary_sync_security(
        request=request,
        ledger=ledger,
    )

    data = result_to_dict(result)

    assert data["status"] == "accepted"
    assert data["accepted_demo_sync"] is True
    assert data["solidary_point_demo"] == 1
    assert isinstance(data["stages_completed"], list)
    assert isinstance(data["risk_flags"], list)
    assert isinstance(data["warnings"], list)


def test_sync_rejects_outside_argentina_context():
    context = create_demo_transport_sync_context(country="Uruguay")

    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-outside-argentina-001",
        priority_user_token="test-priority-user-outside-001",
        priority_attribute_token="test-priority-attribute-outside-001",
        collaborator_token="test-collaborator-outside-001",
        actual_context=context,
        expected_context=context,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "outside_argentina_context" in result.risk_flags


def test_sync_rejects_priority_user_token_free_text():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-priority-free-text-001",
        priority_user_token="quiero viajar gratis",
        priority_attribute_token="test-priority-attribute-free-text-001",
        collaborator_token="test-collaborator-free-text-001",
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "priority_user_token_looks_like_free_text" in result.risk_flags


def test_sync_rejects_collaborator_token_free_text():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-collaborator-free-text-001",
        priority_user_token="test-priority-user-free-text-001",
        priority_attribute_token="test-priority-attribute-free-text-002",
        collaborator_token="quiero viajar gratis",
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "collaborator_token_looks_like_free_text" in result.risk_flags


def test_sync_rejects_self_sync_attempt():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-self-001",
        priority_user_token="test-same-token-sync-001",
        priority_attribute_token="test-priority-attribute-self-001",
        collaborator_token="test-same-token-sync-001",
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "self_sync_attempt" in result.risk_flags


def test_sync_rejects_replay_sync_event_id():
    ledger = SyncSecurityLedger()

    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-replay-001",
        priority_user_token="test-priority-user-replay-001",
        priority_attribute_token="test-priority-attribute-replay-001",
        collaborator_token="test-collaborator-replay-001",
    )

    first_result = simulate_solidary_sync_security(
        request=request,
        ledger=ledger,
    )

    second_result = simulate_solidary_sync_security(
        request=request,
        ledger=ledger,
    )

    assert first_result.status == SyncStatus.ACCEPTED
    assert first_result.accepted_demo_sync is True
    assert first_result.solidary_point_demo == 1

    assert second_result.status == SyncStatus.REJECTED
    assert second_result.accepted_demo_sync is False
    assert second_result.solidary_point_demo == 0
    assert "replay_sync_event_id" in second_result.risk_flags


def test_sync_rejects_expired_sync_window():
    issued_at = datetime.now(timezone.utc) - timedelta(minutes=10)

    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-expired-001",
        priority_user_token="test-priority-user-expired-001",
        priority_attribute_token="test-priority-attribute-expired-001",
        collaborator_token="test-collaborator-expired-001",
        issued_at_utc=issued_at,
        ttl_minutes=1,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "expired_sync_window" in result.risk_flags


def test_sync_rejects_need_not_previously_accredited():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-need-not-accredited-001",
        priority_user_token="test-priority-user-not-accredited-001",
        priority_attribute_token="test-priority-attribute-not-accredited-001",
        collaborator_token="test-collaborator-not-accredited-001",
        previously_accredited_need=False,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "need_not_previously_accredited" in result.risk_flags


def test_sync_rejects_no_voluntary_seat_yield():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-no-voluntary-yield-001",
        priority_user_token="test-priority-user-no-yield-001",
        priority_attribute_token="test-priority-attribute-no-yield-001",
        collaborator_token="test-collaborator-no-yield-001",
        voluntary_seat_yield=False,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "no_voluntary_seat_yield" in result.risk_flags


def test_sync_rejects_legal_priority_seat():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-legal-priority-seat-001",
        priority_user_token="test-priority-user-legal-seat-001",
        priority_attribute_token="test-priority-attribute-legal-seat-001",
        collaborator_token="test-collaborator-legal-seat-001",
        seat_type=SeatType.LEGAL_PRIORITY,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "legal_priority_seat_not_eligible" in result.risk_flags


def test_sync_rejects_collaborator_unilateral_claim():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-unilateral-claim-001",
        priority_user_token="test-priority-user-unilateral-001",
        priority_attribute_token="test-priority-attribute-unilateral-001",
        collaborator_token="test-collaborator-unilateral-001",
        collaborator_claims_reward=True,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "collaborator_unilateral_claim" in result.risk_flags
    assert "colaborador no puede" in result.reason.lower()


def test_sync_rejects_without_priority_user_confirmation():
    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-no-user-confirmation-001",
        priority_user_token="test-priority-user-no-confirmation-001",
        priority_attribute_token="test-priority-attribute-no-confirmation-001",
        collaborator_token="test-collaborator-no-confirmation-001",
        priority_user_confirms_sync=False,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "priority_user_confirmation_required" in result.risk_flags
    assert "sin confirmación voluntaria" in result.reason.lower()


def test_sync_rejects_different_transport_context():
    actual_context = create_demo_transport_sync_context(
        country="Argentina",
        network_demo_id="test-network-context",
        route_demo_id="test-route-context",
        vehicle_demo_id="test-vehicle-context-001",
        trip_demo_id="test-trip-context",
        time_window_demo_id="test-window-context",
    )

    expected_context = create_demo_transport_sync_context(
        country="Argentina",
        network_demo_id="test-network-context",
        route_demo_id="test-route-context",
        vehicle_demo_id="test-vehicle-context-999",
        trip_demo_id="test-trip-context",
        time_window_demo_id="test-window-context",
    )

    request = create_demo_sync_request(
        sync_event_demo_id="test-sync-different-context-001",
        priority_user_token="test-priority-user-context-001",
        priority_attribute_token="test-priority-attribute-context-001",
        collaborator_token="test-collaborator-context-001",
        actual_context=actual_context,
        expected_context=expected_context,
    )

    result = simulate_solidary_sync_security(request)

    assert result.status == SyncStatus.REJECTED
    assert result.accepted_demo_sync is False
    assert result.solidary_point_demo == 0
    assert "different_transport_context" in result.risk_flags


def test_sync_needs_review_when_priority_user_trip_limit_exceeded():
    ledger = SyncSecurityLedger()

    context = create_demo_transport_sync_context(
        network_demo_id="test-network-priority-limit",
        route_demo_id="test-route-priority-limit",
        vehicle_demo_id="test-vehicle-priority-limit",
        trip_demo_id="test-trip-priority-limit",
        time_window_demo_id="test-window-priority-limit",
    )

    first_request = create_demo_sync_request(
        sync_event_demo_id="test-sync-priority-limit-001",
        priority_user_token="test-priority-user-limit-001",
        priority_attribute_token="test-priority-attribute-limit-001",
        collaborator_token="test-collaborator-limit-001",
        actual_context=context,
        expected_context=context,
    )

    second_request = create_demo_sync_request(
        sync_event_demo_id="test-sync-priority-limit-002",
        priority_user_token="test-priority-user-limit-001",
        priority_attribute_token="test-priority-attribute-limit-001",
        collaborator_token="test-collaborator-limit-002",
        actual_context=context,
        expected_context=context,
    )

    first_result = simulate_solidary_sync_security(
        request=first_request,
        ledger=ledger,
    )

    second_result = simulate_solidary_sync_security(
        request=second_request,
        ledger=ledger,
    )

    assert first_result.status == SyncStatus.ACCEPTED
    assert first_result.accepted_demo_sync is True
    assert first_result.solidary_point_demo == 1

    assert second_result.status == SyncStatus.NEEDS_REVIEW
    assert second_result.accepted_demo_sync is False
    assert second_result.solidary_point_demo == 0
    assert "priority_user_trip_sync_limit_exceeded" in second_result.risk_flags


def test_sync_needs_review_when_collaborator_trip_limit_exceeded():
    ledger = SyncSecurityLedger()

    context = create_demo_transport_sync_context(
        network_demo_id="test-network-collaborator-limit",
        route_demo_id="test-route-collaborator-limit",
        vehicle_demo_id="test-vehicle-collaborator-limit",
        trip_demo_id="test-trip-collaborator-limit",
        time_window_demo_id="test-window-collaborator-limit",
    )

    first_request = create_demo_sync_request(
        sync_event_demo_id="test-sync-collaborator-limit-001",
        priority_user_token="test-priority-user-collab-limit-001",
        priority_attribute_token="test-priority-attribute-collab-limit-001",
        collaborator_token="test-collaborator-limit-same",
        actual_context=context,
        expected_context=context,
    )

    second_request = create_demo_sync_request(
        sync_event_demo_id="test-sync-collaborator-limit-002",
        priority_user_token="test-priority-user-collab-limit-002",
        priority_attribute_token="test-priority-attribute-collab-limit-002",
        collaborator_token="test-collaborator-limit-same",
        actual_context=context,
        expected_context=context,
    )

    third_request = create_demo_sync_request(
        sync_event_demo_id="test-sync-collaborator-limit-003",
        priority_user_token="test-priority-user-collab-limit-003",
        priority_attribute_token="test-priority-attribute-collab-limit-003",
        collaborator_token="test-collaborator-limit-same",
        actual_context=context,
        expected_context=context,
    )

    first_result = simulate_solidary_sync_security(
        request=first_request,
        ledger=ledger,
    )

    second_result = simulate_solidary_sync_security(
        request=second_request,
        ledger=ledger,
    )

    third_result = simulate_solidary_sync_security(
        request=third_request,
        ledger=ledger,
    )

    assert first_result.status == SyncStatus.ACCEPTED
    assert first_result.accepted_demo_sync is True
    assert first_result.solidary_point_demo == 1

    assert second_result.status == SyncStatus.ACCEPTED
    assert second_result.accepted_demo_sync is True
    assert second_result.solidary_point_demo == 1

    assert third_result.status == SyncStatus.NEEDS_REVIEW
    assert third_result.accepted_demo_sync is False
    assert third_result.solidary_point_demo == 0
    assert "collaborator_trip_sync_limit_exceeded" in third_result.risk_flags


def test_assert_no_prohibited_fields_rejects_dni():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "sync_event_demo_id": "test-sync-sensitive-dni",
            }
        )

    assert "dni" in str(error.value).lower()


def test_assert_no_prohibited_fields_rejects_medical_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "diagnostico": "dato no permitido",
                "cud": "dato no permitido",
            }
        )

    message = str(error.value).lower()

    assert "diagnostico" in message
    assert "cud" in message


def test_create_demo_sync_request_rejects_empty_sync_event_id():
    with pytest.raises(ValueError):
        create_demo_sync_request(
            sync_event_demo_id="",
            priority_user_token="test-priority-user-empty-event",
            priority_attribute_token="test-priority-attribute-empty-event",
            collaborator_token="test-collaborator-empty-event",
        )


def test_create_demo_sync_request_rejects_empty_priority_user_token():
    with pytest.raises(ValueError):
        create_demo_sync_request(
            sync_event_demo_id="test-sync-empty-priority-user",
            priority_user_token="",
            priority_attribute_token="test-priority-attribute-empty-priority-user",
            collaborator_token="test-collaborator-empty-priority-user",
        )


def test_create_demo_sync_request_rejects_empty_priority_attribute_token():
    with pytest.raises(ValueError):
        create_demo_sync_request(
            sync_event_demo_id="test-sync-empty-priority-attribute",
            priority_user_token="test-priority-user-empty-priority-attribute",
            priority_attribute_token="",
            collaborator_token="test-collaborator-empty-priority-attribute",
        )


def test_create_demo_sync_request_rejects_empty_collaborator_token():
    with pytest.raises(ValueError):
        create_demo_sync_request(
            sync_event_demo_id="test-sync-empty-collaborator",
            priority_user_token="test-priority-user-empty-collaborator",
            priority_attribute_token="test-priority-attribute-empty-collaborator",
            collaborator_token="",
        )

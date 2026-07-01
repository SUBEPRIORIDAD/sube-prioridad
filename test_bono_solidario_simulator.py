from datetime import datetime, timedelta, timezone

import pytest

from bono_solidario_simulator import (
    DemoRecognitionLedger,
    SeatType,
    SolidaryRecognitionStatus,
    assert_no_prohibited_fields,
    create_demo_solidary_event,
    create_demo_transport_context,
    run_demo,
    simulate_solidary_recognition,
)


def test_run_demo_accepts_valid_solidary_recognition():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Bono Solidario"
    assert result["demo_mode"] is True
    assert result["status"] == "accepted"
    assert result["solidary_point_demo"] == 1
    assert result["recognition_enabled_by_priority_user"] is True
    assert result["same_transport_context"] is True
    assert result["review_required"] is False
    assert result["risk_flags"] == []
    assert "Usuario SUBE Prioridad" in result["reason"] or "usuario SUBE Prioridad" in result["reason"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "El Bono Solidario queda en manos del usuario SUBE Prioridad." in result["warnings"]


def test_solidary_recognition_requires_priority_user_decision():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-user-decision",
        priority_user_token="test-priority-user-001",
        collaborator_token="test-collaborator-001",
        priority_user_decides_to_recognize=False,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert result.recognition_enabled_by_priority_user is False
    assert result.review_required is False
    assert "priority_user_did_not_recognize" in result.risk_flags


def test_solidary_recognition_requires_voluntary_seat_yield():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-no-voluntary-yield",
        priority_user_token="test-priority-user-002",
        collaborator_token="test-collaborator-002",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=False,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "no_voluntary_seat_yield" in result.risk_flags


def test_solidary_recognition_rejects_legal_priority_seat():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-legal-priority-seat",
        priority_user_token="test-priority-user-003",
        collaborator_token="test-collaborator-003",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.LEGAL_PRIORITY,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "legal_priority_seat_not_eligible" in result.risk_flags


def test_solidary_recognition_requires_same_transport_context():
    actual_context = create_demo_transport_context(
        country="Argentina",
        vehicle_demo_id="test-bus-001",
        route_demo_id="test-route-001",
        trip_demo_id="test-trip-001",
        time_window_demo_id="test-window-001",
    )

    expected_context = create_demo_transport_context(
        country="Argentina",
        vehicle_demo_id="test-bus-999",
        route_demo_id="test-route-001",
        trip_demo_id="test-trip-001",
        time_window_demo_id="test-window-001",
    )

    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-context",
        priority_user_token="test-priority-user-004",
        collaborator_token="test-collaborator-004",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=actual_context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=expected_context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert result.same_transport_context is False
    assert "different_transport_context" in result.risk_flags


def test_solidary_recognition_requires_argentina_context():
    context = create_demo_transport_context(country="Uruguay")
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-outside-argentina",
        priority_user_token="test-priority-user-005",
        collaborator_token="test-collaborator-005",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "outside_argentina_context" in result.risk_flags


def test_solidary_recognition_rejects_self_recognition():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-self-recognition",
        priority_user_token="test-same-token-001",
        collaborator_token="test-same-token-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "self_recognition_attempt" in result.risk_flags


def test_solidary_recognition_rejects_replay_event_id():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-replay",
        priority_user_token="test-priority-user-006",
        collaborator_token="test-collaborator-006",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    first_result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    second_result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert first_result.status == SolidaryRecognitionStatus.ACCEPTED
    assert first_result.solidary_point_demo == 1

    assert second_result.status == SolidaryRecognitionStatus.REJECTED
    assert second_result.solidary_point_demo == 0
    assert "replay_event_id" in second_result.risk_flags


def test_solidary_recognition_rejects_expired_event():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    issued_at = datetime.now(timezone.utc) - timedelta(minutes=10)

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-expired",
        priority_user_token="test-priority-user-007",
        collaborator_token="test-collaborator-007",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
        issued_at_utc=issued_at,
        ttl_minutes=1,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "expired_event" in result.risk_flags


def test_solidary_recognition_needs_review_when_priority_user_trip_limit_exceeded():
    context = create_demo_transport_context(
        vehicle_demo_id="test-bus-priority-limit",
        route_demo_id="test-route-priority-limit",
        trip_demo_id="test-trip-priority-limit",
        time_window_demo_id="test-window-priority-limit",
    )

    ledger = DemoRecognitionLedger()

    first_event = create_demo_solidary_event(
        event_demo_id="test-solidary-priority-limit-001",
        priority_user_token="test-priority-user-limit-001",
        collaborator_token="test-collaborator-limit-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    second_event = create_demo_solidary_event(
        event_demo_id="test-solidary-priority-limit-002",
        priority_user_token="test-priority-user-limit-001",
        collaborator_token="test-collaborator-limit-002",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    first_result = simulate_solidary_recognition(
        event=first_event,
        expected_context=context,
        ledger=ledger,
    )

    second_result = simulate_solidary_recognition(
        event=second_event,
        expected_context=context,
        ledger=ledger,
    )

    assert first_result.status == SolidaryRecognitionStatus.ACCEPTED
    assert first_result.solidary_point_demo == 1

    assert second_result.status == SolidaryRecognitionStatus.NEEDS_REVIEW
    assert second_result.solidary_point_demo == 0
    assert second_result.review_required is True
    assert "priority_user_trip_limit_exceeded" in second_result.risk_flags


def test_solidary_recognition_needs_review_when_collaborator_trip_limit_exceeded():
    context = create_demo_transport_context(
        vehicle_demo_id="test-bus-collaborator-limit",
        route_demo_id="test-route-collaborator-limit",
        trip_demo_id="test-trip-collaborator-limit",
        time_window_demo_id="test-window-collaborator-limit",
    )

    ledger = DemoRecognitionLedger()

    first_event = create_demo_solidary_event(
        event_demo_id="test-solidary-collaborator-limit-001",
        priority_user_token="test-priority-user-collab-limit-001",
        collaborator_token="test-collaborator-limit-same",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    second_event = create_demo_solidary_event(
        event_demo_id="test-solidary-collaborator-limit-002",
        priority_user_token="test-priority-user-collab-limit-002",
        collaborator_token="test-collaborator-limit-same",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    third_event = create_demo_solidary_event(
        event_demo_id="test-solidary-collaborator-limit-003",
        priority_user_token="test-priority-user-collab-limit-003",
        collaborator_token="test-collaborator-limit-same",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    first_result = simulate_solidary_recognition(
        event=first_event,
        expected_context=context,
        ledger=ledger,
    )

    second_result = simulate_solidary_recognition(
        event=second_event,
        expected_context=context,
        ledger=ledger,
    )

    third_result = simulate_solidary_recognition(
        event=third_event,
        expected_context=context,
        ledger=ledger,
    )

    assert first_result.status == SolidaryRecognitionStatus.ACCEPTED
    assert first_result.solidary_point_demo == 1

    assert second_result.status == SolidaryRecognitionStatus.ACCEPTED
    assert second_result.solidary_point_demo == 1

    assert third_result.status == SolidaryRecognitionStatus.NEEDS_REVIEW
    assert third_result.solidary_point_demo == 0
    assert third_result.review_required is True
    assert "collaborator_trip_limit_exceeded" in third_result.risk_flags


def test_solidary_recognition_rejects_priority_user_token_free_text():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-priority-free-text",
        priority_user_token="quiero viajar gratis",
        collaborator_token="test-collaborator-008",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "priority_user_token_looks_like_free_text" in result.risk_flags


def test_solidary_recognition_rejects_collaborator_token_free_text():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="test-solidary-event-collaborator-free-text",
        priority_user_token="test-priority-user-008",
        collaborator_token="quiero viajar gratis",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "collaborator_token_looks_like_free_text" in result.risk_flags


def test_assert_no_prohibited_fields_rejects_sensitive_payload():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "token": "demo-token",
            }
        )

    assert "dni" in str(error.value).lower()


def test_assert_no_prohibited_fields_rejects_medical_payload():
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


def test_create_demo_solidary_event_rejects_empty_event_demo_id():
    with pytest.raises(ValueError):
        create_demo_solidary_event(
            event_demo_id="",
            priority_user_token="test-priority-user-empty-event",
            collaborator_token="test-collaborator-empty-event",
            priority_user_decides_to_recognize=True,
        )


def test_create_demo_solidary_event_rejects_empty_priority_user_token():
    with pytest.raises(ValueError):
        create_demo_solidary_event(
            event_demo_id="test-solidary-empty-priority-user",
            priority_user_token="",
            collaborator_token="test-collaborator-empty-priority-user",
            priority_user_decides_to_recognize=True,
        )


def test_create_demo_solidary_event_rejects_empty_collaborator_token():
    with pytest.raises(ValueError):
        create_demo_solidary_event(
            event_demo_id="test-solidary-empty-collaborator",
            priority_user_token="test-priority-user-empty-collaborator",
            collaborator_token="",
            priority_user_decides_to_recognize=True,
        )

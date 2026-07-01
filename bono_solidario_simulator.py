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
    assert "usuario SUBE Prioridad" in result["reason"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "El Bono Solidario queda en manos del usuario SUBE Prioridad." in result["warnings"]


def test_solidary_recognition_requires_priority_user_decision():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-user-decision",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
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
    assert result.review_required is False
    assert result.recognition_enabled_by_priority_user is False
    assert "priority_user_did_not_recognize" in result.risk_flags
    assert "no decidió reconocer" in result.reason.lower()
    assert "no es automático" in result.reason.lower()


def test_solidary_recognition_requires_voluntary_seat_yield():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-no-voluntary-yield",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
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
    assert "no se registra una cesión voluntaria" in result.reason.lower()


def test_solidary_recognition_rejects_legal_priority_seat():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-legal-seat",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
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
    assert "asientos prioritarios legales" in result.reason.lower()
    assert "asientos de uso general" in result.reason.lower()


def test_solidary_recognition_requires_same_transport_context():
    actual_context = create_demo_transport_context(
        country="Argentina",
        vehicle_demo_id="demo-bus-001",
        route_demo_id="demo-route-001",
        trip_demo_id="demo-trip-001",
        time_window_demo_id="demo-window-001",
    )

    different_context = create_demo_transport_context(
        country="Argentina",
        vehicle_demo_id="demo-bus-999",
        route_demo_id="demo-route-001",
        trip_demo_id="demo-trip-001",
        time_window_demo_id="demo-window-001",
    )

    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-different-context",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=actual_context,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=different_context,
        ledger=ledger,
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert result.same_transport_context is False
    assert "different_transport_context" in result.risk_flags
    assert "no se verifica el mismo contexto" in result.reason.lower()


def test_solidary_recognition_requires_argentina_context():
    context = create_demo_transport_context(country="Uruguay")
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-outside-argentina",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
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
    assert "argentina" in result.reason.lower()


def test_solidary_recognition_rejects_self_recognition():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-self-recognition",
        priority_user_token="demo-same-token-001",
        collaborator_token="demo-same-token-001",
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
    assert "no pueden ser el mismo token" in result.reason.lower()


def test_solidary_recognition_rejects_replay_event_id():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-replay",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
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
    assert "ya fue utilizado" in second_result.reason.lower()


def test_solidary_recognition_rejects_expired_event():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    issued_at = datetime.now(timezone.utc) - timedelta(minutes=20)

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-expired",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
        issued_at_utc=issued_at,
        ttl_minutes=5,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=context,
        ledger=ledger,
        now_utc=datetime.now(timezone.utc),
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "expired_event" in result.risk_flags
    assert "expiró" in result.reason.lower()


def test_solidary_recognition_needs_review_when_priority_user_trip_limit_exceeded():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    first_event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-priority-limit-001",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    second_event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-priority-limit-002",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-002",
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
    assert "ya emitió un reconocimiento" in second_result.reason.lower()


def test_solidary_recognition_needs_review_when_collaborator_trip_limit_exceeded():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    first_event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-collaborator-limit-001",
        priority_user_token="demo-priority-user-001",
        collaborator_token="demo-collaborator-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    second_event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-collaborator-limit-002",
        priority_user_token="demo-priority-user-002",
        collaborator_token="demo-collaborator-001",
        priority_user_decides_to_recognize=True,
        seat_type=SeatType.GENERAL_USE,
        voluntary_seat_yield=True,
        transport_context=context,
    )

    third_event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-collaborator-limit-003",
        priority_user_token="demo-priority-user-003",
        collaborator_token="demo-collaborator-001",
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
    assert second_result.status == SolidaryRecognitionStatus.ACCEPTED

    assert third_result.status == SolidaryRecognitionStatus.NEEDS_REVIEW
    assert third_result.solidary_point_demo == 0
    assert third_result.review_required is True
    assert "collaborator_trip_limit_exceeded" in third_result.risk_flags
    assert "múltiples reconocimientos" in third_result.reason.lower()


def test_solidary_recognition_rejects_priority_user_token_that_looks_like_free_text():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-priority-free-text",
        priority_user_token="quiero bono solidario",
        collaborator_token="demo-collaborator-001",
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
    assert "texto libre" in result.reason.lower()


def test_solidary_recognition_rejects_collaborator_token_that_looks_like_free_text():
    context = create_demo_transport_context()
    ledger = DemoRecognitionLedger()

    event = create_demo_solidary_event(
        event_demo_id="demo-solidary-event-collaborator-free-text",
        priority_user_token="demo-priority-user-001",
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
    assert "texto libre" in result.reason.lower()


def test_solidary_recognition_rejects_sensitive_payload_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "vehicle_demo_id": "demo-bus-001",
            }
        )

    assert "dni" in str(error.value).lower()


def test_solidary_recognition_rejects_medical_payload_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "diagnostico": "dato no permitido",
                "route_demo_id": "demo-route-001",
            }
        )

    assert "diagnostico" in str(error.value).lower()


def test_create_demo_solidary_event_rejects_empty_event_demo_id():
    with pytest.raises(ValueError) as error:
        create_demo_solidary_event(
            event_demo_id="",
            priority_user_token="demo-priority-user-001",
            collaborator_token="demo-collaborator-001",
            priority_user_decides_to_recognize=True,
        )

    assert "evento" in str(error.value).lower()


def test_create_demo_solidary_event_rejects_empty_priority_user_token():
    with pytest.raises(ValueError) as error:
        create_demo_solidary_event(
            event_demo_id="demo-solidary-event-empty-priority",
            priority_user_token="",
            collaborator_token="demo-collaborator-001",
            priority_user_decides_to_recognize=True,
        )

    assert "usuario sube prioridad" in str(error.value).lower()


def test_create_demo_solidary_event_rejects_empty_collaborator_token():
    with pytest.raises(ValueError) as error:
        create_demo_solidary_event(
            event_demo_id="demo-solidary-event-empty-collaborator",
            priority_user_token="demo-priority-user-001",
            collaborator_token="",
            priority_user_decides_to_recognize=True,
        )

    assert "colaborador" in str(error.value).lower()

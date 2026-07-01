import pytest

from bono_solidario_simulator import (
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
    assert "usuario SUBE Prioridad" in result["reason"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "El Bono Solidario queda en manos del usuario SUBE Prioridad." in result["warnings"]


def test_solidary_recognition_requires_priority_user_decision():
    context = create_demo_transport_context()

    event = create_demo_solidary_event(
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
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert result.recognition_enabled_by_priority_user is False
    assert "no decidió reconocer" in result.reason.lower()
    assert "no es automático" in result.reason.lower()


def test_solidary_recognition_requires_voluntary_seat_yield():
    context = create_demo_transport_context()

    event = create_demo_solidary_event(
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
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "no se registra una cesión voluntaria" in result.reason.lower()


def test_solidary_recognition_rejects_legal_priority_seat():
    context = create_demo_transport_context()

    event = create_demo_solidary_event(
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
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
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

    event = create_demo_solidary_event(
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
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert result.same_transport_context is False
    assert "no se verifica el mismo contexto" in result.reason.lower()


def test_solidary_recognition_requires_argentina_context():
    context = create_demo_transport_context(country="Uruguay")

    event = create_demo_solidary_event(
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
    )

    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert result.solidary_point_demo == 0
    assert "argentina" in result.reason.lower()


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


def test_create_demo_solidary_event_rejects_empty_priority_user_token():
    with pytest.raises(ValueError) as error:
        create_demo_solidary_event(
            priority_user_token="",
            collaborator_token="demo-collaborator-001",
            priority_user_decides_to_recognize=True,
        )

    assert "usuario sube prioridad" in str(error.value).lower()


def test_create_demo_solidary_event_rejects_empty_collaborator_token():
    with pytest.raises(ValueError) as error:
        create_demo_solidary_event(
            priority_user_token="demo-priority-user-001",
            collaborator_token="",
            priority_user_decides_to_recognize=True,
        )

    assert "colaborador" in str(error.value).lower()

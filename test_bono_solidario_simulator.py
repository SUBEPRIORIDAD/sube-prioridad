"""
SUBE Prioridad — Tests unitarios para el Simulador de Bono Solidario.
Valida el comportamiento analítico del backend despersonalizado.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timezone
from bono_solidario_simulator import (
    create_demo_solidary_event,
    simulate_solidary_recognition,
    SeatType,
    SolidaryRecognitionStatus,
    SolidaryRejectionReason,
    DemoRecognitionLedger
)

def test_successful_solidary_recognition():
    """Valida la aprobación de un evento colaborativo legítimo en asiento general."""
    event = create_demo_solidary_event(
        event_demo_id="test-event-ok",
        priority_user_token="user-priority-ok",
        collaborator_token="user-collaborator-ok",
        voluntary_seat_yield=True,
        priority_user_confirms_seat_yield=True,
        same_transport_context=True,
        seat_type=SeatType.GENERAL_USE
    )
    result = simulate_solidary_recognition(event)
    assert result.accepted is True
    assert result.status == SolidaryRecognitionStatus.ACCEPTED
    assert result.rejection_reason == SolidaryRejectionReason.NONE
    assert len(result.risk_flags) == 0

def test_rejection_no_voluntary_yield():
    """Valida el rechazo si la cesión del asiento de uso general no fue voluntaria."""
    event = create_demo_solidary_event(
        event_demo_id="test-event-no-voluntary",
        priority_user_token="user-priority-ok",
        collaborator_token="user-collaborator-ok",
        voluntary_seat_yield=False,
        priority_user_confirms_seat_yield=True,
        same_transport_context=True,
        seat_type=SeatType.GENERAL_USE
    )
    result = simulate_solidary_recognition(event)
    assert result.accepted is False
    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert "no_voluntary_seat_yield" in result.risk_flags
    assert result.rejection_reason == SolidaryRejectionReason.NO_VOLUNTARY_SEAT_YIELD

def test_rejection_same_user_attempt():
    """Valida el bloqueo antifraude si el token del colaborador coincide con el prioritario."""
    event = create_demo_solidary_event(
        event_demo_id="test-event-same-user",
        priority_user_token="fraud-token-01",
        collaborator_token="fraud-token-01",
        voluntary_seat_yield=True,
        priority_user_confirms_seat_yield=True,
        same_transport_context=True,
        seat_type=SeatType.GENERAL_USE
    )
    result = simulate_solidary_recognition(event)
    assert result.accepted is False
    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert "same_user_not_allowed" in result.risk_flags
    assert result.rejection_reason == SolidaryRejectionReason.SAME_USER_NOT_ALLOWED

def test_rejection_legal_priority_seat():
    """Valida que no se premie la ocupación de asientos legalmente prioritarios."""
    event = create_demo_solidary_event(
        event_demo_id="test-event-legal-seat",
        priority_user_token="user-priority-ok",
        collaborator_token="user-collaborator-ok",
        voluntary_seat_yield=True,
        priority_user_confirms_seat_yield=True,
        same_transport_context=True,
        seat_type=SeatType.LEGAL_PRIORITY
    )
    result = simulate_solidary_recognition(event)
    assert result.accepted is False
    assert result.status == SolidaryRecognitionStatus.REJECTED
    assert "legal_priority_seat_not_rewardable" in result.risk_flags
    assert result.rejection_reason == SolidaryRejectionReason.LEGAL_PRIORITY_SEAT_NOT_REWARDABLE

def test_prohibited_fields_exception():
    """Valida que el escudo de privacidad arroje excepción ante campos de identidad civil."""
    with pytest.raises(ValueError) as exc_info:
        create_demo_solidary_event(**{"dni": "12345678", "priority_user_token": "ok"})
    assert "campos prohibidos para SUBE Prioridad" in str(exc_info.value)

def test_demo_recognition_ledger_operations():
    """Valida el correcto funcionamiento del libro de registros en memoria exigido en el DIP."""
    ledger = DemoRecognitionLedger()
    assert ledger.size == 0
    
    event = create_demo_solidary_event(
        event_demo_id="ledger-test-01",
        priority_user_token="priority-token",
        collaborator_token="collaborator-token"
    )
    
    registration_success = ledger.register_interaction(event)
    assert registration_success is True
    assert ledger.size == 1
    
    ledger.clear()
    assert ledger.size == 0

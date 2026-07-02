"""
SUBE Prioridad — Tests para AntifraudValidator hardware behavior.
"""

from __future__ import annotations
import pytest
from red_sube_trip_window_matcher import create_demo_validation_signal

def test_validator_hardware_behavior():
    """Valida que las señales conceptuales operen de forma correcta."""
    signal = create_demo_validation_signal(
        validation_event_demo_id="sig-val-01",
        participant_token="token-val-ok"
    )
    assert signal.validation_event_demo_id == "sig-val-01"
    assert signal.participant_token == "token-val-ok"

def test_validator_prohibited_fields_exception():
    """Valida el escudo protector de datos sensibles en el validador."""
    with pytest.raises(ValueError):
        create_demo_validation_signal(validation_event_demo_id="ev-01", **{"dni": "12345678"})

"""
SUBE Prioridad — Tests unitarios para preferencias y alertas pasivas.
"""

from __future__ import annotations
from solidary_bonus_frontend_flow import create_demo_priority_account_frontend_context

def test_passive_alert_preferences_active():
    """Valida la persistencia conceptual del atributo activo de prioridad."""
    context = create_demo_priority_account_frontend_context(
        priority_attribute_active=True,
        solidary_bonus_frontend_enabled=True
    )
    assert context.priority_attribute_active is True
    assert context.solidary_bonus_frontend_enabled is True

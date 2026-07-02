"""
SUBE Prioridad — Tests unitarios para las políticas antifraude del ecosistema.
Valida la mitigación de riesgos de acumulación asíncrona en el transporte.
"""

from __future__ import annotations
from red_sube_discount_policy import (
    create_demo_red_sube_policy,
    create_demo_solidary_bonus_eligibility_context,
    create_demo_red_sube_trip_combination,
    calculate_solidary_bonus_discount_quote,
    DiscountPolicyStatus
)

def test_antifraud_legitimate_quote_flow():
    """Valida que una solicitud libre de riesgos sea aprobada económicamente."""
    policy = create_demo_red_sube_policy()
    context = create_demo_solidary_bonus_eligibility_context(bonus_already_used=False)
    trip = create_demo_red_sube_trip_combination(combination_number_demo=2, validation_paid=True)
    
    result = calculate_solidary_bonus_discount_quote(policy, context, trip)
    assert result.status == DiscountPolicyStatus.ELIGIBLE
    assert result.applied_to_next_trip is True

def test_antifraud_double_spend_rejection():
    """Valida el bloqueo inmediato si el bono ya fue consumido por el colaborador."""
    policy = create_demo_red_sube_policy()
    context = create_demo_solidary_bonus_eligibility_context(bonus_already_used=True)
    trip = create_demo_red_sube_trip_combination(combination_number_demo=2, validation_paid=True)
    
    result = calculate_solidary_bonus_discount_quote(policy, context, trip)
    assert result.status == DiscountPolicyStatus.REJECTED
    assert "solidary_bonus_already_used" in result.risk_flags

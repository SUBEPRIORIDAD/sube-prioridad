"""
SUBE Prioridad — Tests para el Frontend Conceptual de Bono Solidario.
"""

from __future__ import annotations
from solidary_bonus_frontend_flow import (
    create_demo_solidary_bonus_frontend_request,
    evaluate_solidary_bonus_frontend_request,
    FrontendDecisionStatus
)

def test_frontend_flow_ready_for_handoff():
    """Valida que un flujo de confirmación legítimo quede listo para seguridad."""
    request = create_demo_solidary_bonus_frontend_request(
        priority_user_confirms_send=True,
        priority_user_understands_demo_scope=True
    )
    result = evaluate_solidary_bonus_frontend_request(request)
    assert result.frontend_ready is True
    assert result.status == FrontendDecisionStatus.READY_FOR_SECURITY_FLOW
    assert result.handoff_to_security_flow_enabled is True
    assert "Frontend conceptual y demostrativo." in result.warnings

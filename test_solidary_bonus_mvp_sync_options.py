"""
SUBE Prioridad — Tests unitarios para las opciones MVP de sincronización.
Valida los canales de acoplamiento de hardware de forma despersonalizada.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timezone
from solidary_bonus_mvp_sync_options import (
    create_demo_mobile_to_mobile_request,
    evaluate_mvp_solidary_sync_option,
    MvpSyncStatus,
    MvpSyncOption
)

def test_successful_mobile_to_mobile_sync_option():
    """Valida la aprobación analítica del canal de sincronización móvil a móvil."""
    request = create_demo_mobile_to_mobile_request(
        mvp_sync_event_demo_id="test-sync-m2m-ok",
        priority_user_token="priority-token-api",
        collaborator_token="collaborator-token-api"
    )
    result = evaluate_mvp_solidary_sync_option(request)
    assert result.status in {MvpSyncStatus.READY, MvpSyncStatus.READY_WITH_AUDIT}
    assert result.blocks_solidary_bonus_flow is False
    assert result.selected_option == MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT.value
def test_sync_option_prohibited_fields_exception():
    """Valida que el escudo de privacidad bloquee inyecciones de DNI en las opciones MVP."""
    from solidary_bonus_mvp_sync_options import assert_no_prohibited_fields
    with pytest.raises(ValueError):
        assert_no_prohibited_fields({"dni": "33444555", "nombre": "Andres"})

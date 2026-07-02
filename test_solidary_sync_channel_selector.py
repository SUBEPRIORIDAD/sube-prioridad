"""
SUBE Prioridad — Tests unitarios para el Selector de Canales de Sincronización.
Valida la omnicanalidad inclusiva para pasajeros sin celular.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timezone
from solidary_sync_channel_selector import (
    create_demo_solidary_sync_channel_request,
    create_demo_no_mobile_validator_based_request,
    create_demo_station_no_mobile_deferred_request,
    evaluate_solidary_sync_channel,
    SyncChannelStatus,
    SyncChannel,
    WindowKind
)

def test_sync_channel_reinforced_mobile_path():
    """Valida la asignación del canal optimizado cuando hay dispositivos disponibles."""
    request = create_demo_solidary_sync_channel_request(
        sync_channel_event_demo_id="test-chan-reinforced",
        priority_user_token="user-priority-api",
        collaborator_user_token="user-collaborator-api"
    )
    result = evaluate_solidary_sync_channel(request)
    assert result.status == SyncChannelStatus.READY_REINFORCED
    assert result.selected_channel == SyncChannel.PRIORITY_MOBILE_NFC_CARD_TAP
    assert result.opens_bonus_evaluation_window is True

def test_sync_channel_no_mobile_validator_window():
    """Valida que la falta de celular no bloquee y abra una ventana física a bordo del bus."""
    request = create_demo_no_mobile_validator_based_request()
    result = evaluate_solidary_sync_channel(request)
    assert result.status == SyncChannelStatus.READY_WITHOUT_MOBILE
    assert result.selected_channel == SyncChannel.VALIDATOR_CONTEXT_WINDOW
    assert result.window_kind == WindowKind.IN_VEHICLE_SHORT_WINDOW
    assert result.opens_bonus_evaluation_window is True
def test_sync_channel_station_deferred_window():
    """Valida la ventana extendida en molinetes ferroviarios/subtes con cuenta diferida."""
    request = create_demo_station_no_mobile_deferred_request()
    result = evaluate_solidary_sync_channel(request)
    assert result.status == SyncChannelStatus.READY_DEFERRED_CONFIRMATION
    assert result.selected_channel == SyncChannel.ACCOUNT_DEFERRED_CONFIRMATION
    assert result.window_kind == WindowKind.STATION_EXTENDED_WINDOW
    assert result.requires_audit_review is True

def test_sync_channel_prohibited_fields_exception():
    """Valida el escudo de privacidad duro frente a inyecciones de DNI en el selector."""
    from solidary_sync_channel_selector import assert_no_prohibited_fields
    with pytest.raises(ValueError):
        assert_no_prohibited_fields({"dni": "44555666", "sync_channel_event_demo_id": "err"})

"""
SUBE Prioridad — Tests unitarios para la Pasarela de Enlace (Casual Gateway).
Valida las comunicaciones de las validadoras y los mensajes a la pantalla del chofer.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timezone
from casual_gateway import (
    GatewayHardwareContext,
    CasualGatewaySignalPayload,
    process_casual_gateway_signal,
    GatewayCommsStatus,
    DriverDisplayMessage
)

def test_gateway_online_rail_network_approval():
    """Valida el procesamiento exitoso en línea para molinetes de subte o tren."""
    now = datetime.now(timezone.utc)
    hardware = GatewayHardwareContext(
        network_demo_id="red-sube-rail", route_demo_id="linea-mitre",
        vehicle_demo_id=None, station_demo_id="estacion-san-isidro",
        turnstile_demo_id="turnstile-si-01", is_rail_network=True
    )
    payload = CasualGatewaySignalPayload(
        signal_demo_id="test-sig-rail-ok", priority_user_token_demo="p-token-123",
        collaborator_token_demo="c-token-456", validation_timestamp_utc=now,
        voluntary_seat_yield_declared=True
    )
    result = process_casual_gateway_signal(payload, hardware, is_wan_online=True)
    assert result.signal_processed is True
    assert result.comms_status == GatewayCommsStatus.ONLINE_SYNC
    assert result.driver_display_message == DriverDisplayMessage.ACCESS_GRANTED
def test_gateway_degraded_offline_failsafe():
    """Valida la conmutación a modo Fail-Safe y buffer local ante la caída de red WAN."""
    now = datetime.now(timezone.utc)
    hardware = GatewayHardwareContext(
        network_demo_id="red-sube-bus", route_demo_id="linea-60",
        vehicle_demo_id="unidad-12", station_demo_id=None,
        turnstile_demo_id=None, is_rail_network=False
    )
    payload = CasualGatewaySignalPayload(
        signal_demo_id="test-sig-bus-degraded", priority_user_token_demo="p-token-123",
        collaborator_token_demo="c-token-456", validation_timestamp_utc=now,
        voluntary_seat_yield_declared=True
    )
    result = process_casual_gateway_signal(payload, hardware, is_wan_online=False)
    assert result.comms_status == GatewayCommsStatus.DEGRADED_EDGE_BUFFER
    assert result.payload_buffered_locally is True
    assert result.driver_display_message == DriverDisplayMessage.CONNECTION_DEGRADED

def test_gateway_prohibited_fields_exception():
    """Valida que el escudo de privacidad intercepte inyecciones de DNI en la pasarela."""
    from casual_gateway import assert_no_prohibited_fields
    with pytest.raises(ValueError):
        assert_no_prohibited_fields({"dni": "33444555", "signal_demo_id": "ok"})

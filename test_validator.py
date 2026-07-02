import pytest
from datetime import datetime, timezone
from validator import AntifraudValidator, EventoValidacion, HardwareTargetKind

def test_hardware_behavior_colectivo_edge():
    """Valida el procesamiento local de borde y apertura de ventana para Colectivos."""
    validador = AntifraudValidator()
    evento = EventoValidacion(
        tarjeta_id="sube_hash_1",
        linea = "141",
        unidad = "int_44",
        timestamp = datetime.now(timezone.utc),
        hardware_origen = HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
    )
    
    resultado = validador.validar_evento(evento)
    assert resultado.permitido is True
    assert resultado.hardware_action == "execute_immediate_edge_habitaculo_alert"
    assert resultado.open_solidary_window is True
    assert resultado.latency_estimation_ms < 300

def test_hardware_behavior_subte_molinete():
    """Valida el enrutamiento silencioso asíncrono y omisión de ventana en Molinetes."""
    validador = AntifraudValidator()
    evento = EventoValidacion(
        tarjeta_id="sube_hash_2",
        linea = "Subte_D",
        unidad = "molinete_fixed_02",
        timestamp = datetime.now(timezone.utc),
        hardware_origen = HardwareTargetKind.SUBTE_MOLINETE
    )
    
    resultado = validador.validar_evento(evento)
    assert resultado.permitido is True
    assert resultado.hardware_action == "route_async_signal_to_platform_displays"
    assert resultado.open_solidary_window is False

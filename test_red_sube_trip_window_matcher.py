"""
SUBE Prioridad — Tests para el Matcher de Ventana Temporal Red SUBE.
Valida la ingeniería de transporte real sobre colectivos y trazas ferroviarias.
"""

from __future__ import annotations
import pytest
from datetime import datetime, timedelta, timezone
from red_sube_trip_window_matcher import (
    create_demo_trip_window_match_policy,
    create_demo_validation_signal,
    evaluate_trip_window_match,
    assert_no_prohibited_fields,
    TransportMode,
    ValidationPointType,
    MatchStatus,
    MatchStrength
)

def test_railway_line_shared_route_match():
    """Valida estaciones diferentes de una misma línea ferroviaria sincronizada."""
    timestamp = datetime.now(timezone.utc)
    
    p_signal = create_demo_validation_signal(
        validation_event_demo_id="p-rail-si",
        participant_role="priority_user",
        participant_token="token-prioritario-ferroviario",
        transport_mode=TransportMode.TRAIN,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="linea-mitre-ramal-tigre",
        station_demo_id="estacion-san-isidro",
        validation_timestamp_utc=timestamp
    )
    
    c_signal = create_demo_validation_signal(
        validation_event_demo_id="c-rail-mtz",
        participant_role="collaborator",
        participant_token="token-colaborador-ferroviario",
        transport_mode=TransportMode.TRAIN,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="linea-mitre-ramal-tigre",
        station_demo_id="estacion-martinez",
        validation_timestamp_utc=timestamp + timedelta(minutes=5)
    )
    
    policy = create_demo_trip_window_match_policy()
    result = evaluate_trip_window_match(p_signal, c_signal, policy)
    
    assert result.matched is True
    assert result.status == MatchStatus.MATCHED

def test_bus_different_route_rejection():
    """Valida que colectivos de líneas distintas sean rechazados por el matcher."""
    timestamp = datetime.now(timezone.utc)
    
    p_signal = create_demo_validation_signal(
        validation_event_demo_id="p-bus-60",
        participant_role="priority_user",
        transport_mode=TransportMode.BUS,
        route_demo_id="linea-60-ramal-pampa",
        validation_timestamp_utc=timestamp
    )
    
    c_signal = create_demo_validation_signal(
        validation_event_demo_id="c-bus-152",
        participant_role="collaborator",
        transport_mode=TransportMode.BUS,
        route_demo_id="linea-152-ramal-olivos",
        validation_timestamp_utc=timestamp + timedelta(minutes=2)
    )
    
    result = evaluate_trip_window_match(p_signal, c_signal)
    assert result.matched is False

def test_prohibited_fields_in_matcher():
    """Valida el escudo de privacidad duro frente a inyecciones de DNI en payloads."""
    with pytest.raises(ValueError):
        assert_no_prohibited_fields({"dni": "44555666", "certificado_medico": "inyeccion"})

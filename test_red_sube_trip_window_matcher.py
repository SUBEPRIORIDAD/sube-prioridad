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
    assert result.same_route is True
    assert result.match_strength == MatchStrength.SAME_ROUTE_TIME_WINDOW_WEAK
def test_tren_de_la_costa_restrictive_breaker():
    """Valida el breaker de hardware de 3 minutos para el Tren de la Costa."""
    timestamp = datetime.now(timezone.utc)
    
    p_signal = create_demo_validation_signal(
        validation_event_demo_id="p-tdlc",
        participant_role="priority_user",
        participant_token="token-p-tdlc",
        transport_mode=TransportMode.TREN_DE_LA_COSTA,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="traza-tren-de-la-costa",
        validation_timestamp_utc=timestamp
    )
    
    c_signal = create_demo_validation_signal(
        validation_event_demo_id="c-tdlc",
        participant_role="collaborator",
        participant_token="token-c-tdlc",
        transport_mode=TransportMode.TREN_DE_LA_COSTA,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="traza-tren-de-la-costa",
        validation_timestamp_utc=timestamp + timedelta(minutes=8)
    )
    
    policy = create_demo_trip_window_match_policy(in_vehicle_proximity_minutes_demo=10)
    result = evaluate_trip_window_match(p_signal, c_signal, policy)
    
    assert result.matched is False
    assert result.status == MatchStatus.REJECTED
    assert "effective_sync_window_expired" in result.risk_flags

def test_bus_different_route_rejection():
    """Valida que colectivos de líneas distintas sean rechazados."""
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
    assert "no_shared_transport_context" in result.risk_flags

def test_prohibited_fields_in_matcher():
    """Valida el escudo de privacidad duro frente a inyecciones de DNI."""
    with pytest.raises(ValueError):
        create_demo_validation_signal(validation_event_demo_id="ev-01", participant_token="ok", **{"dni": "44555666"})

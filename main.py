"""
SUBE Prioridad — API de Producción Saneada.
Expone los endpoints del simulador de Bono Solidario, Matcher y Políticas de Descuento.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

import bono_solidario_simulator as simulator
import red_sube_trip_window_matcher as matcher
import red_sube_discount_policy as policy
import solidary_bonus_frontend_flow as frontend

app = FastAPI(
    title="SUBE Prioridad API",
    version="0.3.0",
    description="Endpoints conceptuales para la prueba piloto de co-presencia cívica."
)

class SolidaryEventPayload(BaseModel):
    event_demo_id: str = Field(default="demo-event-001")
    priority_user_token: str = Field(default="demo-priority-user-001")
    collaborator_token: str = Field(default="demo-collaborator-user-001")
    voluntary_seat_yield: bool = True
    priority_user_confirms_seat_yield: bool = True
    same_transport_context: bool = True
    seat_type: str = Field(default="general_use")

class ValidationSignalPayload(BaseModel):
    validation_event_demo_id: str
    participant_role: str
    participant_token: str
    payment_method_demo_token: str
    validation_paid: bool
    country: str = "Argentina"
    network_demo_id: str
    transport_mode: str
    validation_point_type: str
    route_demo_id: Optional[str] = None
    vehicle_demo_id: Optional[str] = None
    station_demo_id: Optional[str] = None
    turnstile_demo_id: Optional[str] = None
    platform_demo_id: Optional[str] = None
    trip_demo_id: Optional[str] = None

class MatchEvaluationRequest(BaseModel):
    priority_signal: ValidationSignalPayload
    collaborator_signal: ValidationSignalPayload

@app.post("/api/v1/solidary-recognition", status_code=status.HTTP_200_OK)
def process_solidary_recognition(payload: SolidaryEventPayload) -> Dict[str, Any]:
    try:
        seat_type_enum = simulator.SeatType(payload.seat_type)
    except ValueError:
        raise HTTPException(status_code=422, detail="Tipo de asiento no válido.")
        
    payload_dict = payload.dict()
    try:
        simulator.assert_no_prohibited_fields(payload_dict)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
        
    event = simulator.create_demo_solidary_event(
        event_demo_id=payload.event_demo_id,
        priority_user_token=payload.priority_user_token,
        collaborator_token=payload.collaborator_token,
        voluntary_seat_yield=payload.voluntary_seat_yield,
        priority_user_confirms_seat_yield=payload.priority_user_confirms_seat_yield,
        same_transport_context=payload.same_transport_context,
        seat_type=seat_type_enum
    )
    result = simulator.simulate_solidary_recognition(event)
    if not result.accepted:
        raise HTTPException(status_code=422, detail=f"Rechazado: {result.rejection_reason.value}")
    return simulator.result_to_dict(result)
@app.post("/api/v1/trip-window-match", status_code=status.HTTP_200_OK)
def evaluate_hardware_match(payload: MatchEvaluationRequest) -> Dict[str, Any]:
    try:
        matcher.assert_no_prohibited_fields(payload.priority_signal.dict())
        matcher.assert_no_prohibited_fields(payload.collaborator_signal.dict())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
        
    p_sig = matcher.create_demo_validation_signal(
        validation_event_demo_id=payload.priority_signal.validation_event_demo_id,
        participant_role=matcher.ParticipantRole(payload.priority_signal.participant_role),
        participant_token=payload.priority_signal.participant_token,
        payment_method_demo_token=payload.priority_signal.payment_method_demo_token,
        validation_paid=payload.priority_signal.validation_paid,
        country=payload.priority_signal.country,
        network_demo_id=payload.priority_signal.network_demo_id,
        transport_mode=matcher.TransportMode(payload.priority_signal.transport_mode),
        validation_point_type=matcher.ValidationPointType(payload.priority_signal.validation_point_type),
        route_demo_id=payload.priority_signal.route_demo_id,
        vehicle_demo_id=payload.priority_signal.vehicle_demo_id,
        station_demo_id=payload.priority_signal.station_demo_id,
        turnstile_demo_id=payload.priority_signal.turnstile_demo_id,
        platform_demo_id=payload.priority_signal.platform_demo_id,
        trip_demo_id=payload.priority_signal.trip_demo_id
    )
    
    c_sig = matcher.create_demo_validation_signal(
        validation_event_demo_id=payload.collaborator_signal.validation_event_demo_id,
        participant_role=matcher.ParticipantRole(payload.collaborator_signal.participant_role),
        participant_token=payload.collaborator_signal.participant_token,
        payment_method_demo_token=payload.collaborator_signal.payment_method_demo_token,
        validation_paid=payload.collaborator_signal.validation_paid,
        country=payload.collaborator_signal.country,
        network_demo_id=payload.collaborator_signal.network_demo_id,
        transport_mode=matcher.TransportMode(payload.collaborator_signal.transport_mode),
        validation_point_type=matcher.ValidationPointType(payload.collaborator_signal.validation_point_type),
        route_demo_id=payload.collaborator_signal.route_demo_id,
        vehicle_demo_id=payload.collaborator_signal.vehicle_demo_id,
        station_demo_id=payload.collaborator_signal.station_demo_id,
        turnstile_demo_id=payload.collaborator_signal.turnstile_demo_id,
        platform_demo_id=payload.collaborator_signal.platform_demo_id,
        trip_demo_id=payload.collaborator_signal.trip_demo_id
    )
    
    result = matcher.evaluate_trip_window_match(p_sig, c_sig)
    if not result.matched:
        raise HTTPException(status_code=422, detail="Las señales de hardware no coinciden.")
    return matcher.result_to_dict(result)

@app.get("/api/v1/health-check")
def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "project": "SUBE Prioridad"
    }

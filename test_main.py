"""
SUBE Prioridad — Tests unitarios para la API principal (FastAPI).
Valida el comportamiento de los endpoints frente a payloads válidos y fraudes.
"""

from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_health_check():
    """Valida el endpoint base de estado operativo del servidor web."""
    response = client.get("/api/v1/health-check")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_api_successful_solidary_recognition():
    """Valida la aceptación HTTP 200 de un reconocimiento legítimo en asiento general."""
    payload = {
        "event_demo_id": "api-test-ok",
        "priority_user_token": "token-prioritario-api-ok",
        "collaborator_token": "token-colaborador-api-ok",
        "voluntary_seat_yield": True,
        "priority_user_confirms_seat_yield": True,
        "same_transport_context": True,
        "seat_type": "general_use"
    }
    response = client.post("/api/v1/solidary-recognition", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["matched"] is True

def test_api_rejection_legal_priority_seat():
    """Valida que la API devuelva un código de error 422 al intentar premiar un asiento de ley."""
    payload = {
        "event_demo_id": "api-test-legal-seat",
        "priority_user_token": "token-prioritario-api-ok",
        "collaborator_token": "token-colaborador-api-ok",
        "voluntary_seat_yield": True,
        "priority_user_confirms_seat_yield": True,
        "same_transport_context": True,
        "seat_type": "legal_priority"
    }
    response = client.post("/api/v1/solidary-recognition", json=payload)
    assert response.status_code == 422
    assert "Rechazado" in response.json()["detail"]
def test_api_rejection_sensitive_dni_field():
    """Valida el bloqueo inmediato HTTP 422 si el payload inyecta datos civiles prohibidos."""
    payload = {
        "event_demo_id": "api-test-fraud-dni",
        "priority_user_token": "token-ok",
        "collaborator_token": "token-ok",
        "dni": "33444555",
        "seat_type": "general_use"
    }
    response = client.post("/api/v1/solidary-recognition", json=payload)
    assert response.status_code == 422
    assert "campos prohibidos para SUBE Prioridad" in response.json()["detail"]

def test_api_hardware_match_evaluation():
    """Valida el endpoint de emparejamiento de señales sincronizadas de la Red SUBE."""
    payload = {
        "priority_signal": {
            "validation_event_demo_id": "sig-p-01",
            "participant_role": "priority_user",
            "participant_token": "p-token-api",
            "payment_method_demo_token": "p-card-api",
            "validation_paid": True,
            "country": "Argentina",
            "network_demo_id": "network-sube-api",
            "transport_mode": "bus",
            "validation_point_type": "vehicle_validator",
            "route_demo_id": "route-api-152",
            "vehicle_demo_id": "intern-12"
        },
        "collaborator_signal": {
            "validation_event_demo_id": "sig-c-01",
            "participant_role": "collaborator",
            "participant_token": "c-token-api",
            "payment_method_demo_token": "c-card-api",
            "validation_paid": True,
            "country": "Argentina",
            "network_demo_id": "network-sube-api",
            "transport_mode": "bus",
            "validation_point_type": "vehicle_validator",
            "route_demo_id": "route-api-152",
            "vehicle_demo_id": "intern-12"
        }
    }
    response = client.post("/api/v1/trip-window-match", json=payload)
    assert response.status_code == 200
    assert response.json()["matched"] is True

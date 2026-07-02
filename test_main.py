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
    """Valida la aceptación HTTP de un reconocimiento legítimo en asiento general."""
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

def test_api_rejection_legal_priority_seat():
    """Valida que la API devuelva un código de error al intentar premiar un asiento de ley."""
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

def test_api_rejection_sensitive_dni_field():
    """Valida el bloqueo inmediato si el payload inyecta datos civiles prohibidos."""
    payload = {
        "event_demo_id": "api-test-fraud-dni",
        "priority_user_token": "token-ok",
        "collaborator_token": "token-ok",
        "dni": "33444555",
        "seat_type": "general_use"
    }
    response = client.post("/api/v1/solidary-recognition", json=payload)
    assert response.status_code == 422

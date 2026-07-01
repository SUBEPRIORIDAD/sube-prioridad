from fastapi.testclient import TestClient

from main import APP_NAME, APP_VERSION, app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == APP_NAME
    assert data["version"] == APP_VERSION
    assert data["demo_mode"] is True
    assert data["status"] == "ok"

    guardrails_text = " ".join(data["guardrails"]).lower()

    assert "bono solidario" in guardrails_text
    assert "prioridad" in guardrails_text


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["project"] == APP_NAME
    assert data["version"] == APP_VERSION
    assert data["demo_mode"] is True
    assert "timestamp_utc" in data


def test_project_guardrails_endpoint():
    response = client.get("/project/guardrails")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == APP_NAME
    assert data["version"] == APP_VERSION
    assert data["demo_mode"] is True

    guardrails_text = " ".join(data["guardrails"]).lower()

    assert "sube prioridad" in guardrails_text
    assert "conceptual" in guardrails_text
    assert "implementación oficial" in guardrails_text or "implementacion oficial" in guardrails_text
    assert "sube real" in guardrails_text
    assert "validadoras reales" in guardrails_text
    assert "dni" in guardrails_text
    assert "nombre" in guardrails_text
    assert "diagnóstico" in guardrails_text or "diagnostico" in guardrails_text
    assert "cud" in guardrails_text
    assert "asientos prioritarios legales" in guardrails_text
    assert "chofer" in guardrails_text
    assert "bono solidario" in guardrails_text


def test_priority_verification_accepts_registered_demo_token():
    payload = {
        "token_prioridad": "demo-priority-attribute-001",
        "preferencia_asistencia": 3,
        "linea": "demo-linea-001",
        "unidad": "demo-unidad-001",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == APP_NAME
    assert data["version"] == APP_VERSION
    assert data["demo_mode"] is True
    assert data["status"] == "valid"
    assert data["prioridad_activa"] is True
    assert data["token_verificado"] is True
    assert data["preferencia_asistencia"] == 3

    warnings_text = " ".join(data["advertencias"]).lower()

    assert "sube" in warnings_text
    assert "bono solidario" in warnings_text


def test_priority_verification_rejects_bono_solidario_as_priority_token():
    payload = {
        "token_prioridad": "bono-solidario-tarifa-social-vigente",
        "preferencia_asistencia": 3,
        "linea": "demo-linea-001",
        "unidad": "demo-unidad-001",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "invalid"
    assert data["prioridad_activa"] is False
    assert data["token_verificado"] is False
    assert "bono solidario" in data["motivo"].lower()


def test_priority_verification_rejects_unknown_demo_token():
    payload = {
        "token_prioridad": "demo-priority-attribute-no-registrado",
        "preferencia_asistencia": 2,
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "invalid"
    assert data["prioridad_activa"] is False
    assert data["token_verificado"] is False


def test_priority_verification_rejects_magic_free_text():
    payload = {
        "token_prioridad": "quiero viajar gratis porque esta palabra activa el sistema",
        "preferencia_asistencia": 4,
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "invalid"
    assert data["prioridad_activa"] is False
    assert data["token_verificado"] is False


def test_priority_verification_rejects_sensitive_dni_field():
    payload = {
        "token_prioridad": "demo-priority-attribute-001",
        "preferencia_asistencia": 3,
        "dni": "12345678",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 422
    assert "dni" in response.text.lower()


def test_priority_verification_rejects_medical_diagnosis_field():
    payload = {
        "token_prioridad": "demo-priority-attribute-001",
        "preferencia_asistencia": 3,
        "diagnostico": "dato no permitido",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 422
    assert "diagnostico" in response.text.lower()


def test_bono_solidario_endpoint_accepts_valid_demo_event():
    payload = {
        "event_demo_id": "api-solidary-valid-stable-001",
        "priority_user_token": "api-priority-user-valid-stable-001",
        "collaborator_token": "api-collaborator-valid-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-valid-stable-001",
        "route_demo_id": "api-route-valid-stable-001",
        "trip_demo_id": "api-trip-valid-stable-001",
        "time_window_demo_id": "api-window-valid-stable-001",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Bono Solidario"
    assert data["demo_mode"] is True
    assert data["status"] == "accepted"
    assert data["solidary_point_demo"] == 1
    assert data["recognition_enabled_by_priority_user"] is True
    assert data["same_transport_context"] is True
    assert data["review_required"] is False
    assert data["risk_flags"] == []


def test_bono_solidario_endpoint_rejects_without_priority_user_decision():
    payload = {
        "event_demo_id": "api-solidary-no-user-decision-stable-001",
        "priority_user_token": "api-priority-user-no-decision-stable-001",
        "collaborator_token": "api-collaborator-no-decision-stable-001",
        "priority_user_decides_to_recognize": False,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-no-decision-stable-001",
        "route_demo_id": "api-route-no-decision-stable-001",
        "trip_demo_id": "api-trip-no-decision-stable-001",
        "time_window_demo_id": "api-window-no-decision-stable-001",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert data["recognition_enabled_by_priority_user"] is False
    assert "priority_user_did_not_recognize" in data["risk_flags"]


def test_bono_solidario_endpoint_rejects_legal_priority_seat():
    payload = {
        "event_demo_id": "api-solidary-legal-seat-stable-001",
        "priority_user_token": "api-priority-user-legal-seat-stable-001",
        "collaborator_token": "api-collaborator-legal-seat-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "legal_priority",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-legal-seat-stable-001",
        "route_demo_id": "api-route-legal-seat-stable-001",
        "trip_demo_id": "api-trip-legal-seat-stable-001",
        "time_window_demo_id": "api-window-legal-seat-stable-001",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert "legal_priority_seat_not_eligible" in data["risk_flags"]


def test_bono_solidario_endpoint_rejects_self_recognition():
    payload = {
        "event_demo_id": "api-solidary-self-recognition-stable-001",
        "priority_user_token": "api-same-token-stable-001",
        "collaborator_token": "api-same-token-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-self-stable-001",
        "route_demo_id": "api-route-self-stable-001",
        "trip_demo_id": "api-trip-self-stable-001",
        "time_window_demo_id": "api-window-self-stable-001",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert "self_recognition_attempt" in data["risk_flags"]


def test_bono_solidario_endpoint_rejects_replay_event():
    payload = {
        "event_demo_id": "api-solidary-replay-stable-001",
        "priority_user_token": "api-priority-user-replay-stable-001",
        "collaborator_token": "api-collaborator-replay-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-replay-stable-001",
        "route_demo_id": "api-route-replay-stable-001",
        "trip_demo_id": "api-trip-replay-stable-001",
        "time_window_demo_id": "api-window-replay-stable-001",
    }

    first_response = client.post("/api/v1/bono-solidario/simular", json=payload)
    second_response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_data = first_response.json()
    second_data = second_response.json()

    assert first_data["status"] == "accepted"
    assert first_data["solidary_point_demo"] == 1

    assert second_data["status"] == "rejected"
    assert second_data["solidary_point_demo"] == 0
    assert "replay_event_id" in second_data["risk_flags"]


def test_bono_solidario_endpoint_rejects_different_transport_context():
    payload = {
        "event_demo_id": "api-solidary-different-context-stable-001",
        "priority_user_token": "api-priority-user-context-stable-001",
        "collaborator_token": "api-collaborator-context-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-context-stable-001",
        "route_demo_id": "api-route-context-stable-001",
        "trip_demo_id": "api-trip-context-stable-001",
        "time_window_demo_id": "api-window-context-stable-001",
        "expected_vehicle_demo_id": "api-bus-context-stable-different",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert data["same_transport_context"] is False
    assert "different_transport_context" in data["risk_flags"]


def test_bono_solidario_endpoint_rejects_free_text_collaborator_token():
    payload = {
        "event_demo_id": "api-solidary-free-text-stable-001",
        "priority_user_token": "api-priority-user-free-text-stable-001",
        "collaborator_token": "quiero viajar gratis",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-free-text-stable-001",
        "route_demo_id": "api-route-free-text-stable-001",
        "trip_demo_id": "api-trip-free-text-stable-001",
        "time_window_demo_id": "api-window-free-text-stable-001",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert "collaborator_token_looks_like_free_text" in data["risk_flags"]


def test_bono_solidario_endpoint_requires_review_for_priority_user_trip_limit():
    first_payload = {
        "event_demo_id": "api-solidary-priority-limit-stable-001",
        "priority_user_token": "api-priority-user-limit-stable-001",
        "collaborator_token": "api-collaborator-limit-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-priority-limit-stable-001",
        "route_demo_id": "api-route-priority-limit-stable-001",
        "trip_demo_id": "api-trip-priority-limit-stable-001",
        "time_window_demo_id": "api-window-priority-limit-stable-001",
    }

    second_payload = {
        "event_demo_id": "api-solidary-priority-limit-stable-002",
        "priority_user_token": "api-priority-user-limit-stable-001",
        "collaborator_token": "api-collaborator-limit-stable-002",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-priority-limit-stable-001",
        "route_demo_id": "api-route-priority-limit-stable-001",
        "trip_demo_id": "api-trip-priority-limit-stable-001",
        "time_window_demo_id": "api-window-priority-limit-stable-001",
    }

    first_response = client.post("/api/v1/bono-solidario/simular", json=first_payload)
    second_response = client.post("/api/v1/bono-solidario/simular", json=second_payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_data = first_response.json()
    second_data = second_response.json()

    assert first_data["status"] == "accepted"
    assert first_data["solidary_point_demo"] == 1

    assert second_data["status"] == "needs_review"
    assert second_data["solidary_point_demo"] == 0
    assert second_data["review_required"] is True
    assert "priority_user_trip_limit_exceeded" in second_data["risk_flags"]


def test_bono_solidario_endpoint_rejects_sensitive_dni_field():
    payload = {
        "event_demo_id": "api-solidary-sensitive-dni-stable-001",
        "priority_user_token": "api-priority-user-sensitive-dni-stable-001",
        "collaborator_token": "api-collaborator-sensitive-dni-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "dni": "12345678",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 422
    assert "dni" in response.text.lower()


def test_bono_solidario_endpoint_rejects_sensitive_cud_field():
    payload = {
        "event_demo_id": "api-solidary-sensitive-cud-stable-001",
        "priority_user_token": "api-priority-user-sensitive-cud-stable-001",
        "collaborator_token": "api-collaborator-sensitive-cud-stable-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "cud": "dato no permitido",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 422
    assert "cud" in response.text.lower()

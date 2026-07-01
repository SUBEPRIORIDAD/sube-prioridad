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
    assert data["core"]["priority_verification"] == "/api/v1/prioridad/verificar"
    assert (
        data["core"]["bono_solidario_future_module"]
        == "/api/v1/bono-solidario/simular"
    )
    assert "Bono Solidario separado del token de prioridad." in data["guardrails"]


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
    assert "No integración real con SUBE." in data["guardrails"]
    assert "No procesa DNI." in data["guardrails"]
    assert "No procesa diagnóstico." in data["guardrails"]
    assert "No procesa CUD." in data["guardrails"]
    assert "No reemplaza los asientos prioritarios legales." in data["guardrails"]
    assert "No traslada cargas operativas al chofer." in data["guardrails"]
    assert "El Bono Solidario es un módulo futuro, opcional y separado." in data["guardrails"]
    assert "El Bono Solidario queda en manos del usuario SUBE Prioridad." in data["guardrails"]


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
    assert data["linea"] == "demo-linea-001"
    assert data["unidad"] == "demo-unidad-001"
    assert "Atributo técnico demostrativo verificado" in data["motivo"]
    assert "no revela diagnóstico" in data["motivo"]
    assert "Sin integración real con SUBE." in data["advertencias"]
    assert "Bono Solidario separado del token de prioridad." in data["advertencias"]


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
    assert "texto libre" in data["motivo"].lower()
    assert "bono solidario" in data["motivo"].lower()
    assert "tarifa social" in data["motivo"].lower()
    assert "atributo técnico demostrativo" in data["motivo"].lower()


def test_priority_verification_rejects_unknown_demo_token():
    payload = {
        "token_prioridad": "demo-priority-attribute-no-registrado",
        "preferencia_asistencia": 2,
        "linea": "demo-linea-001",
        "unidad": "demo-unidad-001",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "invalid"
    assert data["prioridad_activa"] is False
    assert data["token_verificado"] is False
    assert "no se registra" in data["motivo"].lower()
    assert "evita falsos positivos" in data["motivo"].lower()


def test_priority_verification_rejects_magic_free_text():
    payload = {
        "token_prioridad": "quiero viajar gratis porque esta palabra activa el sistema",
        "preferencia_asistencia": 4,
        "linea": "demo-linea-001",
        "unidad": "demo-unidad-001",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "invalid"
    assert data["prioridad_activa"] is False
    assert data["token_verificado"] is False
    assert "palabras mágicas" in data["motivo"].lower()
    assert "atributo técnico demostrativo" in data["motivo"].lower()


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
        "event_demo_id": "api-solidary-valid-001",
        "priority_user_token": "api-priority-user-valid-001",
        "collaborator_token": "api-collaborator-valid-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-001",
        "route_demo_id": "api-route-001",
        "trip_demo_id": "api-trip-001",
        "time_window_demo_id": "api-window-001",
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
    assert "usuario SUBE Prioridad" in data["reason"]
    assert "asiento de uso general" in data["reason"]
    assert "Sin integración real con Red SUBE." in data["warnings"]
    assert "El Bono Solidario queda en manos del usuario SUBE Prioridad." in data["warnings"]


def test_bono_solidario_endpoint_rejects_without_priority_user_decision():
    payload = {
        "event_demo_id": "api-solidary-no-user-decision-001",
        "priority_user_token": "api-priority-user-no-decision-001",
        "collaborator_token": "api-collaborator-no-decision-001",
        "priority_user_decides_to_recognize": False,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-002",
        "route_demo_id": "api-route-002",
        "trip_demo_id": "api-trip-002",
        "time_window_demo_id": "api-window-002",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert data["recognition_enabled_by_priority_user"] is False
    assert data["review_required"] is False
    assert "priority_user_did_not_recognize" in data["risk_flags"]
    assert "no decidió reconocer" in data["reason"].lower()
    assert "no es automático" in data["reason"].lower()


def test_bono_solidario_endpoint_rejects_legal_priority_seat():
    payload = {
        "event_demo_id": "api-solidary-legal-seat-001",
        "priority_user_token": "api-priority-user-legal-seat-001",
        "collaborator_token": "api-collaborator-legal-seat-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "legal_priority",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-003",
        "route_demo_id": "api-route-003",
        "trip_demo_id": "api-trip-003",
        "time_window_demo_id": "api-window-003",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert "legal_priority_seat_not_eligible" in data["risk_flags"]
    assert "asientos prioritarios legales" in data["reason"].lower()
    assert "asientos de uso general" in data["reason"].lower()


def test_bono_solidario_endpoint_rejects_self_recognition():
    payload = {
        "event_demo_id": "api-solidary-self-recognition-001",
        "priority_user_token": "api-same-token-001",
        "collaborator_token": "api-same-token-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-004",
        "route_demo_id": "api-route-004",
        "trip_demo_id": "api-trip-004",
        "time_window_demo_id": "api-window-004",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert "self_recognition_attempt" in data["risk_flags"]
    assert "no pueden ser el mismo token" in data["reason"].lower()


def test_bono_solidario_endpoint_rejects_replay_event():
    payload = {
        "event_demo_id": "api-solidary-replay-001",
        "priority_user_token": "api-priority-user-replay-001",
        "collaborator_token": "api-collaborator-replay-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-005",
        "route_demo_id": "api-route-005",
        "trip_demo_id": "api-trip-005",
        "time_window_demo_id": "api-window-005",
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
    assert "ya fue utilizado" in second_data["reason"].lower()


def test_bono_solidario_endpoint_rejects_different_transport_context():
    payload = {
        "event_demo_id": "api-solidary-different-context-001",
        "priority_user_token": "api-priority-user-context-001",
        "collaborator_token": "api-collaborator-context-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-006",
        "route_demo_id": "api-route-006",
        "trip_demo_id": "api-trip-006",
        "time_window_demo_id": "api-window-006",
        "expected_vehicle_demo_id": "api-bus-different",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert data["same_transport_context"] is False
    assert "different_transport_context" in data["risk_flags"]
    assert "no se verifica el mismo contexto" in data["reason"].lower()


def test_bono_solidario_endpoint_rejects_free_text_collaborator_token():
    payload = {
        "event_demo_id": "api-solidary-free-text-001",
        "priority_user_token": "api-priority-user-free-text-001",
        "collaborator_token": "quiero viajar gratis",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-007",
        "route_demo_id": "api-route-007",
        "trip_demo_id": "api-trip-007",
        "time_window_demo_id": "api-window-007",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "rejected"
    assert data["solidary_point_demo"] == 0
    assert "collaborator_token_looks_like_free_text" in data["risk_flags"]
    assert "texto libre" in data["reason"].lower()


def test_bono_solidario_endpoint_requires_review_for_priority_user_trip_limit():
    first_payload = {
        "event_demo_id": "api-solidary-priority-limit-001",
        "priority_user_token": "api-priority-user-limit-001",
        "collaborator_token": "api-collaborator-limit-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-008",
        "route_demo_id": "api-route-008",
        "trip_demo_id": "api-trip-008",
        "time_window_demo_id": "api-window-008",
    }

    second_payload = {
        "event_demo_id": "api-solidary-priority-limit-002",
        "priority_user_token": "api-priority-user-limit-001",
        "collaborator_token": "api-collaborator-limit-002",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "country": "Argentina",
        "vehicle_demo_id": "api-bus-008",
        "route_demo_id": "api-route-008",
        "trip_demo_id": "api-trip-008",
        "time_window_demo_id": "api-window-008",
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
    assert "ya emitió un reconocimiento" in second_data["reason"].lower()


def test_bono_solidario_endpoint_rejects_sensitive_dni_field():
    payload = {
        "event_demo_id": "api-solidary-sensitive-dni-001",
        "priority_user_token": "api-priority-user-sensitive-dni-001",
        "collaborator_token": "api-collaborator-sensitive-dni-001",
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
        "event_demo_id": "api-solidary-sensitive-cud-001",
        "priority_user_token": "api-priority-user-sensitive-cud-001",
        "collaborator_token": "api-collaborator-sensitive-cud-001",
        "priority_user_decides_to_recognize": True,
        "seat_type": "general_use",
        "voluntary_seat_yield": True,
        "cud": "dato no permitido",
    }

    response = client.post("/api/v1/bono-solidario/simular", json=payload)

    assert response.status_code == 422
    assert "cud" in response.text.lower()

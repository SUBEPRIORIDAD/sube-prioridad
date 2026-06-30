from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["proyecto"] == "SUBE Prioridad"
    assert data["estado"] == "MVP conceptual, técnico y demostrativo"
    assert data["implementacion_productiva"] is False
    assert data["integracion_real_con_organismos"] is False
    assert data["modificacion_sistema_sube"] is False
    assert data["procesa_datos_medicos"] is False
    assert data["procesa_datos_identificatorios"] is False
    assert data["documentacion"] == "/docs"
    assert data["health"] == "/health"
    assert data["guardrails"] == "/project/guardrails"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "sube-prioridad-api"
    assert data["environment"] == "mvp-conceptual"
    assert data["datos_sensibles_procesados"] is False
    assert data["integracion_real_con_organismos"] is False
    assert data["implementacion_productiva"] is False


def test_project_guardrails_endpoint():
    response = client.get("/project/guardrails")

    assert response.status_code == 200

    data = response.json()

    assert data["naturaleza"] == "MVP conceptual, técnico y demostrativo"
    assert data["implementacion_productiva"] is False
    assert data["integracion_real_con_organismos"] is False
    assert data["modificacion_sistema_sube"] is False
    assert data["procesamiento_datos_medicos"] is False
    assert data["procesamiento_datos_identificatorios"] is False

    assert "privacidad por diseño" in data["principios"]
    assert "minimización de datos" in data["principios"]
    assert "no exposición de diagnósticos" in data["principios"]
    assert "atributo técnico de prioridad" in data["principios"]
    assert "no sustitución de asientos prioritarios" in data["principios"]
    assert "no imposición de nuevas cargas al chofer" in data["principios"]

    assert "DNI" in data["datos_no_procesados_en_core"]
    assert "diagnóstico médico" in data["datos_no_procesados_en_core"]
    assert "historia clínica" in data["datos_no_procesados_en_core"]
    assert "certificado médico en texto plano" in data["datos_no_procesados_en_core"]

    assert data["integraciones"]["sube"] == "no integrada en este MVP"
    assert data["integraciones"]["mi_argentina"] == "no integrada en este MVP"
    assert data["integraciones"]["nacion_servicios"] == "no integrada en este MVP"


def test_verificar_prioridad_activa():
    payload = {
        "token_prioridad": "demo-prioridad-activa",
        "linea": "60",
        "unidad": "1234",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["prioridad_activa"] is True
    assert data["perfil_ux"] == "preventiva"
    assert data["fecha_caducidad"] is not None
    assert data["motivo"] == "Atributo técnico de prioridad activo en entorno MVP conceptual."
    assert data["entorno"] == "mvp-conceptual"
    assert data["datos_sensibles_procesados"] is False
    assert data["integracion_real_con_organismos"] is False


def test_verificar_prioridad_inactiva():
    payload = {
        "token_prioridad": "demo-prioridad-inactiva",
        "linea": "60",
        "unidad": "1234",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["prioridad_activa"] is False
    assert data["perfil_ux"] == "sin_prioridad_operativa"
    assert data["fecha_caducidad"] is None
    assert data["motivo"] == "No se registra atributo técnico activo en la simulación del MVP."
    assert data["entorno"] == "mvp-conceptual"
    assert data["datos_sensibles_procesados"] is False
    assert data["integracion_real_con_organismos"] is False


def test_verificar_prioridad_sin_datos_sensibles():
    payload = {
        "token_prioridad": "token-tecnico-demo",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "diagnostico" not in data
    assert "diagnóstico" not in data
    assert "dni" not in data
    assert "nombre" not in data
    assert "apellido" not in data
    assert "historia_clinica" not in data
    assert "certificado_medico" not in data

    assert data["datos_sensibles_procesados"] is False
    assert data["integracion_real_con_organismos"] is False


def test_verificar_prioridad_request_invalido_sin_token():
    payload = {
        "linea": "60",
        "unidad": "1234",
    }

    response = client.post("/api/v1/prioridad/verificar", json=payload)

    assert response.status_code == 422

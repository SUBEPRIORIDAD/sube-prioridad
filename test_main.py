from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "timestamp" in body


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()

    assert body["servicio"] == "SUBE Prioridad API"
    assert body["estado"] == "operativo"
    assert body["version"] == "0.2.0"
    assert "MVP" in body["naturaleza"]
    assert "asistencia preventiva" in body["objetivo"]


def test_project_guardrails_endpoint():
    response = client.get("/project/guardrails")

    assert response.status_code == 200
    body = response.json()

    assert body["datos_sensibles_en_core"] is False
    assert body["diagnostico_medico_en_core"] is False
    assert body["modifica_regimen_asientos_prioritarios"] is False
    assert body["impone_cargas_al_chofer"] is False
    assert body["genera_sanciones_a_pasajeros"] is False
    assert body["modifica_recaudacion_sube"] is False
    assert body["bono_solidario_es_core_inicial"] is False
    assert body["bono_solidario_es_evolucion_futura"] is True
    assert body["integraciones_externas_reales"] is False


def test_verificar_prioridad_endpoint_aprueba_token_valido():
    token = "a" * 64

    response = client.post(
        "/api/v1/prioridad/verificar",
        json={
            "token_tramite_hash": token,
            "firma_digital_medico": "firma-demo",
            "entidad_emisora": "entidad-demo",
            "perfil_asistencia_preferido": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["atributo_prioridad_activo"] is True
    assert body["perfil_alertas_ux"] == 2
    assert "fecha_caducidad" in body
    assert "MVP" in body["motivo"]
    assert body["entorno"] == "simulado_mvp"
    assert body["datos_sensibles_procesados"] is False
    assert body["integracion_real_con_organismos"] is False


def test_verificar_prioridad_endpoint_respeta_preferencia_visible():
    token = "b" * 64

    response = client.post(
        "/api/v1/prioridad/verificar",
        json={
            "token_tramite_hash": token,
            "perfil_asistencia_preferido": 3,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["perfil_alertas_ux"] == 3


def test_verificar_prioridad_endpoint_rechaza_token_corto():
    response = client.post(
        "/api/v1/prioridad/verificar",
        json={
            "token_tramite_hash": "abc",
        },
    )

    assert response.status_code == 422


def test_verificar_prioridad_endpoint_rechaza_token_no_alfanumerico():
    token = "a" * 63 + "-"

    response = client.post(
        "/api/v1/prioridad/verificar",
        json={
            "token_tramite_hash": token,
        },
    )

    assert response.status_code == 400


def test_verificar_prioridad_endpoint_rechaza_perfil_fuera_de_rango():
    token = "c" * 64

    response = client.post(
        "/api/v1/prioridad/verificar",
        json={
            "token_tramite_hash": token,
            "perfil_asistencia_preferido": 9,
        },
    )

    assert response.status_code == 422

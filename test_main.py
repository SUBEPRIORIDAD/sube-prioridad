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


def test_verificar_prioridad_endpoint_aprueba_token_valido():
    token = "a" * 64

    response = client.post(
        "/api/v1/prioridad/verificar",
        json={
            "token_tramite_hash": token,
            "firma_digital_medico": "firma-demo",
            "entidad_emisora": "entidad-demo",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["atributo_prioridad_activo"] is True
    assert body["perfil_alertas_ux"] == 2
    assert "fecha_caducidad" in body
    assert "MVP" in body["motivo"]


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
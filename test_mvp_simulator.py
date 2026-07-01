import pytest

from mvp_simulator import (
    AssistancePreference,
    ValidationStatus,
    assert_no_prohibited_fields,
    create_demo_priority_attribute,
    run_demo,
    simulate_priority_validation,
)


def test_run_demo_returns_valid_result():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["demo_mode"] is True
    assert result["status"] == "valid"
    assert result["assistance_preference"] == "preventiva"
    assert "diagnóstico" in result["privacy_notice"]
    assert "Sin integración real con SUBE." in result["warnings"]


def test_priority_validation_accepts_demo_token():
    attribute = create_demo_priority_attribute(
        token="demo-priority-attribute-999",
        assistance_preference=AssistancePreference.DISCRETA,
    )

    result = simulate_priority_validation(attribute)

    assert result.status == ValidationStatus.VALID
    assert result.assistance_preference == AssistancePreference.DISCRETA
    assert "discreta" in result.alert_message.lower()


def test_priority_validation_rejects_invalid_token():
    attribute = create_demo_priority_attribute(
        token="invalid-token",
        assistance_preference=AssistancePreference.PREVENTIVA,
    )

    result = simulate_priority_validation(attribute)

    assert result.status == ValidationStatus.INVALID
    assert result.assistance_preference is None
    assert "inválido" in result.alert_message.lower()


def test_rejects_sensitive_context_fields():
    attribute = create_demo_priority_attribute(
        token="demo-priority-attribute-123",
        assistance_preference=AssistancePreference.VISIBLE,
    )

    with pytest.raises(ValueError) as error:
        simulate_priority_validation(
            attribute,
            context={
                "dni": "12345678",
                "vehicle_demo_id": "demo-bus-001",
            },
        )

    assert "dni" in str(error.value).lower()


def test_rejects_medical_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "diagnostico": "dato no permitido",
                "route_demo_id": "demo-route-001",
            }
        )

    assert "diagnostico" in str(error.value).lower()

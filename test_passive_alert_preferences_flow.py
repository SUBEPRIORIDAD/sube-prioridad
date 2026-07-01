import pytest

from passive_alert_preferences_flow import (
    AlertChannel,
    AlertDecisionStatus,
    AssistanceMode,
    assert_no_prohibited_fields,
    create_demo_alert_context,
    create_demo_passive_alert_request,
    create_demo_user_alert_preference,
    evaluate_passive_alert_request,
    result_to_dict,
    run_demo,
)


def test_run_demo_accepts_passive_alert_flow():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Preferencias y Alertas Pasivas"
    assert result["demo_mode"] is True
    assert result["status"] == "allowed"
    assert result["selected_channel"] == "passive_signal"
    assert result["assistance_mode"] == "passive"
    assert result["alert_enabled"] is True
    assert result["exposure_level"] == "minimal_passive"
    assert result["blocked_reasons"] == []
    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]
    assert "no diagnostica" in result["driver_burden"].lower()
    assert "no impone obligaciones" in result["passenger_burden"].lower()
    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin diagnóstico médico." in result["warnings"]
    assert "Sin CUD real." in result["warnings"]
    assert "Sin carga operativa para el chofer." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-to-dict-001",
        priority_attribute_token="test-priority-attribute-to-dict-001",
    )

    result = evaluate_passive_alert_request(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Preferencias y Alertas Pasivas"
    assert data["demo_mode"] is True
    assert isinstance(data["warnings"], list)
    assert isinstance(data["blocked_reasons"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_silent_mode_blocks_external_alert():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.SILENT,
        allow_passive_signal=True,
        allow_discreet_signal=True,
        allow_visible_generic_signal=True,
        allow_luminous_generic_signal=True,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-silent-001",
        priority_attribute_token="test-priority-attribute-silent-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.ALLOWED
    assert result.selected_channel == AlertChannel.NONE
    assert result.alert_enabled is False
    assert result.exposure_level == "none"
    assert "modo silencioso" in result.message.lower()


def test_passive_mode_uses_passive_signal_when_allowed():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.PASSIVE,
        allow_passive_signal=True,
        allow_discreet_signal=False,
        allow_visible_generic_signal=False,
        allow_luminous_generic_signal=False,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-passive-001",
        priority_attribute_token="test-priority-attribute-passive-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.ALLOWED
    assert result.selected_channel == AlertChannel.PASSIVE_SIGNAL
    assert result.alert_enabled is True
    assert result.exposure_level == "minimal_passive"


def test_passive_mode_falls_back_to_internal_record_when_passive_not_allowed():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.PASSIVE,
        allow_passive_signal=False,
        allow_discreet_signal=False,
        allow_visible_generic_signal=False,
        allow_luminous_generic_signal=False,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-passive-fallback-001",
        priority_attribute_token="test-priority-attribute-passive-fallback-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.DEGRADED
    assert result.selected_channel == AlertChannel.INTERNAL_RECORD
    assert result.alert_enabled is True
    assert result.exposure_level == "internal_only"
    assert "registro interno" in result.message.lower()


def test_discreet_mode_uses_discreet_signal_when_allowed():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.DISCREET,
        allow_passive_signal=True,
        allow_discreet_signal=True,
        allow_visible_generic_signal=False,
        allow_luminous_generic_signal=False,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-discreet-001",
        priority_attribute_token="test-priority-attribute-discreet-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.ALLOWED
    assert result.selected_channel == AlertChannel.DISCREET_SIGNAL
    assert result.alert_enabled is True
    assert result.exposure_level == "low_discreet"
    assert "sin diagnóstico" in result.message.lower()


def test_visible_generic_mode_requires_user_permission():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.VISIBLE_GENERIC,
        allow_passive_signal=True,
        allow_discreet_signal=True,
        allow_visible_generic_signal=False,
        allow_luminous_generic_signal=False,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-visible-no-permission-001",
        priority_attribute_token="test-priority-attribute-visible-no-permission-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.DEGRADED
    assert result.selected_channel in {
        AlertChannel.DISCREET_SIGNAL,
        AlertChannel.PASSIVE_SIGNAL,
        AlertChannel.INTERNAL_RECORD,
    }
    assert result.selected_channel != AlertChannel.GENERIC_VISUAL_SIGNAL


def test_visible_generic_mode_uses_visible_signal_when_allowed():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.VISIBLE_GENERIC,
        allow_passive_signal=True,
        allow_discreet_signal=True,
        allow_visible_generic_signal=True,
        allow_luminous_generic_signal=False,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-visible-allowed-001",
        priority_attribute_token="test-priority-attribute-visible-allowed-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.ALLOWED
    assert result.selected_channel == AlertChannel.GENERIC_VISUAL_SIGNAL
    assert result.alert_enabled is True
    assert result.exposure_level == "generic_visible"
    assert "no se informa el motivo" in result.message.lower()


def test_luminous_generic_mode_requires_user_permission():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.LUMINOUS_GENERIC,
        allow_passive_signal=True,
        allow_discreet_signal=True,
        allow_visible_generic_signal=False,
        allow_luminous_generic_signal=False,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-luminous-no-permission-001",
        priority_attribute_token="test-priority-attribute-luminous-no-permission-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.DEGRADED
    assert result.selected_channel != AlertChannel.GENERIC_LUMINOUS_SIGNAL
    assert result.alert_enabled is True


def test_luminous_generic_mode_uses_luminous_signal_when_allowed():
    preference = create_demo_user_alert_preference(
        assistance_mode=AssistanceMode.LUMINOUS_GENERIC,
        allow_passive_signal=True,
        allow_discreet_signal=True,
        allow_visible_generic_signal=True,
        allow_luminous_generic_signal=True,
        allow_internal_record=True,
    )

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-luminous-allowed-001",
        priority_attribute_token="test-priority-attribute-luminous-allowed-001",
        preference=preference,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.ALLOWED
    assert result.selected_channel == AlertChannel.GENERIC_LUMINOUS_SIGNAL
    assert result.alert_enabled is True
    assert result.exposure_level == "generic_luminous"
    assert "sin datos personales" in result.message.lower()


def test_alert_blocks_outside_argentina_context():
    context = create_demo_alert_context(country="Uruguay")

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-outside-argentina-001",
        priority_attribute_token="test-priority-attribute-outside-argentina-001",
        context=context,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.BLOCKED
    assert result.selected_channel == AlertChannel.NONE
    assert result.alert_enabled is False
    assert "outside_argentina_context" in result.blocked_reasons


def test_alert_blocks_need_not_previously_accredited():
    context = create_demo_alert_context(previously_accredited_need=False)

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-need-not-accredited-001",
        priority_attribute_token="test-priority-attribute-need-not-accredited-001",
        context=context,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.BLOCKED
    assert result.selected_channel == AlertChannel.NONE
    assert result.alert_enabled is False
    assert "need_not_previously_accredited" in result.blocked_reasons


def test_alert_blocks_inactive_priority_attribute():
    context = create_demo_alert_context(priority_attribute_active=False)

    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-inactive-priority-001",
        priority_attribute_token="test-priority-attribute-inactive-001",
        context=context,
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.BLOCKED
    assert result.selected_channel == AlertChannel.NONE
    assert result.alert_enabled is False
    assert "priority_attribute_not_active" in result.blocked_reasons


def test_alert_blocks_priority_attribute_free_text():
    request = create_demo_passive_alert_request(
        alert_request_demo_id="test-alert-free-text-001",
        priority_attribute_token="quiero viajar gratis",
    )

    result = evaluate_passive_alert_request(request)

    assert result.status == AlertDecisionStatus.BLOCKED
    assert result.selected_channel == AlertChannel.NONE
    assert result.alert_enabled is False
    assert "priority_attribute_token_looks_like_free_text" in result.blocked_reasons


def test_assert_no_prohibited_fields_rejects_dni():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "alert_request_demo_id": "test-alert-sensitive-dni",
            }
        )

    assert "dni" in str(error.value).lower()


def test_assert_no_prohibited_fields_rejects_medical_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "diagnostico": "dato no permitido",
                "cud": "dato no permitido",
            }
        )

    message = str(error.value).lower()

    assert "diagnostico" in message
    assert "cud" in message


def test_create_demo_passive_alert_request_rejects_empty_alert_id():
    with pytest.raises(ValueError):
        create_demo_passive_alert_request(
            alert_request_demo_id="",
            priority_attribute_token="test-priority-attribute-empty-alert-id",
        )


def test_create_demo_passive_alert_request_rejects_empty_priority_attribute_token():
    with pytest.raises(ValueError):
        create_demo_passive_alert_request(
            alert_request_demo_id="test-alert-empty-priority-attribute",
            priority_attribute_token="",
        )

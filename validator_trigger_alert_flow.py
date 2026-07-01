import pytest

from validator_trigger_alert_flow import (
    AlertChannel,
    AssistanceMode,
    TriggerStatus,
    ValidationPointType,
    ValidationStatus,
    assert_no_prohibited_fields,
    create_demo_priority_attribute_snapshot,
    create_demo_station_operator_context,
    create_demo_validation_alert_preferences,
    create_demo_validation_event,
    create_demo_validator_trigger_request,
    evaluate_validator_trigger_request,
    result_to_dict,
    run_demo,
)


def test_run_demo_triggers_passive_alert_after_vehicle_validation():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Alerta Posterior a Validación"
    assert result["demo_mode"] is True
    assert result["status"] == "triggered"
    assert result["validation_paid"] is True
    assert result["priority_active"] is True
    assert result["selected_channels"] == ["passive_internal"]
    assert result["passive_alert_enabled"] is True
    assert result["luminous_alert_enabled"] is False
    assert result["visible_generic_alert_enabled"] is False
    assert result["station_operator_notification_enabled"] is False
    assert result["blocked_reasons"] == []
    assert result["degraded_reasons"] == []

    assert "validadora" in result["validation_trigger_notice"]
    assert "molinete" in result["validation_trigger_notice"]
    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]
    assert "no diagnostica" in result["driver_burden"].lower()
    assert "no impone obligaciones" in result["passenger_burden"].lower()

    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "Sin modificación de validadoras reales." in result["warnings"]
    assert "Sin modificación de molinetes reales." in result["warnings"]
    assert "La alerta se evalúa sólo luego de validar el pago del pasaje." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-to-dict-001"
    )

    result = evaluate_validator_trigger_request(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Alerta Posterior a Validación"
    assert data["demo_mode"] is True
    assert isinstance(data["selected_channels"], list)
    assert isinstance(data["blocked_reasons"], list)
    assert isinstance(data["degraded_reasons"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_trigger_blocks_outside_argentina_context():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-outside-argentina-001",
        country="Uruguay",
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-outside-argentina-001",
        validation_event=validation_event,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert result.validation_paid is True
    assert result.priority_active is True
    assert result.selected_channels == []
    assert "outside_argentina_context" in result.blocked_reasons


def test_trigger_blocks_when_payment_not_confirmed():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-not-paid-001",
        validation_status=ValidationStatus.REJECTED,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-not-paid-001",
        validation_event=validation_event,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert result.validation_paid is False
    assert result.selected_channels == []
    assert "validation_payment_not_confirmed" in result.blocked_reasons


def test_trigger_blocks_when_priority_attribute_not_active():
    priority_snapshot = create_demo_priority_attribute_snapshot(
        priority_attribute_token="test-priority-attribute-inactive-001",
        priority_attribute_active=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-priority-inactive-001",
        priority_snapshot=priority_snapshot,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert result.priority_active is False
    assert result.selected_channels == []
    assert "priority_attribute_not_active" in result.blocked_reasons


def test_trigger_blocks_when_need_not_previously_accredited():
    priority_snapshot = create_demo_priority_attribute_snapshot(
        priority_attribute_token="test-priority-attribute-not-accredited-001",
        previously_accredited_need=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-need-not-accredited-001",
        priority_snapshot=priority_snapshot,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert result.selected_channels == []
    assert "need_not_previously_accredited" in result.blocked_reasons


def test_trigger_blocks_priority_attribute_free_text():
    priority_snapshot = create_demo_priority_attribute_snapshot(
        priority_attribute_token="quiero viajar gratis",
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-priority-free-text-001",
        priority_snapshot=priority_snapshot,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert result.selected_channels == []
    assert "priority_attribute_token_looks_like_free_text" in result.blocked_reasons


def test_vehicle_validator_requires_vehicle_context():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-vehicle-without-context-001",
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        vehicle_demo_id=None,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-vehicle-without-context-001",
        validation_event=validation_event,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert "vehicle_validator_without_vehicle_context" in result.blocked_reasons


def test_station_turnstile_requires_station_context():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-turnstile-without-station-001",
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        vehicle_demo_id=None,
        station_demo_id=None,
        turnstile_demo_id="test-turnstile-001",
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-turnstile-without-station-001",
        validation_event=validation_event,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert "station_turnstile_without_station_context" in result.blocked_reasons


def test_station_turnstile_requires_turnstile_context():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-turnstile-without-turnstile-001",
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        vehicle_demo_id=None,
        station_demo_id="test-station-001",
        turnstile_demo_id=None,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-turnstile-without-turnstile-001",
        validation_event=validation_event,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.BLOCKED
    assert "station_turnstile_without_turnstile_context" in result.blocked_reasons


def test_silent_mode_does_not_emit_alert_but_validation_is_accepted():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.SILENT,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=True,
        allow_visible_generic_alert_after_validation=True,
        allow_luminous_alert_after_validation=True,
        allow_station_operator_notification=True,
        allow_emergency_help_notification=True,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-silent-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert result.validation_paid is True
    assert result.priority_active is True
    assert result.selected_channels == []
    assert result.passive_alert_enabled is False
    assert result.visible_generic_alert_enabled is False
    assert result.luminous_alert_enabled is False
    assert result.station_operator_notification_enabled is False
    assert result.blocked_reasons == []
    assert result.degraded_reasons == []
    assert "modo silencioso" in result.message.lower()


def test_passive_mode_triggers_passive_internal_channel():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.PASSIVE,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=False,
        allow_visible_generic_alert_after_validation=False,
        allow_luminous_alert_after_validation=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-passive-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert result.selected_channels == [AlertChannel.PASSIVE_INTERNAL]
    assert result.passive_alert_enabled is True


def test_discreet_mode_triggers_discreet_channel_when_allowed():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.DISCREET,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=True,
        allow_visible_generic_alert_after_validation=False,
        allow_luminous_alert_after_validation=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-discreet-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert result.selected_channels == [AlertChannel.DISCREET_GENERIC]
    assert result.passive_alert_enabled is False


def test_discreet_mode_falls_back_to_passive_when_discreet_not_allowed():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.DISCREET,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=False,
        allow_visible_generic_alert_after_validation=False,
        allow_luminous_alert_after_validation=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-discreet-fallback-passive-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert result.selected_channels == [AlertChannel.PASSIVE_INTERNAL]
    assert result.passive_alert_enabled is True


def test_visible_generic_mode_triggers_visible_channel_when_allowed():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.VISIBLE_GENERIC,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=True,
        allow_visible_generic_alert_after_validation=True,
        allow_luminous_alert_after_validation=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-visible-allowed-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert result.selected_channels == [AlertChannel.VISIBLE_GENERIC]
    assert result.visible_generic_alert_enabled is True
    assert result.degraded_reasons == []


def test_visible_generic_mode_degrades_when_visible_not_allowed():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.VISIBLE_GENERIC,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=True,
        allow_visible_generic_alert_after_validation=False,
        allow_luminous_alert_after_validation=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-visible-degraded-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.DEGRADED
    assert result.selected_channels == [AlertChannel.DISCREET_GENERIC]
    assert result.visible_generic_alert_enabled is False
    assert "visible_alert_degraded_to_less_exposed_channel" in result.degraded_reasons


def test_luminous_generic_mode_triggers_luminous_channel_when_allowed():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.LUMINOUS_GENERIC,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=True,
        allow_visible_generic_alert_after_validation=True,
        allow_luminous_alert_after_validation=True,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-luminous-allowed-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert result.selected_channels == [AlertChannel.LUMINOUS_GENERIC]
    assert result.luminous_alert_enabled is True
    assert result.degraded_reasons == []


def test_luminous_generic_mode_degrades_when_luminous_not_allowed():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.LUMINOUS_GENERIC,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=True,
        allow_visible_generic_alert_after_validation=True,
        allow_luminous_alert_after_validation=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-luminous-degraded-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.DEGRADED
    assert result.selected_channels == [AlertChannel.VISIBLE_GENERIC]
    assert result.luminous_alert_enabled is False
    assert "luminous_alert_degraded_to_less_exposed_channel" in result.degraded_reasons


def test_preventive_mode_notifies_station_operator_when_turnstile_and_user_allows():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-turnstile-operator-001",
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        vehicle_demo_id=None,
        station_demo_id="test-station-operator-001",
        turnstile_demo_id="test-turnstile-operator-001",
    )

    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.PREVENTIVE,
        allow_passive_alert_after_validation=True,
        allow_discreet_alert_after_validation=True,
        allow_visible_generic_alert_after_validation=False,
        allow_luminous_alert_after_validation=False,
        allow_station_operator_notification=True,
        allow_emergency_help_notification=False,
    )

    station_operator_context = create_demo_station_operator_context(
        station_staff_present=True,
        operator_device_channel_available=True,
        station_has_assistance_protocol=True,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-turnstile-operator-001",
        validation_event=validation_event,
        preferences=preferences,
        station_operator_context=station_operator_context,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert AlertChannel.PASSIVE_INTERNAL in result.selected_channels
    assert AlertChannel.STATION_OPERATOR_NOTIFICATION in result.selected_channels
    assert result.station_operator_notification_enabled is True
    assert result.passive_alert_enabled is True
    assert "operarios presentes" in result.station_operator_notice


def test_station_operator_notification_degrades_when_validation_is_vehicle_validator():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-vehicle-operator-not-available-001",
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        vehicle_demo_id="test-vehicle-operator-not-available-001",
    )

    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.PREVENTIVE,
        allow_passive_alert_after_validation=True,
        allow_station_operator_notification=True,
        allow_emergency_help_notification=False,
    )

    station_operator_context = create_demo_station_operator_context(
        station_staff_present=True,
        operator_device_channel_available=True,
        station_has_assistance_protocol=True,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-vehicle-operator-not-available-001",
        validation_event=validation_event,
        preferences=preferences,
        station_operator_context=station_operator_context,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.DEGRADED
    assert AlertChannel.PASSIVE_INTERNAL in result.selected_channels
    assert AlertChannel.STATION_OPERATOR_NOTIFICATION not in result.selected_channels
    assert result.station_operator_notification_enabled is False
    assert "station_operator_notification_not_available" in result.degraded_reasons
    assert "validadora de unidad" in result.station_operator_notice


def test_station_operator_notification_degrades_when_no_operator_context():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-turnstile-no-operator-context-001",
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        vehicle_demo_id=None,
        station_demo_id="test-station-no-operator-context-001",
        turnstile_demo_id="test-turnstile-no-operator-context-001",
    )

    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.PREVENTIVE,
        allow_passive_alert_after_validation=True,
        allow_station_operator_notification=True,
        allow_emergency_help_notification=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-turnstile-no-operator-context-001",
        validation_event=validation_event,
        preferences=preferences,
        station_operator_context=None,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.DEGRADED
    assert AlertChannel.PASSIVE_INTERNAL in result.selected_channels
    assert AlertChannel.STATION_OPERATOR_NOTIFICATION not in result.selected_channels
    assert "station_operator_notification_not_available" in result.degraded_reasons


def test_station_operator_notification_degrades_when_staff_not_present():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-turnstile-staff-not-present-001",
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        vehicle_demo_id=None,
        station_demo_id="test-station-staff-not-present-001",
        turnstile_demo_id="test-turnstile-staff-not-present-001",
    )

    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.PREVENTIVE,
        allow_passive_alert_after_validation=True,
        allow_station_operator_notification=True,
        allow_emergency_help_notification=False,
    )

    station_operator_context = create_demo_station_operator_context(
        station_staff_present=False,
        operator_device_channel_available=True,
        station_has_assistance_protocol=True,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-turnstile-staff-not-present-001",
        validation_event=validation_event,
        preferences=preferences,
        station_operator_context=station_operator_context,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.DEGRADED
    assert AlertChannel.STATION_OPERATOR_NOTIFICATION not in result.selected_channels
    assert "station_operator_notification_not_available" in result.degraded_reasons


def test_emergency_help_notification_can_enable_station_operator_notification():
    validation_event = create_demo_validation_event(
        validation_event_demo_id="test-validation-turnstile-emergency-help-001",
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        vehicle_demo_id=None,
        station_demo_id="test-station-emergency-help-001",
        turnstile_demo_id="test-turnstile-emergency-help-001",
    )

    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.PREVENTIVE,
        allow_passive_alert_after_validation=True,
        allow_station_operator_notification=False,
        allow_emergency_help_notification=True,
    )

    station_operator_context = create_demo_station_operator_context(
        station_staff_present=True,
        operator_device_channel_available=True,
        station_has_assistance_protocol=True,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-turnstile-emergency-help-001",
        validation_event=validation_event,
        preferences=preferences,
        station_operator_context=station_operator_context,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.TRIGGERED
    assert AlertChannel.STATION_OPERATOR_NOTIFICATION in result.selected_channels
    assert result.station_operator_notification_enabled is True


def test_no_channel_available_under_user_preferences_degrades():
    preferences = create_demo_validation_alert_preferences(
        assistance_mode=AssistanceMode.PASSIVE,
        allow_passive_alert_after_validation=False,
        allow_discreet_alert_after_validation=False,
        allow_visible_generic_alert_after_validation=False,
        allow_luminous_alert_after_validation=False,
        allow_station_operator_notification=False,
        allow_emergency_help_notification=False,
    )

    request = create_demo_validator_trigger_request(
        trigger_request_demo_id="test-trigger-no-channel-001",
        preferences=preferences,
    )

    result = evaluate_validator_trigger_request(request)

    assert result.status == TriggerStatus.DEGRADED
    assert result.selected_channels == []
    assert "no_alert_channel_available_under_user_preferences" in result.degraded_reasons


def test_assert_no_prohibited_fields_rejects_dni():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "validation_event_demo_id": "test-sensitive-dni",
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


def test_create_demo_validation_event_rejects_empty_validation_event_id():
    with pytest.raises(ValueError):
        create_demo_validation_event(
            validation_event_demo_id="",
        )


def test_create_demo_priority_attribute_snapshot_rejects_empty_priority_token():
    with pytest.raises(ValueError):
        create_demo_priority_attribute_snapshot(
            priority_attribute_token="",
        )


def test_create_demo_priority_attribute_snapshot_rejects_empty_preference_version():
    with pytest.raises(ValueError):
        create_demo_priority_attribute_snapshot(
            priority_attribute_token="test-priority-token-empty-preference-version",
            preference_version_demo_id="",
        )


def test_create_demo_validator_trigger_request_rejects_empty_trigger_id():
    with pytest.raises(ValueError):
        create_demo_validator_trigger_request(
            trigger_request_demo_id="",
        )

import pytest

from sube_account_preferences_flow import (
    AssistancePreferenceMode,
    PreferenceSource,
    PreferenceUpdateStatus,
    SyncTarget,
    assert_no_prohibited_fields,
    create_demo_preference_update_request,
    create_demo_sube_account_context,
    create_demo_user_assistance_preferences,
    evaluate_preference_update_request,
    result_to_dict,
    run_demo,
)


def test_run_demo_accepts_preference_update_from_sube_account():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Preferencias desde Cuenta SUBE"
    assert result["demo_mode"] is True

    assert result["status"] in {"accepted", "needs_review"}
    assert result["preferences_saved_demo"] is True
    assert result["simulated_sync_enabled"] is True

    assert "sube_account" in result["synchronized_targets"]
    assert "sube_card_profile" in result["synchronized_targets"]
    assert "validator_edge" in result["synchronized_targets"]
    assert "turnstile_edge" in result["synchronized_targets"]
    assert "solidary_sync_frontend" in result["synchronized_targets"]

    assert "station_operator_devices" in result["blocked_targets"]

    assert result["risk_flags"] in [
        [],
        ["some_targets_blocked_by_user_preferences"],
    ]

    assert "cuenta SUBE demostrativa" in result["account_scope"]
    assert "validadora" in result["validation_trigger_notice"]
    assert "molinete" in result["validation_trigger_notice"]
    assert "Bono Solidario" in result["solidary_bonus_frontend_notice"]
    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]

    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "Sin consulta a cuentas reales." in result["warnings"]
    assert "Sin consulta a tarjetas reales." in result["warnings"]
    assert "Las preferencias son revocables." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_preference_update_request(
        request_demo_id="test-preference-to-dict-001",
        source=PreferenceSource.WEB_PORTAL,
    )

    result = evaluate_preference_update_request(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Preferencias desde Cuenta SUBE"
    assert data["demo_mode"] is True
    assert isinstance(data["synchronized_targets"], list)
    assert isinstance(data["blocked_targets"], list)
    assert isinstance(data["risk_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_preference_update_accepts_web_portal_source():
    request = create_demo_preference_update_request(
        request_demo_id="test-preference-web-portal-001",
        source=PreferenceSource.WEB_PORTAL,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.SUBE_CARD_PROFILE,
            SyncTarget.VALIDATOR_EDGE,
            SyncTarget.TURNSTILE_EDGE,
            SyncTarget.SOLIDARY_SYNC_FRONTEND,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.ACCEPTED
    assert result.preferences_saved_demo is True
    assert result.simulated_sync_enabled is True
    assert SyncTarget.SUBE_ACCOUNT in result.synchronized_targets
    assert SyncTarget.SUBE_CARD_PROFILE in result.synchronized_targets
    assert SyncTarget.VALIDATOR_EDGE in result.synchronized_targets
    assert SyncTarget.TURNSTILE_EDGE in result.synchronized_targets
    assert SyncTarget.SOLIDARY_SYNC_FRONTEND in result.synchronized_targets
    assert result.blocked_targets == []
    assert result.risk_flags == []


def test_preference_update_accepts_mobile_app_source():
    request = create_demo_preference_update_request(
        request_demo_id="test-preference-mobile-app-001",
        source=PreferenceSource.MOBILE_APP,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.SUBE_CARD_PROFILE,
            SyncTarget.VALIDATOR_EDGE,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.ACCEPTED
    assert result.preferences_saved_demo is True
    assert result.simulated_sync_enabled is True
    assert SyncTarget.SUBE_ACCOUNT in result.synchronized_targets
    assert SyncTarget.SUBE_CARD_PROFILE in result.synchronized_targets
    assert SyncTarget.VALIDATOR_EDGE in result.synchronized_targets


def test_preference_update_rejects_without_user_confirmation():
    request = create_demo_preference_update_request(
        request_demo_id="test-preference-no-confirmation-001",
        user_confirms_update=False,
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.REJECTED
    assert result.preferences_saved_demo is False
    assert result.simulated_sync_enabled is False
    assert "user_confirmation_required" in result.risk_flags
    assert result.synchronized_targets == []
    assert set(result.blocked_targets) == set(request.requested_sync_targets)


def test_preference_update_rejects_inactive_sube_account():
    account_context = create_demo_sube_account_context(
        account_demo_id="test-account-inactive-001",
        card_demo_id="test-card-inactive-001",
        priority_attribute_token="test-priority-attribute-inactive-account-001",
        account_active=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-inactive-account-001",
        account_context=account_context,
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.REJECTED
    assert result.preferences_saved_demo is False
    assert "sube_account_not_active" in result.risk_flags


def test_preference_update_rejects_unassociated_sube_card():
    account_context = create_demo_sube_account_context(
        account_demo_id="test-account-unassociated-card-001",
        card_demo_id="test-card-unassociated-001",
        priority_attribute_token="test-priority-attribute-unassociated-card-001",
        card_associated=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-unassociated-card-001",
        account_context=account_context,
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.REJECTED
    assert result.preferences_saved_demo is False
    assert "sube_card_not_associated" in result.risk_flags


def test_preference_update_rejects_inactive_priority_attribute():
    account_context = create_demo_sube_account_context(
        account_demo_id="test-account-inactive-priority-001",
        card_demo_id="test-card-inactive-priority-001",
        priority_attribute_token="test-priority-attribute-inactive-001",
        priority_attribute_active=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-inactive-priority-001",
        account_context=account_context,
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.REJECTED
    assert result.preferences_saved_demo is False
    assert "priority_attribute_not_active" in result.risk_flags


def test_preference_update_rejects_non_revocable_preference():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PASSIVE,
        preference_revocable=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-not-revocable-001",
        preferences=preferences,
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.REJECTED
    assert result.preferences_saved_demo is False
    assert "preference_must_be_revocable" in result.risk_flags


def test_preference_update_rejects_priority_attribute_free_text():
    account_context = create_demo_sube_account_context(
        account_demo_id="test-account-free-text-001",
        card_demo_id="test-card-free-text-001",
        priority_attribute_token="quiero viajar gratis",
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-free-text-001",
        account_context=account_context,
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.REJECTED
    assert result.preferences_saved_demo is False
    assert "priority_attribute_token_looks_like_free_text" in result.risk_flags


def test_preference_update_rejects_without_sync_targets():
    request = create_demo_preference_update_request(
        request_demo_id="test-preference-no-sync-targets-001",
        requested_sync_targets=[],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.REJECTED
    assert result.preferences_saved_demo is False
    assert "no_sync_targets_requested" in result.risk_flags


def test_station_operator_devices_are_blocked_when_user_does_not_allow_notifications():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PASSIVE,
        allow_station_operator_notification=False,
        allow_emergency_help_notification=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-operator-blocked-001",
        preferences=preferences,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.STATION_OPERATOR_DEVICES,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.NEEDS_REVIEW
    assert result.preferences_saved_demo is True
    assert SyncTarget.SUBE_ACCOUNT in result.synchronized_targets
    assert SyncTarget.STATION_OPERATOR_DEVICES in result.blocked_targets
    assert "some_targets_blocked_by_user_preferences" in result.risk_flags
    assert "no habilitó notificación a operarios" in result.station_operator_notice


def test_station_operator_devices_are_enabled_when_user_allows_station_notification():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PREVENTIVE,
        allow_station_operator_notification=True,
        allow_emergency_help_notification=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-operator-enabled-001",
        preferences=preferences,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.STATION_OPERATOR_DEVICES,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.ACCEPTED
    assert result.preferences_saved_demo is True
    assert SyncTarget.SUBE_ACCOUNT in result.synchronized_targets
    assert SyncTarget.STATION_OPERATOR_DEVICES in result.synchronized_targets
    assert result.blocked_targets == []
    assert "habilitó conceptualmente la notificación" in result.station_operator_notice


def test_station_operator_devices_are_enabled_when_user_allows_emergency_help_notification():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PREVENTIVE,
        allow_station_operator_notification=False,
        allow_emergency_help_notification=True,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-emergency-help-enabled-001",
        preferences=preferences,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.STATION_OPERATOR_DEVICES,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.ACCEPTED
    assert result.preferences_saved_demo is True
    assert SyncTarget.STATION_OPERATOR_DEVICES in result.synchronized_targets
    assert result.blocked_targets == []


def test_solidary_bonus_frontend_is_blocked_when_user_does_not_allow_it():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PASSIVE,
        allow_solidary_bonus_sync_frontend=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-solidary-frontend-blocked-001",
        preferences=preferences,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.SOLIDARY_SYNC_FRONTEND,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.NEEDS_REVIEW
    assert result.preferences_saved_demo is True
    assert SyncTarget.SUBE_ACCOUNT in result.synchronized_targets
    assert SyncTarget.SOLIDARY_SYNC_FRONTEND in result.blocked_targets
    assert "some_targets_blocked_by_user_preferences" in result.risk_flags
    assert "no habilitó el frontend" in result.solidary_bonus_frontend_notice


def test_solidary_bonus_frontend_is_enabled_when_user_allows_it():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PASSIVE,
        allow_solidary_bonus_sync_frontend=True,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-solidary-frontend-enabled-001",
        preferences=preferences,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.SOLIDARY_SYNC_FRONTEND,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.ACCEPTED
    assert result.preferences_saved_demo is True
    assert SyncTarget.SOLIDARY_SYNC_FRONTEND in result.synchronized_targets
    assert result.blocked_targets == []
    assert "frontend de sincronización de Bono Solidario" in result.solidary_bonus_frontend_notice


def test_validator_and_turnstile_edges_are_blocked_when_no_alert_after_validation_is_enabled():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.SILENT,
        allow_passive_alert_after_validation=False,
        allow_luminous_alert_after_validation=False,
        allow_visible_generic_alert_after_validation=False,
        allow_station_operator_notification=False,
        allow_emergency_help_notification=False,
        allow_solidary_bonus_sync_frontend=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-validator-turnstile-blocked-001",
        preferences=preferences,
        requested_sync_targets=[
            SyncTarget.SUBE_ACCOUNT,
            SyncTarget.VALIDATOR_EDGE,
            SyncTarget.TURNSTILE_EDGE,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.NEEDS_REVIEW
    assert SyncTarget.SUBE_ACCOUNT in result.synchronized_targets
    assert SyncTarget.VALIDATOR_EDGE in result.blocked_targets
    assert SyncTarget.TURNSTILE_EDGE in result.blocked_targets
    assert "some_targets_blocked_by_user_preferences" in result.risk_flags


def test_validator_and_turnstile_edges_are_enabled_when_passive_alert_is_enabled():
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PASSIVE,
        allow_passive_alert_after_validation=True,
        allow_luminous_alert_after_validation=False,
        allow_visible_generic_alert_after_validation=False,
        allow_station_operator_notification=False,
        allow_emergency_help_notification=False,
    )

    request = create_demo_preference_update_request(
        request_demo_id="test-preference-validator-turnstile-enabled-001",
        preferences=preferences,
        requested_sync_targets=[
            SyncTarget.VALIDATOR_EDGE,
            SyncTarget.TURNSTILE_EDGE,
        ],
    )

    result = evaluate_preference_update_request(request)

    assert result.status == PreferenceUpdateStatus.ACCEPTED
    assert SyncTarget.VALIDATOR_EDGE in result.synchronized_targets
    assert SyncTarget.TURNSTILE_EDGE in result.synchronized_targets
    assert result.blocked_targets == []


def test_assert_no_prohibited_fields_rejects_dni():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "request_demo_id": "test-sensitive-dni",
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


def test_create_demo_sube_account_context_rejects_empty_account_demo_id():
    with pytest.raises(ValueError):
        create_demo_sube_account_context(
            account_demo_id="",
            card_demo_id="test-card-empty-account",
            priority_attribute_token="test-priority-attribute-empty-account",
        )


def test_create_demo_sube_account_context_rejects_empty_card_demo_id():
    with pytest.raises(ValueError):
        create_demo_sube_account_context(
            account_demo_id="test-account-empty-card",
            card_demo_id="",
            priority_attribute_token="test-priority-attribute-empty-card",
        )


def test_create_demo_sube_account_context_rejects_empty_priority_attribute_token():
    with pytest.raises(ValueError):
        create_demo_sube_account_context(
            account_demo_id="test-account-empty-priority",
            card_demo_id="test-card-empty-priority",
            priority_attribute_token="",
        )


def test_create_demo_preference_update_request_rejects_empty_request_demo_id():
    with pytest.raises(ValueError):
        create_demo_preference_update_request(
            request_demo_id="",
        )

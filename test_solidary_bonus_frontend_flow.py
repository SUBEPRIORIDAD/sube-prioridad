import pytest

from solidary_bonus_frontend_flow import (
    FrontendChannel,
    FrontendDecisionStatus,
    RecipientSelectionMethod,
    SeatType,
    assert_no_prohibited_fields,
    create_demo_candidate_collaborator,
    create_demo_priority_account_frontend_context,
    create_demo_solidary_bonus_frontend_request,
    create_demo_solidary_frontend_transport_context,
    evaluate_solidary_bonus_frontend_request,
    result_to_dict,
    run_demo,
)


def test_run_demo_is_ready_for_security_flow():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Frontend Conceptual de Bono Solidario"
    assert result["demo_mode"] is True
    assert result["status"] == "ready_for_security_flow"
    assert result["frontend_ready"] is True
    assert result["handoff_to_security_flow_enabled"] is True
    assert result["solidary_point_demo"] == 0
    assert result["risk_flags"] == []

    assert result["frontend_channel"] == "mobile_app"
    assert result["recipient_selection_method"] == "same_trip_context_demo"

    payload = result["security_flow_payload_demo"]

    assert payload["sync_event_demo_id"] == "demo-solidary-frontend-request-001"
    assert payload["priority_user_token"] == "demo-priority-user-001"
    assert payload["priority_attribute_token"] == "demo-priority-attribute-001"
    assert payload["collaborator_token"] == "demo-collaborator-001"
    assert payload["country"] == "Argentina"
    assert payload["seat_type"] == "general_use"
    assert payload["priority_user_confirms_sync"] is True
    assert payload["voluntary_seat_yield"] is True
    assert payload["same_transport_context"] is True

    assert "usuario SUBE Prioridad" in result["priority_user_control"]
    assert "colaborador no puede" in result["collaborator_limit"].lower()
    assert "validación demostrativa de pago" in result["validation_context_notice"]
    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]
    assert "chofer no verifica" in result["driver_burden"].lower()

    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "Sin transferencia real de beneficios." in result["warnings"]
    assert "Sin puntos reales." in result["warnings"]
    assert "Sin carga operativa para el chofer." in result["warnings"]
    assert "El handoff posterior debe pasar por filtros de seguridad antifraude." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-to-dict-001"
    )

    result = evaluate_solidary_bonus_frontend_request(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Frontend Conceptual de Bono Solidario"
    assert data["demo_mode"] is True
    assert isinstance(data["risk_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["security_flow_payload_demo"], dict)
    assert isinstance(data["timestamp_utc"], str)


def test_frontend_accepts_web_portal_channel():
    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-web-001",
        frontend_channel=FrontendChannel.WEB_PORTAL,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.READY_FOR_SECURITY_FLOW
    assert result.frontend_ready is True
    assert result.handoff_to_security_flow_enabled is True
    assert result.frontend_channel == FrontendChannel.WEB_PORTAL
    assert result.risk_flags == []


def test_frontend_accepts_account_panel_channel():
    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-account-panel-001",
        frontend_channel=FrontendChannel.ACCOUNT_PANEL,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.READY_FOR_SECURITY_FLOW
    assert result.frontend_ready is True
    assert result.handoff_to_security_flow_enabled is True
    assert result.frontend_channel == FrontendChannel.ACCOUNT_PANEL


def test_frontend_accepts_temporary_qr_selection_method():
    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-collaborator-qr-001",
        selection_method=RecipientSelectionMethod.TEMPORARY_QR_DEMO,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-qr-001",
        candidate_collaborator=candidate,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.READY_FOR_SECURITY_FLOW
    assert result.recipient_selection_method == RecipientSelectionMethod.TEMPORARY_QR_DEMO
    assert result.security_flow_payload_demo["collaborator_token"] == "test-collaborator-qr-001"


def test_frontend_rejects_outside_argentina_context():
    transport_context = create_demo_solidary_frontend_transport_context(
        country="Uruguay",
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-outside-argentina-001",
        transport_context=transport_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert result.frontend_ready is False
    assert result.handoff_to_security_flow_enabled is False
    assert result.security_flow_payload_demo == {}
    assert "outside_argentina_context" in result.risk_flags


def test_frontend_rejects_without_validation_payment():
    transport_context = create_demo_solidary_frontend_transport_context(
        validation_paid=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-no-payment-001",
        transport_context=transport_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert result.frontend_ready is False
    assert result.handoff_to_security_flow_enabled is False
    assert "validation_payment_not_confirmed" in result.risk_flags


def test_frontend_rejects_inactive_sube_account():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-inactive-001",
        card_demo_id="test-card-inactive-001",
        priority_user_token="test-priority-user-inactive-account-001",
        priority_attribute_token="test-priority-attribute-inactive-account-001",
        account_active=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-inactive-account-001",
        priority_account_context=account_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "sube_account_not_active" in result.risk_flags


def test_frontend_rejects_unassociated_sube_card():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-unassociated-card-001",
        card_demo_id="test-card-unassociated-001",
        priority_user_token="test-priority-user-unassociated-card-001",
        priority_attribute_token="test-priority-attribute-unassociated-card-001",
        card_associated=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-unassociated-card-001",
        priority_account_context=account_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "sube_card_not_associated" in result.risk_flags


def test_frontend_rejects_inactive_priority_attribute():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-inactive-priority-001",
        card_demo_id="test-card-inactive-priority-001",
        priority_user_token="test-priority-user-inactive-priority-001",
        priority_attribute_token="test-priority-attribute-inactive-priority-001",
        priority_attribute_active=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-inactive-priority-001",
        priority_account_context=account_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "priority_attribute_not_active" in result.risk_flags


def test_frontend_rejects_need_not_previously_accredited():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-not-accredited-001",
        card_demo_id="test-card-not-accredited-001",
        priority_user_token="test-priority-user-not-accredited-001",
        priority_attribute_token="test-priority-attribute-not-accredited-001",
        previously_accredited_need=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-not-accredited-001",
        priority_account_context=account_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "need_not_previously_accredited" in result.risk_flags


def test_frontend_rejects_when_user_did_not_enable_solidary_frontend():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-frontend-disabled-001",
        card_demo_id="test-card-frontend-disabled-001",
        priority_user_token="test-priority-user-frontend-disabled-001",
        priority_attribute_token="test-priority-attribute-frontend-disabled-001",
        solidary_bonus_frontend_enabled=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-disabled-001",
        priority_account_context=account_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "solidary_bonus_frontend_not_enabled_by_user" in result.risk_flags


def test_frontend_rejects_without_priority_user_confirmation():
    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-no-confirmation-001",
        priority_user_confirms_send=False,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert result.frontend_ready is False
    assert result.handoff_to_security_flow_enabled is False
    assert "priority_user_confirmation_required" in result.risk_flags


def test_frontend_needs_review_without_demo_scope_acknowledgement():
    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-demo-scope-review-001",
        priority_user_understands_demo_scope=False,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.NEEDS_REVIEW
    assert result.frontend_ready is False
    assert result.handoff_to_security_flow_enabled is False
    assert result.security_flow_payload_demo == {}
    assert result.risk_flags == ["demo_scope_acknowledgement_required"]


def test_frontend_rejects_priority_user_token_free_text():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-priority-user-free-text-001",
        card_demo_id="test-card-priority-user-free-text-001",
        priority_user_token="quiero viajar gratis",
        priority_attribute_token="test-priority-attribute-free-text-001",
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-priority-user-free-text-001",
        priority_account_context=account_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "priority_user_token_looks_like_free_text" in result.risk_flags


def test_frontend_rejects_priority_attribute_token_free_text():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-priority-attribute-free-text-001",
        card_demo_id="test-card-priority-attribute-free-text-001",
        priority_user_token="test-priority-user-free-text-001",
        priority_attribute_token="quiero viajar gratis",
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-priority-attribute-free-text-001",
        priority_account_context=account_context,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "priority_attribute_token_looks_like_free_text" in result.risk_flags


def test_frontend_rejects_collaborator_token_free_text():
    candidate = create_demo_candidate_collaborator(
        collaborator_token="quiero viajar gratis",
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-collaborator-free-text-001",
        candidate_collaborator=candidate,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "collaborator_token_looks_like_free_text" in result.risk_flags


def test_frontend_rejects_self_bonus_attempt():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-self-bonus-001",
        card_demo_id="test-card-self-bonus-001",
        priority_user_token="test-same-token-self-bonus-001",
        priority_attribute_token="test-priority-attribute-self-bonus-001",
    )

    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-same-token-self-bonus-001",
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-self-bonus-001",
        priority_account_context=account_context,
        candidate_collaborator=candidate,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "self_bonus_attempt" in result.risk_flags


def test_frontend_rejects_different_transport_context():
    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-collaborator-different-context-001",
        same_transport_context=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-different-context-001",
        candidate_collaborator=candidate,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "different_transport_context" in result.risk_flags


def test_frontend_rejects_without_voluntary_seat_yield():
    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-collaborator-no-voluntary-yield-001",
        voluntary_seat_yield_declared=False,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-no-voluntary-yield-001",
        candidate_collaborator=candidate,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "no_voluntary_seat_yield_declared" in result.risk_flags


def test_frontend_rejects_collaborator_unilateral_claim():
    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-collaborator-unilateral-claim-001",
        collaborator_claims_reward=True,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-unilateral-claim-001",
        candidate_collaborator=candidate,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "collaborator_unilateral_claim" in result.risk_flags
    assert "colaborador no puede" in result.collaborator_limit.lower()


def test_frontend_rejects_legal_priority_seat():
    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-collaborator-legal-priority-seat-001",
        seat_type=SeatType.LEGAL_PRIORITY,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-legal-priority-seat-001",
        candidate_collaborator=candidate,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert "legal_priority_seat_not_eligible" in result.risk_flags


def test_frontend_rejects_multiple_risk_flags():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-account-multiple-risk-001",
        card_demo_id="test-card-multiple-risk-001",
        priority_user_token="test-priority-user-multiple-risk-001",
        priority_attribute_token="test-priority-attribute-multiple-risk-001",
        account_active=False,
        card_associated=False,
        priority_attribute_active=False,
    )

    transport_context = create_demo_solidary_frontend_transport_context(
        country="Uruguay",
        validation_paid=False,
    )

    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-collaborator-multiple-risk-001",
        same_transport_context=False,
        voluntary_seat_yield_declared=False,
        collaborator_claims_reward=True,
        seat_type=SeatType.LEGAL_PRIORITY,
    )

    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-multiple-risk-001",
        priority_account_context=account_context,
        transport_context=transport_context,
        candidate_collaborator=candidate,
        priority_user_confirms_send=False,
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    assert result.status == FrontendDecisionStatus.REJECTED
    assert result.frontend_ready is False
    assert result.handoff_to_security_flow_enabled is False
    assert "outside_argentina_context" in result.risk_flags
    assert "validation_payment_not_confirmed" in result.risk_flags
    assert "sube_account_not_active" in result.risk_flags
    assert "sube_card_not_associated" in result.risk_flags
    assert "priority_attribute_not_active" in result.risk_flags
    assert "priority_user_confirmation_required" in result.risk_flags
    assert "different_transport_context" in result.risk_flags
    assert "no_voluntary_seat_yield_declared" in result.risk_flags
    assert "collaborator_unilateral_claim" in result.risk_flags
    assert "legal_priority_seat_not_eligible" in result.risk_flags


def test_security_flow_payload_contains_minimal_demo_data_only():
    request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-solidary-frontend-minimal-payload-001",
    )

    result = evaluate_solidary_bonus_frontend_request(request)

    payload = result.security_flow_payload_demo

    assert result.status == FrontendDecisionStatus.READY_FOR_SECURITY_FLOW
    assert "dni" not in payload
    assert "nombre" not in payload
    assert "apellido" not in payload
    assert "diagnostico" not in payload
    assert "diagnóstico" not in payload
    assert "cud" not in payload
    assert "certificado_medico" not in payload
    assert "historia_clinica" not in payload

    expected_keys = {
        "sync_event_demo_id",
        "priority_user_token",
        "priority_attribute_token",
        "collaborator_token",
        "country",
        "network_demo_id",
        "route_demo_id",
        "vehicle_demo_id",
        "trip_demo_id",
        "time_window_demo_id",
        "seat_type",
        "priority_user_confirms_sync",
        "voluntary_seat_yield",
        "same_transport_context",
    }

    assert set(payload.keys()) == expected_keys


def test_assert_no_prohibited_fields_rejects_dni():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "frontend_request_demo_id": "test-sensitive-dni",
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


def test_create_demo_priority_account_frontend_context_rejects_empty_account_id():
    with pytest.raises(ValueError):
        create_demo_priority_account_frontend_context(
            account_demo_id="",
            card_demo_id="test-card-empty-account",
            priority_user_token="test-priority-user-empty-account",
            priority_attribute_token="test-priority-attribute-empty-account",
        )


def test_create_demo_priority_account_frontend_context_rejects_empty_card_id():
    with pytest.raises(ValueError):
        create_demo_priority_account_frontend_context(
            account_demo_id="test-account-empty-card",
            card_demo_id="",
            priority_user_token="test-priority-user-empty-card",
            priority_attribute_token="test-priority-attribute-empty-card",
        )


def test_create_demo_priority_account_frontend_context_rejects_empty_priority_user_token():
    with pytest.raises(ValueError):
        create_demo_priority_account_frontend_context(
            account_demo_id="test-account-empty-priority-user",
            card_demo_id="test-card-empty-priority-user",
            priority_user_token="",
            priority_attribute_token="test-priority-attribute-empty-priority-user",
        )


def test_create_demo_priority_account_frontend_context_rejects_empty_priority_attribute_token():
    with pytest.raises(ValueError):
        create_demo_priority_account_frontend_context(
            account_demo_id="test-account-empty-priority-attribute",
            card_demo_id="test-card-empty-priority-attribute",
            priority_user_token="test-priority-user-empty-priority-attribute",
            priority_attribute_token="",
        )


def test_create_demo_candidate_collaborator_rejects_empty_collaborator_token():
    with pytest.raises(ValueError):
        create_demo_candidate_collaborator(
            collaborator_token="",
        )


def test_create_demo_solidary_bonus_frontend_request_rejects_empty_frontend_request_id():
    with pytest.raises(ValueError):
        create_demo_solidary_bonus_frontend_request(
            frontend_request_demo_id="",
        )

import pytest

from solidary_bonus_frontend_flow import (
    FrontendChannel,
    RecipientSelectionMethod,
    create_demo_candidate_collaborator,
    create_demo_priority_account_frontend_context,
    create_demo_solidary_bonus_frontend_request,
    create_demo_solidary_frontend_transport_context,
)

from solidary_bonus_handoff_flow import (
    HandoffStatus,
    assert_no_prohibited_fields,
    create_demo_solidary_bonus_handoff_request,
    execute_solidary_bonus_handoff,
    result_to_dict,
    run_demo,
)

from solidary_sync_security_flow import SyncSecurityLedger


def test_run_demo_completes_handoff_successfully():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Handoff Seguro de Bono Solidario"
    assert result["demo_mode"] is True

    assert result["status"] == "completed"
    assert result["frontend_status"] == "ready_for_security_flow"
    assert result["security_status"] == "accepted"

    assert result["handoff_completed"] is True
    assert result["frontend_ready"] is True
    assert result["security_flow_executed"] is True
    assert result["solidary_point_demo"] == 1
    assert result["risk_flags"] == []

    assert result["frontend_result"]["status"] == "ready_for_security_flow"
    assert result["security_result"]["status"] == "accepted"
    assert result["security_result"]["solidary_point_demo"] == 1

    assert "usuario SUBE Prioridad" in result["priority_user_control"]
    assert "colaborador no puede" in result["collaborator_limit"].lower()
    assert "frontend no acredita puntos" in result["security_notice"].lower()
    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]
    assert "chofer no verifica" in result["driver_burden"].lower()

    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "Sin transferencia real de beneficios." in result["warnings"]
    assert "Sin puntos reales." in result["warnings"]
    assert "Sin carga operativa para el chofer." in result["warnings"]
    assert "El frontend sólo prepara el handoff." in result["warnings"]
    assert "El flujo de seguridad decide el resultado demostrativo." in result["warnings"]


def test_result_to_dict_is_serializable():
    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-to-dict-001"
    )

    result = execute_solidary_bonus_handoff(request)
    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Handoff Seguro de Bono Solidario"
    assert data["demo_mode"] is True
    assert isinstance(data["frontend_result"], dict)
    assert isinstance(data["security_result"], dict)
    assert isinstance(data["risk_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_handoff_completes_from_valid_frontend_request():
    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-valid-frontend-001",
        frontend_channel=FrontendChannel.WEB_PORTAL,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-valid-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.COMPLETED
    assert result.frontend_status == "ready_for_security_flow"
    assert result.security_status == "accepted"
    assert result.handoff_completed is True
    assert result.frontend_ready is True
    assert result.security_flow_executed is True
    assert result.solidary_point_demo == 1
    assert result.risk_flags == []


def test_handoff_blocks_when_frontend_is_not_ready_due_to_no_user_confirmation():
    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-front-no-confirmation-001",
        priority_user_confirms_send=False,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-no-user-confirmation-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.BLOCKED_BY_FRONTEND
    assert result.frontend_status == "rejected"
    assert result.security_status is None
    assert result.handoff_completed is False
    assert result.frontend_ready is False
    assert result.security_flow_executed is False
    assert result.solidary_point_demo == 0
    assert result.security_result == {}
    assert "priority_user_confirmation_required" in result.risk_flags


def test_handoff_blocks_when_frontend_requires_demo_scope_review():
    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-front-demo-scope-001",
        priority_user_understands_demo_scope=False,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-demo-scope-review-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.BLOCKED_BY_FRONTEND
    assert result.frontend_status == "needs_review"
    assert result.security_status is None
    assert result.security_flow_executed is False
    assert result.security_result == {}
    assert result.risk_flags == ["demo_scope_acknowledgement_required"]


def test_handoff_blocks_when_frontend_detects_outside_argentina_context():
    transport_context = create_demo_solidary_frontend_transport_context(
        country="Uruguay",
    )

    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-front-outside-argentina-001",
        transport_context=transport_context,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-outside-argentina-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.BLOCKED_BY_FRONTEND
    assert result.frontend_status == "rejected"
    assert result.security_status is None
    assert "outside_argentina_context" in result.risk_flags


def test_handoff_blocks_when_frontend_detects_no_payment_validation():
    transport_context = create_demo_solidary_frontend_transport_context(
        validation_paid=False,
    )

    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-front-no-payment-001",
        transport_context=transport_context,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-no-payment-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.BLOCKED_BY_FRONTEND
    assert result.frontend_status == "rejected"
    assert result.security_status is None
    assert "validation_payment_not_confirmed" in result.risk_flags


def test_handoff_blocks_when_frontend_detects_collaborator_unilateral_claim():
    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-handoff-collaborator-unilateral-001",
        collaborator_claims_reward=True,
    )

    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-front-unilateral-claim-001",
        candidate_collaborator=candidate,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-unilateral-claim-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.BLOCKED_BY_FRONTEND
    assert result.frontend_status == "rejected"
    assert result.security_status is None
    assert "collaborator_unilateral_claim" in result.risk_flags
    assert "colaborador no puede" in result.collaborator_limit.lower()


def test_handoff_blocks_when_frontend_detects_self_bonus_attempt():
    account_context = create_demo_priority_account_frontend_context(
        account_demo_id="test-handoff-account-self-001",
        card_demo_id="test-handoff-card-self-001",
        priority_user_token="test-handoff-same-token-001",
        priority_attribute_token="test-handoff-priority-attribute-self-001",
    )

    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-handoff-same-token-001",
    )

    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-front-self-bonus-001",
        priority_account_context=account_context,
        candidate_collaborator=candidate,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-self-bonus-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.BLOCKED_BY_FRONTEND
    assert result.frontend_status == "rejected"
    assert result.security_status is None
    assert "self_bonus_attempt" in result.risk_flags


def test_handoff_blocks_when_frontend_detects_legal_priority_seat():
    from solidary_bonus_frontend_flow import SeatType

    candidate = create_demo_candidate_collaborator(
        collaborator_token="test-handoff-collaborator-legal-seat-001",
        seat_type=SeatType.LEGAL_PRIORITY,
    )

    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-front-legal-seat-001",
        candidate_collaborator=candidate,
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-legal-seat-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    assert result.status == HandoffStatus.BLOCKED_BY_FRONTEND
    assert result.frontend_status == "rejected"
    assert result.security_status is None
    assert "legal_priority_seat_not_eligible" in result.risk_flags


def test_handoff_rejected_by_security_on_replay_with_same_ledger():
    ledger = SyncSecurityLedger()

    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-replay-sync-event-001",
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-replay-001",
        frontend_request=frontend_request,
    )

    first_result = execute_solidary_bonus_handoff(
        request=request,
        ledger=ledger,
    )

    second_result = execute_solidary_bonus_handoff(
        request=request,
        ledger=ledger,
    )

    assert first_result.status == HandoffStatus.COMPLETED
    assert first_result.security_status == "accepted"
    assert first_result.solidary_point_demo == 1

    assert second_result.status == HandoffStatus.REJECTED_BY_SECURITY
    assert second_result.frontend_status == "ready_for_security_flow"
    assert second_result.security_status == "rejected"
    assert second_result.handoff_completed is False
    assert second_result.frontend_ready is True
    assert second_result.security_flow_executed is True
    assert second_result.solidary_point_demo == 0
    assert "replay_sync_event_id" in second_result.risk_flags


def test_handoff_needs_review_when_security_detects_priority_user_trip_limit():
    ledger = SyncSecurityLedger()

    first_frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-priority-limit-001",
        candidate_collaborator=create_demo_candidate_collaborator(
            collaborator_token="test-handoff-collaborator-priority-limit-001",
        ),
    )

    second_frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-priority-limit-002",
        candidate_collaborator=create_demo_candidate_collaborator(
            collaborator_token="test-handoff-collaborator-priority-limit-002",
        ),
    )

    first_request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-priority-limit-handoff-001",
        frontend_request=first_frontend_request,
    )

    second_request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-priority-limit-handoff-002",
        frontend_request=second_frontend_request,
    )

    first_result = execute_solidary_bonus_handoff(
        request=first_request,
        ledger=ledger,
    )

    second_result = execute_solidary_bonus_handoff(
        request=second_request,
        ledger=ledger,
    )

    assert first_result.status == HandoffStatus.COMPLETED
    assert first_result.security_status == "accepted"
    assert first_result.solidary_point_demo == 1

    assert second_result.status == HandoffStatus.NEEDS_REVIEW
    assert second_result.frontend_status == "ready_for_security_flow"
    assert second_result.security_status == "needs_review"
    assert second_result.handoff_completed is False
    assert second_result.solidary_point_demo == 0
    assert "priority_user_trip_sync_limit_exceeded" in second_result.risk_flags


def test_handoff_needs_review_when_security_detects_collaborator_trip_limit():
    ledger = SyncSecurityLedger()

    first_frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-collaborator-limit-001",
        priority_account_context=create_demo_priority_account_frontend_context(
            account_demo_id="test-handoff-account-collab-limit-001",
            card_demo_id="test-handoff-card-collab-limit-001",
            priority_user_token="test-handoff-priority-user-collab-limit-001",
            priority_attribute_token="test-handoff-priority-attribute-collab-limit-001",
        ),
        candidate_collaborator=create_demo_candidate_collaborator(
            collaborator_token="test-handoff-collaborator-limit-same",
        ),
    )

    second_frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-collaborator-limit-002",
        priority_account_context=create_demo_priority_account_frontend_context(
            account_demo_id="test-handoff-account-collab-limit-002",
            card_demo_id="test-handoff-card-collab-limit-002",
            priority_user_token="test-handoff-priority-user-collab-limit-002",
            priority_attribute_token="test-handoff-priority-attribute-collab-limit-002",
        ),
        candidate_collaborator=create_demo_candidate_collaborator(
            collaborator_token="test-handoff-collaborator-limit-same",
        ),
    )

    third_frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-collaborator-limit-003",
        priority_account_context=create_demo_priority_account_frontend_context(
            account_demo_id="test-handoff-account-collab-limit-003",
            card_demo_id="test-handoff-card-collab-limit-003",
            priority_user_token="test-handoff-priority-user-collab-limit-003",
            priority_attribute_token="test-handoff-priority-attribute-collab-limit-003",
        ),
        candidate_collaborator=create_demo_candidate_collaborator(
            collaborator_token="test-handoff-collaborator-limit-same",
        ),
    )

    first_request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-collaborator-limit-handoff-001",
        frontend_request=first_frontend_request,
    )

    second_request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-collaborator-limit-handoff-002",
        frontend_request=second_frontend_request,
    )

    third_request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-collaborator-limit-handoff-003",
        frontend_request=third_frontend_request,
    )

    first_result = execute_solidary_bonus_handoff(
        request=first_request,
        ledger=ledger,
    )

    second_result = execute_solidary_bonus_handoff(
        request=second_request,
        ledger=ledger,
    )

    third_result = execute_solidary_bonus_handoff(
        request=third_request,
        ledger=ledger,
    )

    assert first_result.status == HandoffStatus.COMPLETED
    assert first_result.security_status == "accepted"
    assert first_result.solidary_point_demo == 1

    assert second_result.status == HandoffStatus.COMPLETED
    assert second_result.security_status == "accepted"
    assert second_result.solidary_point_demo == 1

    assert third_result.status == HandoffStatus.NEEDS_REVIEW
    assert third_result.security_status == "needs_review"
    assert third_result.solidary_point_demo == 0
    assert "collaborator_trip_sync_limit_exceeded" in third_result.risk_flags


def test_handoff_preserves_minimal_payload_without_sensitive_data():
    frontend_request = create_demo_solidary_bonus_frontend_request(
        frontend_request_demo_id="test-handoff-minimal-payload-001",
        frontend_channel=FrontendChannel.ACCOUNT_PANEL,
        candidate_collaborator=create_demo_candidate_collaborator(
            collaborator_token="test-handoff-collaborator-minimal-payload-001",
            selection_method=RecipientSelectionMethod.TEMPORARY_CODE_DEMO,
        ),
    )

    request = create_demo_solidary_bonus_handoff_request(
        handoff_demo_id="test-handoff-minimal-payload-001",
        frontend_request=frontend_request,
    )

    result = execute_solidary_bonus_handoff(request)

    frontend_payload = result.frontend_result["security_flow_payload_demo"]
    security_result = result.security_result

    assert result.status == HandoffStatus.COMPLETED

    forbidden_keys = {
        "dni",
        "documento",
        "nombre",
        "apellido",
        "domicilio",
        "diagnostico",
        "diagnóstico",
        "cud",
        "certificado_medico",
        "historia_clinica",
        "telefono",
        "email",
    }

    assert forbidden_keys.isdisjoint(set(frontend_payload.keys()))
    assert forbidden_keys.isdisjoint(set(security_result.keys()))

    assert frontend_payload["sync_event_demo_id"] == "test-handoff-minimal-payload-001"
    assert frontend_payload["collaborator_token"] == "test-handoff-collaborator-minimal-payload-001"


def test_assert_no_prohibited_fields_rejects_dni():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "handoff_demo_id": "test-handoff-sensitive-dni",
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


def test_create_demo_handoff_request_rejects_empty_handoff_id():
    with pytest.raises(ValueError):
        create_demo_solidary_bonus_handoff_request(
            handoff_demo_id="",
        )
